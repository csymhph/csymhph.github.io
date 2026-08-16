from __future__ import annotations

import html
import json
import math
import os
import re
import secrets
import tempfile
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping


SCHEMA_VERSION = 1
MAX_NODES = 50
GRAPH_ID_RE = re.compile(r"^cg-\d{8}-[a-z0-9]{8}$")
ELEMENT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
GRAPH_FIGURE_RE = re.compile(
    r'<figure\s+class="causal-figure"\s+data-causal-graph="(?P<id>cg-\d{8}-[a-z0-9]{8})">'
    r"\s*<img\s+src=\"/assets/causal-graphs/(?P=id)\.svg\"\s+alt=\"(?P<alt>[^\"]*)\">"
    r"(?:\s*<figcaption>(?P<caption>.*?)</figcaption>)?\s*</figure>",
    re.DOTALL,
)


class GraphValidationError(ValueError):
    """Raised when a causal graph does not satisfy the v1 contract."""


@dataclass(frozen=True)
class PublishBundle:
    post: Path
    paths: tuple[Path, ...]
    graph_ids: tuple[str, ...]


def generate_graph_id(now: datetime | None = None) -> str:
    date_text = (now or datetime.now()).strftime("%Y%m%d")
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    suffix = "".join(secrets.choice(alphabet) for _ in range(8))
    return f"cg-{date_text}-{suffix}"


def validate_graph_id(graph_id: str) -> str:
    if not isinstance(graph_id, str) or not GRAPH_ID_RE.fullmatch(graph_id):
        raise GraphValidationError("Invalid causal graph ID.")
    return graph_id


