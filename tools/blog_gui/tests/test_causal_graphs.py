from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest import mock


BLOG_GUI = Path(__file__).resolve().parents[1]
if str(BLOG_GUI) not in sys.path:
    sys.path.insert(0, str(BLOG_GUI))

from causal_graphs import (  # noqa: E402
    GraphStore,
    GraphValidationError,
    atomic_replace_texts,
    canonical_figure,
    extract_graph_ids,
    generate_graph_id,
    graph_to_svg,
    publish_bundles,
    validate_graph,
)


GRAPH_ID = "cg-20260801-ab12cd34"


def graph_model(**updates: object) -> dict[str, object]:
    model: dict[str, object] = {
        "id": GRAPH_ID,
        "schema_version": 1,
        "alt": "Treatment X causes outcome Y; U is latent.",
        "caption": "A small causal graph.",
        "nodes": [
            {"id": "x", "label": "처치 X", "x": 80, "y": 40, "role": "exposure", "observed": True},
            {"id": "y", "label": "Outcome & Y", "x": 80, "y": 220, "role": "outcome", "observed": True},
            {"id": "u", "label": "U <latent>", "x": 240, "y": 40, "role": "standard", "observed": False},
        ],
        "edges": [
            {"id": "e1", "source": "x", "target": "y", "kind": "directed", "label": "β < 1"},
            {"id": "e2", "source": "u", "target": "y", "kind": "bidirected", "label": ""},
        ],
    }
    model.update(updates)
    return model


class GraphValidationTests(unittest.TestCase):
    def test_generate_safe_id(self) -> None:
        graph_id = generate_graph_id(datetime(2026, 8, 1))
        self.assertRegex(graph_id, r"^cg-20260801-[a-z0-9]{8}$")

    def test_normalizes_unicode_and_accepts_bidirected_edges(self) -> None:
        model = graph_model()
        model["nodes"][0]["label"] = "  e\u0301  "  # type: ignore[index]
        graph = validate_graph(model)
        self.assertEqual(graph["nodes"][0]["label"], "é")
        self.assertEqual(graph["edges"][1]["kind"], "bidirected")

    def test_rejects_duplicate_label_and_latent_role(self) -> None:
        model = graph_model()
        model["nodes"][1]["label"] = "처치 x"  # type: ignore[index]
        with self.assertRaisesRegex(GraphValidationError, "Duplicate node label"):
            validate_graph(model)

        model = graph_model()
        model["nodes"][0]["observed"] = False  # type: ignore[index]
        with self.assertRaisesRegex(GraphValidationError, "Latent node"):
            validate_graph(model)

    def test_rejects_duplicate_self_missing_and_cycle_edges(self) -> None:
        for extra, message in (
            ({"id": "e3", "source": "x", "target": "y", "kind": "directed", "label": ""}, "Duplicate directed"),
            ({"id": "e3", "source": "x", "target": "x", "kind": "directed", "label": ""}, "Self-edge"),
            ({"id": "e3", "source": "missing", "target": "x", "kind": "directed", "label": ""}, "missing node"),
        ):
            model = graph_model()
            model["edges"].append(extra)  # type: ignore[union-attr]
            with self.assertRaisesRegex(GraphValidationError, message):
                validate_graph(model)

        model = graph_model()
        model["edges"].append(  # type: ignore[union-attr]
            {"id": "e3", "source": "y", "target": "x", "kind": "directed", "label": ""}
        )
        with self.assertRaisesRegex(GraphValidationError, "acyclic"):
            validate_graph(model)

    def test_rejects_unsafe_id_and_more_than_fifty_nodes(self) -> None:
        with self.assertRaisesRegex(GraphValidationError, "Invalid causal graph ID"):
            validate_graph(graph_model(id="../../escape"))
        nodes = [
            {"id": f"n{i}", "label": f"N {i}", "x": i, "y": i, "role": "standard", "observed": True}
            for i in range(51)
        ]
        with self.assertRaisesRegex(GraphValidationError, "at most 50"):
            validate_graph(graph_model(nodes=nodes, edges=[]))


class RenderingTests(unittest.TestCase):
    def test_figure_is_canonical_and_extractable(self) -> None:
        model = graph_model(alt='A "quoted" graph & more', caption="A < B & C")
        figure = canonical_figure(model)
        self.assertIn('alt="A &quot;quoted&quot; graph &amp; more"', figure)
        self.assertIn("<figcaption>A &lt; B &amp; C</figcaption>", figure)
        self.assertEqual(extract_graph_ids(f"before\n\n{figure}\n\nafter"), [GRAPH_ID])
        self.assertEqual(extract_graph_ids(figure + "\n" + figure), [GRAPH_ID])

    def test_svg_is_deterministic_white_and_xml_safe(self) -> None:
        first = graph_to_svg(graph_model())
        second = graph_to_svg(graph_model())
        self.assertEqual(first, second)
        self.assertIn('fill="#ffffff"', first)
        self.assertIn("Outcome &amp; Y", first)
        self.assertIn("U &lt;latent&gt;", first)
        self.assertIn("β &lt; 1", first)
        self.assertIn('marker-start="url(#arrow)"', first)
        self.assertIn('stroke-dasharray="7 5"', first)
        self.assertNotIn("Outcome & Y", first)


class StorageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name).resolve()
        (self.root / "_drafts").mkdir()
        (self.root / "_posts").mkdir()
        self.store = GraphStore(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_save_draft_and_published_graph(self) -> None:
        self.store.save(graph_model(), published=False)
        self.assertTrue(self.store.draft_source(GRAPH_ID).exists())
        self.assertFalse(self.store.published_svg(GRAPH_ID).exists())

        self.store.save(graph_model(), published=True)
        self.assertEqual(json.loads(self.store.published_source(GRAPH_ID).read_text())["id"], GRAPH_ID)
        self.assertIn("<svg", self.store.published_svg(GRAPH_ID).read_text())

    def test_publish_promotes_graph_before_post_and_removes_draft_sources(self) -> None:
        graph = self.store.save(graph_model(), published=False)
        figure = canonical_figure(graph)
        draft = self.root / "_drafts" / "example.md"
        post = self.root / "_posts" / "2026-08-01-example.md"
        draft.write_text(figure, encoding="utf-8")

        promoted = self.store.promote_draft(draft, post, f"---\n---\n{figure}\n", figure)
        self.assertEqual(promoted, (GRAPH_ID,))
        self.assertTrue(post.exists())
        self.assertTrue(self.store.published_source(GRAPH_ID).exists())
        self.assertTrue(self.store.published_svg(GRAPH_ID).exists())
        self.assertFalse(draft.exists())
        self.assertFalse(self.store.draft_source(GRAPH_ID).exists())

    def test_atomic_replace_rolls_back_existing_files(self) -> None:
        first = self.root / "assets" / "first.txt"
        second = self.root / "assets" / "second.txt"
        first.parent.mkdir()
        first.write_text("old first", encoding="utf-8")
        second.write_text("old second", encoding="utf-8")
        real_replace = os.replace
        installs = 0

        def failing_replace(source: object, target: object) -> None:
            nonlocal installs
            source_path = Path(source)  # type: ignore[arg-type]
            if source_path.suffix == ".tmp":
                installs += 1
                if installs == 2:
                    raise OSError("simulated disk failure")
            real_replace(source, target)

        with mock.patch("causal_graphs.os.replace", side_effect=failing_replace):
            with self.assertRaisesRegex(OSError, "simulated"):
                atomic_replace_texts({first: "new first", second: "new second"})
        self.assertEqual(first.read_text(), "old first")
        self.assertEqual(second.read_text(), "old second")

    def test_delete_keeps_shared_graph_and_does_not_clean_orphans(self) -> None:
        graph = self.store.save(graph_model(), published=False)
        figure = canonical_figure(graph)
        first = self.root / "_drafts" / "first.md"
        second = self.root / "_drafts" / "second.md"
        orphan = self.store.draft_graphs / "cg-20260801-deadbeef.json"
        orphan.write_text("{}", encoding="utf-8")
        first.write_text(figure, encoding="utf-8")
        second.write_text(figure, encoding="utf-8")

        self.assertEqual(self.store.draft_graph_delete_summary(first, figure), (0, 1))
        self.store.delete_draft(first, figure)
        self.assertTrue(self.store.draft_source(GRAPH_ID).exists())
        self.assertTrue(orphan.exists())
        self.store.delete_draft(second, figure)
        self.assertFalse(self.store.draft_source(GRAPH_ID).exists())
        self.assertTrue(orphan.exists())

    def test_publish_bundle_includes_graph_only_changes(self) -> None:
        graph = self.store.save(graph_model(), published=True)
        figure = canonical_figure(graph)
        post = self.root / "_posts" / "2026-08-01-example.md"
        post.write_text(figure, encoding="utf-8")
        changed = [f"assets/causal-graphs/{GRAPH_ID}.svg", f"_graph_sources/{GRAPH_ID}.json"]
        bundles = publish_bundles(self.root, [post], changed)
        self.assertEqual(len(bundles), 1)
        self.assertEqual([path.relative_to(self.root).as_posix() for path in bundles[0].paths], changed)
        self.assertEqual(bundles[0].graph_ids, (GRAPH_ID,))


if __name__ == "__main__":
    unittest.main()