def _normalized_label(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise GraphValidationError(f"{field} must be a string.")
    label = unicodedata.normalize("NFC", value).strip()
    if not label:
        raise GraphValidationError(f"{field} cannot be empty.")
    return label


def _finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise GraphValidationError(f"{field} must be a finite number.")
    number = float(value)
    if not math.isfinite(number):
        raise GraphValidationError(f"{field} must be a finite number.")
    return number


def validate_graph(model: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(model, Mapping):
        raise GraphValidationError("Causal graph must be a JSON object.")

    graph_id = validate_graph_id(model.get("id", ""))
    if model.get("schema_version") != SCHEMA_VERSION:
        raise GraphValidationError(f"schema_version must be {SCHEMA_VERSION}.")

    alt = _normalized_label(model.get("alt"), "Alternative text")
    caption_value = model.get("caption", "")
    if not isinstance(caption_value, str):
        raise GraphValidationError("Caption must be a string.")
    caption = unicodedata.normalize("NFC", caption_value).strip()

    raw_nodes = model.get("nodes")
    raw_edges = model.get("edges")
    if not isinstance(raw_nodes, list) or not isinstance(raw_edges, list):
        raise GraphValidationError("nodes and edges must be arrays.")
    if not raw_nodes:
        raise GraphValidationError("Add at least one node.")
    if len(raw_nodes) > MAX_NODES:
        raise GraphValidationError(f"Causal graphs support at most {MAX_NODES} nodes.")

    nodes: list[dict[str, Any]] = []
    node_ids: set[str] = set()
    normalized_labels: set[str] = set()
    roles = {"standard", "exposure", "outcome", "adjusted"}
    for index, raw_node in enumerate(raw_nodes):
        if not isinstance(raw_node, Mapping):
            raise GraphValidationError(f"Node {index + 1} must be an object.")
        node_id = raw_node.get("id")
        if not isinstance(node_id, str) or not ELEMENT_ID_RE.fullmatch(node_id):
            raise GraphValidationError(f"Node {index + 1} has an invalid ID.")
        if node_id in node_ids:
            raise GraphValidationError(f"Duplicate node ID: {node_id}")
        node_ids.add(node_id)

        label = _normalized_label(raw_node.get("label"), f"Node {node_id} label")
        label_key = label.casefold()
        if label_key in normalized_labels:
            raise GraphValidationError(f"Duplicate node label: {label}")
        normalized_labels.add(label_key)

        role = raw_node.get("role", "standard")
        if role not in roles:
            raise GraphValidationError(f"Node {node_id} has an invalid role.")
        observed = raw_node.get("observed", True)
        if not isinstance(observed, bool):
            raise GraphValidationError(f"Node {node_id} observed must be boolean.")
        if not observed and role != "standard":
            raise GraphValidationError(
                f"Latent node {label} cannot also be exposure, outcome, or adjusted."
            )

        nodes.append(
            {
                "id": node_id,
                "label": label,
                "x": _finite_number(raw_node.get("x"), f"Node {node_id} x"),
                "y": _finite_number(raw_node.get("y"), f"Node {node_id} y"),
                "role": role,
                "observed": observed,
            }
        )

    edges: list[dict[str, Any]] = []
    edge_ids: set[str] = set()
    edge_keys: set[tuple[str, str, str]] = set()
    directed_pairs: list[tuple[str, str]] = []
    for index, raw_edge in enumerate(raw_edges):
        if not isinstance(raw_edge, Mapping):
            raise GraphValidationError(f"Edge {index + 1} must be an object.")
        edge_id = raw_edge.get("id")
        if not isinstance(edge_id, str) or not ELEMENT_ID_RE.fullmatch(edge_id):
            raise GraphValidationError(f"Edge {index + 1} has an invalid ID.")
        if edge_id in edge_ids:
            raise GraphValidationError(f"Duplicate edge ID: {edge_id}")
        edge_ids.add(edge_id)

        source = raw_edge.get("source")
        target = raw_edge.get("target")
        if source not in node_ids or target not in node_ids:
            raise GraphValidationError(f"Edge {edge_id} refers to a missing node.")
        if source == target:
            raise GraphValidationError(f"Self-edge is not allowed: {edge_id}")
        kind = raw_edge.get("kind", "directed")
        if kind not in {"directed", "bidirected"}:
            raise GraphValidationError(f"Edge {edge_id} has an invalid kind.")

        key_source, key_target = str(source), str(target)
        if kind == "bidirected" and key_source > key_target:
            key_source, key_target = key_target, key_source
        edge_key = (kind, key_source, key_target)
        if edge_key in edge_keys:
            raise GraphValidationError(
                f"Duplicate {kind} edge between {source} and {target}."
            )
        edge_keys.add(edge_key)

        label_value = raw_edge.get("label", "")
        if not isinstance(label_value, str):
            raise GraphValidationError(f"Edge {edge_id} label must be a string.")
        label = unicodedata.normalize("NFC", label_value).strip()
        edges.append(
            {
                "id": edge_id,
                "source": str(source),
                "target": str(target),
                "kind": kind,
                "label": label,
            }
        )
        if kind == "directed":
            directed_pairs.append((str(source), str(target)))

    _validate_acyclic(node_ids, directed_pairs)
    return {
        "id": graph_id,
        "schema_version": SCHEMA_VERSION,
        "alt": alt,
        "caption": caption,
        "nodes": nodes,
        "edges": edges,
    }


def _validate_acyclic(node_ids: Iterable[str], edges: Iterable[tuple[str, str]]) -> None:
    adjacency = {node_id: [] for node_id in node_ids}
    indegree = {node_id: 0 for node_id in node_ids}
    for source, target in edges:
        adjacency[source].append(target)
        indegree[target] += 1

    queue = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
    visited = 0
    while queue:
        node_id = queue.pop(0)
        visited += 1
        for target in sorted(adjacency[node_id]):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
                queue.sort()
    if visited != len(indegree):
        raise GraphValidationError("Directed edges must form an acyclic graph.")


def canonical_figure(model: Mapping[str, Any]) -> str:
    graph = validate_graph(model)
    graph_id = graph["id"]
    alt = html.escape(graph["alt"], quote=True)
    lines = [
        f'<figure class="causal-figure" data-causal-graph="{graph_id}">',
        f'  <img src="/assets/causal-graphs/{graph_id}.svg" alt="{alt}">',
    ]
    if graph["caption"]:
        lines.append(f"  <figcaption>{html.escape(graph['caption'])}</figcaption>")
    lines.append("</figure>")
    return "\n".join(lines)


def extract_graph_ids(markdown: str) -> list[str]:
    if not isinstance(markdown, str):
        return []
    seen: set[str] = set()
    graph_ids: list[str] = []
    for match in GRAPH_FIGURE_RE.finditer(markdown):
        graph_id = match.group("id")
        if graph_id not in seen:
            seen.add(graph_id)
            graph_ids.append(graph_id)
    return graph_ids


def graph_to_svg(model: Mapping[str, Any]) -> str:
    graph = validate_graph(model)
    nodes = sorted(graph["nodes"], key=lambda item: item["id"])
    edges = sorted(graph["edges"], key=lambda item: item["id"])
    by_id = {node["id"]: node for node in nodes}
    margin = 72.0
    min_x = min(node["x"] for node in nodes) - margin
    min_y = min(node["y"] for node in nodes) - margin
    max_x = max(node["x"] for node in nodes) + margin
    max_y = max(node["y"] for node in nodes) + margin
    width = max(240.0, max_x - min_x)
    height = max(180.0, max_y - min_y)

    def sx(value: float) -> float:
        return value - min_x

    def sy(value: float) -> float:
        return value - min_y

    def number(value: float) -> str:
        rounded = round(value, 2)
        return str(int(rounded)) if rounded.is_integer() else f"{rounded:.2f}".rstrip("0")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-labelledby="title desc" viewBox="0 0 {number(width)} {number(height)}">'
        ),
        f"  <title id=\"title\">{html.escape(graph['alt'])}</title>",
        "  <desc id=\"desc\">Static causal graph. Directed arrows show causal paths; double-headed arrows show bidirected relationships.</desc>",
        f'  <rect width="{number(width)}" height="{number(height)}" fill="#ffffff"/>',
        "  <defs>",
        '    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">',
        '      <path d="M 0 0 L 10 5 L 0 10 z" fill="#24272b"/>',
        "    </marker>",
        "  </defs>",
        '  <g class="edges" fill="none" stroke="#24272b" stroke-width="2">',
    ]

    for edge in edges:
        source = by_id[edge["source"]]
        target = by_id[edge["target"]]
        center_x1, center_y1 = sx(source["x"]), sy(source["y"])
        center_x2, center_y2 = sx(target["x"]), sy(target["y"])
        dx, dy = center_x2 - center_x1, center_y2 - center_y1

        def boundary_fraction(node: Mapping[str, Any]) -> float:
            radius_x = max(42.0, min(105.0, 14.0 + len(node["label"]) * 4.5))
            radius_y = 34.0 if node["role"] == "outcome" else 28.0
            denominator = math.sqrt((dx / radius_x) ** 2 + (dy / radius_y) ** 2)
            return 0.0 if denominator == 0 else min(0.45, 1.0 / denominator)

        source_fraction = boundary_fraction(source)
        target_fraction = boundary_fraction(target)
        x1 = center_x1 + dx * source_fraction
        y1 = center_y1 + dy * source_fraction
        x2 = center_x2 - dx * target_fraction
        y2 = center_y2 - dy * target_fraction
        marker_start = ' marker-start="url(#arrow)"' if edge["kind"] == "bidirected" else ""
        lines.append(
            f'    <line data-edge="{html.escape(edge["id"], quote=True)}" '
            f'x1="{number(x1)}" y1="{number(y1)}" x2="{number(x2)}" y2="{number(y2)}"'
            f'{marker_start} marker-end="url(#arrow)"/>'
        )
        if edge["label"]:
            label_x = (x1 + x2) / 2
            label_y = (y1 + y2) / 2 - 8
            lines.append(
                f'    <text x="{number(label_x)}" y="{number(label_y)}" text-anchor="middle" '
                f'fill="#24272b" stroke="#ffffff" stroke-width="4" paint-order="stroke" '
                f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="13">'
                f'{html.escape(edge["label"])}</text>'
            )
    lines.append("  </g>")
    lines.append('  <g class="nodes" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif">')

    role_style = {
        "standard": ("#ffffff", "#374151", 2),
        "exposure": ("#e8f2ff", "#0057b8", 3),
        "outcome": ("#fff2df", "#a34b00", 3),
        "adjusted": ("#f0eaff", "#6542a6", 3),
    }
    for node in nodes:
        x, y = sx(node["x"]), sy(node["y"])
        half_width = max(42.0, min(105.0, 14.0 + len(node["label"]) * 4.5))
        fill, stroke, stroke_width = role_style[node["role"]]
        dash = ' stroke-dasharray="7 5"' if not node["observed"] else ""
        common = (
            f'data-node="{html.escape(node["id"], quote=True)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}"{dash}'
        )
        if node["role"] == "exposure":
            lines.append(
                f'    <rect {common} x="{number(x - half_width)}" y="{number(y - 27)}" '
                f'width="{number(half_width * 2)}" height="54" rx="8"/>'
            )
        elif node["role"] == "outcome":
            points = f"{number(x)},{number(y - 34)} {number(x + half_width)},{number(y)} {number(x)},{number(y + 34)} {number(x - half_width)},{number(y)}"
            lines.append(f'    <polygon {common} points="{points}"/>')
        elif node["role"] == "adjusted":
            points = f"{number(x - half_width + 12)},{number(y - 28)} {number(x + half_width - 12)},{number(y - 28)} {number(x + half_width)},{number(y)} {number(x + half_width - 12)},{number(y + 28)} {number(x - half_width + 12)},{number(y + 28)} {number(x - half_width)},{number(y)}"
            lines.append(f'    <polygon {common} points="{points}"/>')
        else:
            lines.append(
                f'    <ellipse {common} cx="{number(x)}" cy="{number(y)}" '
                f'rx="{number(half_width)}" ry="28"/>'
            )
        lines.append(
            f'    <text x="{number(x)}" y="{number(y + 5)}" fill="#111827" font-size="15" font-weight="600">'
            f'{html.escape(node["label"])}</text>'
        )
    lines.extend(["  </g>", "</svg>", ""])
    return "\n".join(lines)


class GraphStore:
    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.draft_graphs = self.root / "_drafts" / "graphs"
        self.sources = self.root / "_graph_sources"
        self.assets = self.root / "assets" / "causal-graphs"

    def draft_source(self, graph_id: str) -> Path:
        return self.draft_graphs / f"{validate_graph_id(graph_id)}.json"

    def published_source(self, graph_id: str) -> Path:
        return self.sources / f"{validate_graph_id(graph_id)}.json"

    def published_svg(self, graph_id: str) -> Path:
        return self.assets / f"{validate_graph_id(graph_id)}.svg"

    def load(self, graph_id: str, *, published: bool) -> dict[str, Any]:
        path = self.published_source(graph_id) if published else self.draft_source(graph_id)
        try:
            model = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GraphValidationError(f"Could not load causal graph {graph_id}: {exc}") from exc
        graph = validate_graph(model)
        if graph["id"] != graph_id:
            raise GraphValidationError(
                f"Causal graph source {graph_id} contains a different graph ID."
            )
        return graph

    def load_for_markdown(self, markdown: str, *, published: bool) -> list[dict[str, Any]]:
        return [self.load(graph_id, published=published) for graph_id in extract_graph_ids(markdown)]

    def save(self, model: Mapping[str, Any], *, published: bool) -> dict[str, Any]:
        graph = validate_graph(model)
        if published:
            replacements = {
                self.published_source(graph["id"]): _json_text(graph),
                self.published_svg(graph["id"]): graph_to_svg(graph),
            }
        else:
            replacements = {self.draft_source(graph["id"]): _json_text(graph)}
        atomic_replace_texts(replacements)
        return graph

    def promote_draft(
        self,
        draft_path: Path,
        post_path: Path,
        post_text: str,
        markdown_body: str,
    ) -> tuple[str, ...]:
        graph_ids = tuple(extract_graph_ids(markdown_body))
        replacements: dict[Path, str] = {}
        graphs: dict[str, dict[str, Any]] = {}
        for graph_id in graph_ids:
            graphs[graph_id] = self.load(graph_id, published=False)
        for graph_id, graph in graphs.items():
            replacements[self.published_svg(graph_id)] = graph_to_svg(graph)
        for graph_id, graph in graphs.items():
            replacements[self.published_source(graph_id)] = _json_text(graph)
        replacements[post_path] = post_text
        atomic_replace_texts(replacements)

        try:
            draft_path.unlink()
        except FileNotFoundError:
            pass
        for graph_id in graph_ids:
            source = self.draft_source(graph_id)
            if source.exists() and not _graph_referenced_elsewhere(
                graph_id, self.root / "_drafts", excluding=draft_path
            ):
                source.unlink()
        return graph_ids

    def draft_graph_delete_summary(self, draft_path: Path, markdown: str) -> tuple[int, int]:
        exclusive = 0
        shared = 0
        for graph_id in extract_graph_ids(markdown):
            if _graph_referenced_elsewhere(graph_id, self.root / "_drafts", excluding=draft_path):
                shared += 1
            elif self.draft_source(graph_id).exists():
                exclusive += 1
        return exclusive, shared

    def delete_draft(self, draft_path: Path, markdown: str) -> tuple[int, int]:
        exclusive, shared = self.draft_graph_delete_summary(draft_path, markdown)
        graph_ids = extract_graph_ids(markdown)
        draft_path.unlink()
        for graph_id in graph_ids:
            if not _graph_referenced_elsewhere(graph_id, self.root / "_drafts", excluding=draft_path):
                source = self.draft_source(graph_id)
                if source.exists():
                    source.unlink()
        return exclusive, shared


def _json_text(graph: Mapping[str, Any]) -> str:
    return json.dumps(graph, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _graph_referenced_elsewhere(graph_id: str, drafts_dir: Path, excluding: Path) -> bool:
    for path in drafts_dir.glob("*.md"):
        if path.resolve() == excluding.resolve():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if graph_id in extract_graph_ids(text):
            return True
    return False


def atomic_replace_texts(replacements: Mapping[Path, str]) -> None:
    """Replace a set of UTF-8 text files and restore all prior targets on failure."""
    prepared: dict[Path, Path] = {}
    backups: dict[Path, Path] = {}
    installed: list[Path] = []
    try:
        for target, content in replacements.items():
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
            temp_path = Path(temp_name)
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            prepared[target] = temp_path

        for target in replacements:
            if target.exists():
                fd, backup_name = tempfile.mkstemp(
                    prefix=f".{target.name}.", suffix=".bak", dir=target.parent
                )
                os.close(fd)
                backup_path = Path(backup_name)
                backup_path.unlink()
                os.replace(target, backup_path)
                backups[target] = backup_path
            os.replace(prepared[target], target)
            installed.append(target)
    except Exception:
        for target in reversed(installed):
            if target.exists():
                target.unlink()
        for target, backup in backups.items():
            if backup.exists():
                os.replace(backup, target)
        raise
    finally:
        for temp_path in prepared.values():
            if temp_path.exists():
                temp_path.unlink()
        for backup in backups.values():
            if backup.exists():
                backup.unlink()


def publish_bundles(
    root: Path,
    posts: Iterable[Path],
    changed_relative_paths: Iterable[str],
) -> list[PublishBundle]:
    root = Path(root).resolve()
    changed = {path.replace("\\", "/") for path in changed_relative_paths}
    bundles: list[PublishBundle] = []
    for post in posts:
        try:
            markdown = post.read_text(encoding="utf-8")
        except OSError:
            markdown = ""
        graph_ids = tuple(extract_graph_ids(markdown))
        paths = [post]
        for graph_id in graph_ids:
            paths.extend(
                [
                    root / "assets" / "causal-graphs" / f"{graph_id}.svg",
                    root / "_graph_sources" / f"{graph_id}.json",
                ]
            )
        relevant = []
        for path in paths:
            try:
                relative = path.resolve().relative_to(root).as_posix()
            except ValueError:
                continue
            if relative in changed:
                relevant.append(path)
        if relevant:
            # The post provides review context even when only a graph changed, but only
            # changed paths are staged so an unchanged post is never needlessly touched.
            bundles.append(PublishBundle(post=post, paths=tuple(relevant), graph_ids=graph_ids))
    return bundles
