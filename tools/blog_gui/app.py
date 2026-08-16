from __future__ import annotations

import os
import re
import signal
import subprocess
import threading
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

if __package__:
    from .causal_graphs import (
        GraphStore,
        GraphValidationError,
        PublishBundle,
        canonical_figure,
        generate_graph_id,
        publish_bundles,
    )
    from .rich_editor import themed_markdown_editor
else:
    try:
        from causal_graphs import (
            GraphStore,
            GraphValidationError,
            PublishBundle,
            canonical_figure,
            generate_graph_id,
            publish_bundles,
        )
        from rich_editor import themed_markdown_editor
    except ModuleNotFoundError:
        from tools.blog_gui.causal_graphs import (
            GraphStore,
            GraphValidationError,
            PublishBundle,
            canonical_figure,
            generate_graph_id,
            publish_bundles,
        )
        from tools.blog_gui.rich_editor import themed_markdown_editor


ROOT = Path(__file__).resolve().parents[2]
DRAFTS_DIR = ROOT / "_drafts"
POSTS_DIR = ROOT / "_posts"
WRITING_GUIDE_PATH = Path(__file__).with_name("WRITING_GUIDE.md")
MATHJAX_INCLUDE = "{% include mathjax.html %}"
FLASH_KEY = "blog_gui_flash"
VIEW_KEY = "blog_gui_view"
WRITING_MODE_KEY = "blog_gui_writing_mode"
NEW_DRAFT_VERSION_KEY = "blog_gui_new_draft_version"
DARK_MODE_KEY = "blog_gui_dark_mode"
SITE_URL = "https://csymhph.github.io"
GRAPH_RESPONSE_PREFIX = "blog_gui_graph_response"
GRAPH_REQUEST_PREFIX = "blog_gui_graph_request"
GRAPH_ID_PREFIX = "blog_gui_graph_id"


POST_TYPE_OPTIONS = ("normal", "math note", "project note")
COMMIT_AUTHOR_LINE = "Co-Authored-By: Claude <noreply@anthropic.com>"
EDITOR_FEATURES = {
    "codeblock": True,
    "math": True,
    "table": True,
    "image": False,
    "link": True,
}
GRAPH_STORE = GraphStore(ROOT)


def hide_streamlit_chrome() -> None:
    st.markdown(
        """
        <style>
        .stDeployButton,
        [data-testid="stDeployButton"],
        [data-testid="stToolbar"],
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
        }
        header [data-testid="stToolbar"] {
            display: none !important;
        }
        [data-testid="stMainBlockContainer"] {
            max-width: 1120px;
            padding-top: 3.5rem;
            padding-bottom: 5rem;
        }
        .stApp,
        .stApp button,
        .stApp input,
        .stApp textarea,
        .stApp [data-baseweb="select"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                Helvetica, Arial, sans-serif;
        }
        .stApp h1,
        .stApp h2,
        .stApp h3 {
            letter-spacing: -0.035em;
        }
        .studio-brand {
            padding: 0.45rem 0 1.1rem;
        }
        .studio-brand__eyebrow,
        .workspace-kicker {
            margin: 0 0 0.35rem;
            color: var(--studio-accent) !important;
            font-size: 0.72rem;
            font-weight: 750;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        .studio-brand__title {
            margin: 0;
            color: var(--studio-text) !important;
            font-size: 1.3rem;
            font-weight: 720;
            letter-spacing: -0.035em;
        }
        .studio-brand__copy {
            margin: 0.2rem 0 0;
            color: var(--studio-muted) !important;
            font-size: 0.78rem;
        }
        .workspace-hero {
            max-width: 760px;
            padding-bottom: 1.7rem;
        }
        .workspace-title {
            margin: 0;
            color: var(--studio-text) !important;
            font-size: clamp(2.6rem, 6vw, 4.8rem);
            font-weight: 740;
            letter-spacing: -0.065em;
            line-height: 0.98;
        }
        .workspace-lede {
            max-width: 58ch;
            margin: 1rem 0 0;
            color: var(--studio-muted) !important;
            font-size: 1.02rem;
            line-height: 1.6;
        }
        .workspace-stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.25rem 0 2rem;
        }
        .workspace-stat {
            padding: 1rem 1.1rem;
            border: 1px solid var(--studio-border);
            border-radius: 16px;
            background: var(--studio-surface);
        }
        .workspace-stat__value {
            display: block;
            color: var(--studio-text);
            font-size: 1.45rem;
            font-weight: 720;
            letter-spacing: -0.04em;
        }
        .workspace-stat__label {
            color: var(--studio-muted);
            font-size: 0.75rem;
        }
        [data-testid="stSidebar"] [data-testid="stButton"] button {
            justify-content: flex-start;
            min-height: 2.8rem;
            padding-inline: 0.9rem;
            border-radius: 12px;
        }
        [data-testid="stSidebar"] [data-testid="stLinkButton"] a {
            min-height: 2.8rem;
            border-radius: 12px;
        }
        [data-testid="stRadio"] [role="radiogroup"] {
            width: fit-content;
            padding: 0.3rem;
            border: 1px solid var(--studio-border);
            border-radius: 14px;
            background: var(--studio-surface);
        }
        [data-testid="stRadio"] label {
            min-height: 2.4rem;
            padding: 0.35rem 0.75rem;
            border-radius: 10px;
        }
        [data-testid="stExpander"] details,
        [data-testid="stAlertContainer"],
        [data-baseweb="base-input"],
        [data-baseweb="select"] > div,
        [data-testid="stTextArea"] textarea {
            border-radius: 14px !important;
        }
        [data-testid="stBaseButton-primary"],
        [data-testid="stBaseButton-secondary"],
        [data-testid="stLinkButton"] a {
            min-height: 2.8rem;
            border-radius: 999px;
            font-weight: 650;
        }
        [data-testid="stBaseButton-primary"] {
            background: var(--studio-accent) !important;
            color: var(--studio-on-accent) !important;
            border-color: transparent !important;
        }
        [data-testid="stBaseButton-primary"]:hover {
            background: var(--studio-accent-hover) !important;
        }
        [data-testid="stBaseButton-primary"]:focus-visible,
        [data-testid="stBaseButton-secondary"]:focus-visible,
        [data-testid="stLinkButton"] a:focus-visible {
            outline: 3px solid var(--studio-focus) !important;
            outline-offset: 3px;
        }
        [data-testid="stTextInput"] input[aria-label="Title"] {
            font-size: clamp(2rem, 5vw, 3.4rem);
            font-weight: 720;
            min-height: 4.7rem;
            letter-spacing: -0.05em;
            padding-left: 0;
        }
        [data-testid="stTextInput"]:has(input[aria-label="Title"]) [data-baseweb="base-input"] {
            background: transparent;
            border-color: transparent;
        }
        [data-testid="stTextInput"]:has(input[aria-label="Title"]) [data-baseweb="base-input"]:focus-within {
            border-color: var(--studio-accent);
        }
        @media (max-width: 720px) {
            [data-testid="stMainBlockContainer"] {
                padding-top: 2rem;
            }
            .workspace-stats {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def current_theme() -> str:
    return "dark" if st.session_state.get(DARK_MODE_KEY, False) else "light"


def apply_app_theme(theme: str) -> None:
    dark = theme == "dark"
    background = "#101114" if dark else "#fbfbfd"
    sidebar = "#191b20" if dark else "#f2f4f7"
    surface = "#202329" if dark else "#ffffff"
    input_background = "#202329" if dark else "#ffffff"
    text = "#f5f5f7" if dark else "#1d1d1f"
    muted = "#b2b6bf" if dark else "#5d6168"
    border = "#343841" if dark else "#d8dbe0"
    accent = "#66aaf5" if dark else "#0057b8"
    accent_hover = "#94c5ff" if dark else "#003f88"
    on_accent = "#071629" if dark else "#ffffff"
    focus = "#7bb8ff" if dark else "#0071e3"

    st.markdown(
        f"""
        <style>
        :root {{ color-scheme: {theme}; }}
        .stApp {{
            --studio-background: {background};
            --studio-sidebar: {sidebar};
            --studio-surface: {surface};
            --studio-text: {text};
            --studio-muted: {muted};
            --studio-border: {border};
            --studio-accent: {accent};
            --studio-accent-hover: {accent_hover};
            --studio-on-accent: {on_accent};
            --studio-focus: {focus};
        }}
        html, body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {{
            background: {background} !important;
            color: {text} !important;
        }}
        [data-testid="stSidebar"],
        [data-testid="stSidebarContent"] {{
            background: {sidebar} !important;
            color: {text} !important;
        }}
        [data-testid="stHeader"] {{
            background: transparent !important;
        }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4,
        .stApp p, .stApp label,
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"] {{
            color: {text} !important;
        }}
        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {{
            color: {muted} !important;
        }}
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-baseweb="select"] > div,
        [data-testid="stNumberInput"] input {{
            background: {input_background} !important;
            color: {text} !important;
            -webkit-text-fill-color: {text} !important;
            border-color: {border} !important;
        }}
        [data-baseweb="select"] [role="combobox"],
        [data-baseweb="select"] [role="combobox"] > div {{
            background: {input_background} !important;
            color: {text} !important;
            -webkit-text-fill-color: {text} !important;
        }}
        [data-baseweb="select"] span,
        [data-baseweb="select"] svg {{
            color: {text} !important;
            fill: {text} !important;
        }}
        [data-testid="stSelectbox"] [role="group"],
        [data-testid="stSelectbox"] input[role="combobox"],
        [data-testid="stSelectbox"] button[aria-label="Open"] {{
            background: {input_background} !important;
            color: {text} !important;
            -webkit-text-fill-color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stSelectbox"] svg {{
            color: {text} !important;
            fill: {text} !important;
        }}
        [data-testid="stExpander"] details,
        [data-testid="stExpander"] summary {{
            background: {background} !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stBaseButton-secondary"] {{
            background: transparent !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stLinkButton"] a {{
            background: transparent !important;
            color: {text} !important;
            border-color: {border} !important;
        }}
        [data-testid="stBaseButton-secondary"]:hover {{
            background: {surface} !important;
        }}
        a {{ color: {accent}; }}
        a:hover {{ color: {accent_hover}; }}
        [data-testid="stDivider"] {{
            border-color: {border} !important;
        }}
        iframe {{
            background: {background} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def render_page_intro(kicker: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="workspace-hero">
          <p class="workspace-kicker">{kicker}</p>
          <h1 class="workspace-title">{title}</h1>
          <p class="workspace-lede">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workspace_stats(draft_count: int, post_count: int) -> None:
    changed_count = 0
    try:
        changed_count = len(changed_publish_bundles())
    except RuntimeError:
        pass
    st.markdown(
        f"""
        <div class="workspace-stats" aria-label="Writing status">
          <div class="workspace-stat"><span class="workspace-stat__value">{draft_count}</span><span class="workspace-stat__label">Drafts</span></div>
          <div class="workspace-stat"><span class="workspace-stat__value">{post_count}</span><span class="workspace-stat__label">Published posts</span></div>
          <div class="workspace-stat"><span class="workspace-stat__value">{changed_count}</span><span class="workspace-stat__label">Ready to sync</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def today_text() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_title).strip("-").lower()
    return slug or "untitled"


def draft_path_for_title(title: str) -> Path:
    return DRAFTS_DIR / f"{slugify(title)}.md"


def post_path_for_title(title: str) -> Path:
    return POSTS_DIR / f"{today_text()}-{slugify(title)}.md"


def post_path_for_date_title(date: str, title: str) -> Path:
    return POSTS_DIR / f"{date.strip()}-{slugify(title)}.md"


def date_from_post_path(path: Path) -> str:
    match = re.match(r"(\d{4}-\d{2}-\d{2})-", path.name)
    if match:
        return match.group(1)
    return today_text()


def parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return parse_csv(value)
    return []


def as_csv(value: Any) -> str:
    return ", ".join(as_list(value))


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_array(values: list[str]) -> str:
    return "[" + ", ".join(yaml_quote(value) for value in values) + "]"


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"').strip("'") for part in inner.split(",")]
    return value


def split_document(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text

    metadata: dict[str, Any] = {}
    for line in parts[1].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = parse_scalar(value)

    return metadata, parts[2].lstrip("\n")


def strip_mathjax(body: str) -> str:
    lines = [line for line in body.splitlines() if line.strip() != MATHJAX_INCLUDE]
    return "\n".join(lines).strip("\n")


def normalize_body(body: str, use_math: bool) -> str:
    clean_body = strip_mathjax(body)
    if use_math:
        if clean_body:
            return f"{MATHJAX_INCLUDE}\n\n{clean_body}\n"
        return f"{MATHJAX_INCLUDE}\n"
    return f"{clean_body}\n" if clean_body else ""


def has_mathjax(body: str) -> bool:
    return MATHJAX_INCLUDE in body


def front_matter(metadata: dict[str, Any]) -> str:
    title = str(metadata.get("title", "")).strip()
    date = str(metadata.get("date", today_text())).strip()
    updated = str(metadata.get("updated", now_text())).strip()
    categories = as_list(metadata.get("categories", []))
    tags = as_list(metadata.get("tags", []))

    return "\n".join(
        [
            "---",
            "layout: post",
            f"title: {yaml_quote(title)}",
            f"date: {date}",
            f"categories: {yaml_array(categories)}",
            f"tags: {yaml_array(tags)}",
            f"updated: {updated}",
            "---",
            "",
        ]
    )


def build_document(metadata: dict[str, Any], body: str, use_math: bool) -> str:
    return front_matter(metadata) + normalize_body(body, use_math)


def read_draft(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    return split_document(text)


def read_post(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    return split_document(text)


def list_drafts() -> list[Path]:
    DRAFTS_DIR.mkdir(exist_ok=True)
    return sorted(DRAFTS_DIR.glob("*.md"), key=lambda path: path.stat().st_mtime, reverse=True)


def list_posts() -> list[Path]:
    POSTS_DIR.mkdir(exist_ok=True)
    return sorted(POSTS_DIR.glob("*.md"), reverse=True)


def run_git(args: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def git_output(args: list[str], timeout: int = 30) -> str:
    result = run_git(args, timeout=timeout)
    output = "\n".join(part for part in (result.stdout.strip(), result.stderr.strip()) if part)
    if result.returncode != 0:
        raise RuntimeError(output or f"git {' '.join(args)} failed")
    return output


def git_status_lines() -> list[str]:
    result = run_git(["status", "--short"])
    output = result.stdout.strip()
    return output.splitlines() if output else []


def status_path(line: str) -> str:
    path = line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip().strip('"')


def changed_post_paths() -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for line in git_status_lines():
        raw_path = status_path(line)
        if not raw_path.startswith("_posts/") or not raw_path.endswith(".md"):
            continue
        path = ROOT / raw_path
        if path not in seen:
            paths.append(path)
            seen.add(path)
    return paths


def changed_relative_paths() -> list[str]:
    return [status_path(line) for line in git_status_lines()]


def changed_publish_bundles() -> list[PublishBundle]:
    changed = changed_relative_paths()
    candidates = {path.resolve(): path for path in list_posts()}
    for raw_path in changed:
        if raw_path.startswith("_posts/") and raw_path.endswith(".md"):
            path = (ROOT / raw_path).resolve()
            candidates.setdefault(path, path)
    return publish_bundles(ROOT, candidates.values(), changed)


def changed_post_labels(paths: list[Path]) -> dict[str, Path]:
    labels: dict[str, Path] = {}
    status_by_path = {status_path(line): line[:2].strip() or "modified" for line in git_status_lines()}
    for path in paths:
        rel = relative(path)
        status = status_by_path.get(rel, "changed")
        labels[f"{status} · {rel}"] = path
    return labels


def current_branch() -> str:
    return git_output(["branch", "--show-current"]) or "HEAD"


def current_remote() -> str:
    result = run_git(["remote"])
    remotes = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return "origin" if "origin" in remotes else (remotes[0] if remotes else "")


def commit_selected_posts(paths: list[Path], message: str) -> str:
    if not paths:
        raise ValueError("Select at least one published post file.")
    if not message.strip():
        raise ValueError("Commit message is required.")

    relative_paths = [relative(path) for path in paths]
    allowed = (
        re.compile(r"^_posts/[^/]+\.md$"),
        re.compile(r"^assets/causal-graphs/cg-\d{8}-[a-z0-9]{8}\.svg$"),
        re.compile(r"^_graph_sources/cg-\d{8}-[a-z0-9]{8}\.json$"),
    )
    invalid = [path for path in relative_paths if not any(pattern.fullmatch(path) for pattern in allowed)]
    if invalid:
        raise ValueError("Unsupported publish path: " + ", ".join(invalid))
    add_result = run_git(["add", "--", *relative_paths])
    if add_result.returncode != 0:
        raise RuntimeError(add_result.stderr.strip() or "git add failed")

    commit_message = message.strip()
    if COMMIT_AUTHOR_LINE not in commit_message:
        commit_message = f"{commit_message}\n\n{COMMIT_AUTHOR_LINE}"

    commit_result = run_git(["commit", "-m", commit_message], timeout=60)
    output = "\n".join(
        part for part in (commit_result.stdout.strip(), commit_result.stderr.strip()) if part
    )
    if commit_result.returncode != 0:
        raise RuntimeError(output or "git commit failed")
    return output


def push_current_branch() -> str:
    branch = current_branch()
    remote = current_remote()
    if not branch or branch == "HEAD":
        raise RuntimeError("Cannot push because the repository is not on a named branch.")
    if not remote:
        raise RuntimeError("Cannot push because no Git remote is configured.")
    return git_output(["push", remote, branch], timeout=120)


def sync_selected_posts(paths: list[Path], message: str) -> str:
    commit_output = commit_selected_posts(paths, message)
    push_output = push_current_branch()
    return "\n\n".join(part for part in (commit_output, push_output) if part)


def draft_label(path: Path) -> str:
    metadata, _ = read_draft(path)
    title = metadata.get("title") or path.stem
    updated = metadata.get("updated", "unknown")
    return f"{title} · {path.name} · {updated}"


def post_label(path: Path) -> str:
    metadata, _ = read_post(path)
    title = metadata.get("title") or path.stem
    updated = metadata.get("updated", "unknown")
    return f"{title} · {path.name} · {updated}"


def post_type_defaults(post_type: str) -> tuple[str, bool]:
    if post_type == "math note":
        return "study, notes", True
    if post_type == "project note":
        return "project, notes", False
    return "study, notes", False


def metadata_from_inputs(title: str, categories: str, tags: str, date: str | None = None) -> dict[str, Any]:
    return {
        "layout": "post",
        "title": title.strip(),
        "date": date or today_text(),
        "categories": parse_csv(categories),
        "tags": parse_csv(tags),
        "updated": now_text(),
    }


def validate_metadata(metadata: dict[str, Any]) -> list[str]:
    missing = []
    for key in ("layout", "title", "date", "categories", "tags", "updated"):
        if key not in metadata:
            missing.append(key)
            continue
        value = metadata.get(key)
        if value in (None, ""):
            missing.append(key)
    return missing


def save_draft(path: Path, metadata: dict[str, Any], body: str, use_math: bool) -> Path:
    DRAFTS_DIR.mkdir(exist_ok=True)
    GRAPH_STORE.load_for_markdown(body, published=False)
    metadata = {**metadata, "updated": now_text()}
    path.write_text(build_document(metadata, body, use_math), encoding="utf-8")
    return path


def save_edited_draft(path: Path, metadata: dict[str, Any], body: str, use_math: bool) -> Path:
    target_path = draft_path_for_title(str(metadata.get("title", "")))
    if target_path != path and target_path.exists():
        raise FileExistsError(f"Draft already exists: {relative(target_path)}")

    saved_path = save_draft(target_path, metadata, body, use_math)
    if target_path != path and path.exists():
        path.unlink()
    return saved_path


def save_edited_post(path: Path, metadata: dict[str, Any], body: str, use_math: bool) -> Path:
    missing = validate_metadata(metadata)
    if missing:
        raise ValueError("Missing required front matter: " + ", ".join(missing))
    GRAPH_STORE.load_for_markdown(body, published=True)

    original_metadata, _ = read_post(path)
    original_title = str(original_metadata.get("title", path.stem)).strip()
    original_date = str(original_metadata.get("date", date_from_post_path(path))).strip()
    new_title = str(metadata.get("title", "")).strip()
    new_date = str(metadata.get("date", "")).strip()

    if new_title != original_title or new_date != original_date:
        target_path = post_path_for_date_title(new_date, new_title)
    else:
        target_path = path

    if target_path != path and target_path.exists():
        raise FileExistsError(f"Post already exists: {relative(target_path)}")

    POSTS_DIR.mkdir(exist_ok=True)
    metadata = {**metadata, "updated": now_text()}
    target_path.write_text(build_document(metadata, body, use_math), encoding="utf-8")
    if target_path != path and path.exists():
        path.unlink()
    return target_path


def publish_draft(path: Path, metadata: dict[str, Any], body: str, use_math: bool) -> Path:
    missing = validate_metadata(metadata)
    if missing:
        raise ValueError("Missing required front matter: " + ", ".join(missing))

    title = str(metadata["title"]).strip()
    post_path = post_path_for_title(title)

    if post_path.exists():
        raise FileExistsError(f"Post already exists: {relative(post_path)}")

    POSTS_DIR.mkdir(exist_ok=True)
    metadata = {**metadata, "date": today_text(), "updated": now_text()}
    post_text = build_document(metadata, body, use_math)
    GRAPH_STORE.promote_draft(path, post_path, post_text, body)
    return post_path


def set_flash(message: str, level: str = "success") -> None:
    st.session_state[FLASH_KEY] = (level, message)


def show_flash() -> None:
    flash = st.session_state.pop(FLASH_KEY, None)
    if not flash:
        return
    level, message = flash
    getattr(st, level)(message)


def request_shutdown(delay: float = 0.8) -> None:
    pid = os.getpid()

    def stop_process() -> None:
        os.kill(pid, signal.SIGTERM)

    timer = threading.Timer(delay, stop_process)
    timer.daemon = True
    timer.start()


def render_sidebar(drafts: list[Path], posts: list[Path]) -> None:
    with st.sidebar:
        st.markdown(
            """
            <div class="studio-brand">
              <p class="studio-brand__eyebrow">Sangyeon Cho</p>
              <p class="studio-brand__title">Writing Studio</p>
              <p class="studio-brand__copy">Local editor for the Jekyll site</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button("View live website ↗", SITE_URL, use_container_width=True)
        st.divider()
        st.caption("APPEARANCE")
        st.toggle("Dark appearance", key=DARK_MODE_KEY)
        st.divider()
        st.caption("WORKSPACE")
        current_view = st.session_state[VIEW_KEY]
        if st.button(
            "Write",
            type="primary" if current_view == "writing" else "secondary",
            use_container_width=True,
        ):
            st.session_state[VIEW_KEY] = "writing"
            st.rerun()
        if st.button(
            "Writing guide",
            type="primary" if current_view == "writing_guide" else "secondary",
            use_container_width=True,
        ):
            st.session_state[VIEW_KEY] = "writing_guide"
            st.rerun()
        if st.button(
            "Publish",
            type="primary" if current_view == "github_sync" else "secondary",
            use_container_width=True,
        ):
            st.session_state[VIEW_KEY] = "github_sync"
            st.rerun()
        st.caption(f"{len(drafts)} drafts · {len(posts)} published posts")
        st.divider()
        with st.expander("Local server"):
            st.caption("Runs only on this Mac.")
            confirm_shutdown = st.checkbox("Confirm shutdown")
            if st.button("Stop server", disabled=not confirm_shutdown, use_container_width=True):
                st.warning("Server is shutting down. You can close this browser tab after it disconnects.")
                request_shutdown()


def selected_draft_path(label_to_path: dict[str, Path], key: str) -> Path | None:
    if not label_to_path:
        return None
    selected = st.selectbox("Draft", options=list(label_to_path), key=key)
    return label_to_path[selected]


def selected_post_path(label_to_path: dict[str, Path], key: str) -> Path | None:
    if not label_to_path:
        return None
    selected = st.selectbox("Post", options=list(label_to_path), key=key)
    return label_to_path[selected]


def markdown_editor(
    initial_value: str,
    key: str,
    *,
    document_id: str,
    graph_enabled: bool,
    published: bool,
) -> str:
    graph_hint = " Causal graphs are available from the same menu." if graph_enabled else ""
    st.caption(
        "Type `/` for blocks. For live display math, type `$$` then Space on an empty line."
        + graph_hint
    )
    try:
        graphs = GRAPH_STORE.load_for_markdown(initial_value, published=published) if graph_enabled else []
    except GraphValidationError as exc:
        st.error(str(exc))
        graphs = []

    response_key = f"{GRAPH_RESPONSE_PREFIX}:{key}"
    request_key = f"{GRAPH_REQUEST_PREFIX}:{key}"
    graph_id_key = f"{GRAPH_ID_PREFIX}:{key}"
    if graph_id_key not in st.session_state:
        st.session_state[graph_id_key] = generate_graph_id()
    event = themed_markdown_editor(
        default_value=initial_value,
        height=640,
        placeholder="Start writing, or type / for blocks…",
        features=EDITOR_FEATURES,
        throttle_delay=300,
        theme=current_theme(),
        document_id=document_id,
        graph_enabled=graph_enabled,
        graphs=graphs,
        new_graph_id=st.session_state[graph_id_key],
        graph_response=st.session_state.get(response_key),
        key=key,
    )
    event_type = event.get("type")
    if event_type == "graph_save" and graph_enabled:
        request_id = str(event.get("request_id", ""))
        if request_id and request_id != st.session_state.get(request_key):
            try:
                graph = GRAPH_STORE.save(event.get("graph", {}), published=published)
            except (GraphValidationError, OSError) as exc:
                response = {"request_id": request_id, "ok": False, "error": str(exc)}
            else:
                response = {
                    "request_id": request_id,
                    "ok": True,
                    "figure": canonical_figure(graph),
                    "graph": graph,
                }
                st.session_state[graph_id_key] = generate_graph_id()
            st.session_state[request_key] = request_id
            st.session_state[response_key] = response
            st.rerun()
        return str(event.get("markdown", initial_value))

    if event_type == "content_change":
        st.session_state.pop(response_key, None)
        return str(event.get("markdown", initial_value))
    return initial_value


def writing_guide_flow() -> None:
    try:
        guide = WRITING_GUIDE_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        st.error(f"Could not open the writing guide: {exc}")
        return

    marker = "<!-- RENDERED_MATH_EXAMPLE -->"
    before_example, separator, after_example = guide.partition(marker)
    st.markdown(before_example)
    if separator:
        st.caption("Rendered display-math example")
        st.latex(
            r"\hat{\tau}="
            r"\frac{1}{n_1}\sum_{i:D_i=1}Y_i"
            r"-\frac{1}{n_0}\sum_{i:D_i=0}Y_i"
        )
        st.markdown(after_example)


def new_draft_flow() -> None:
    version = st.session_state.setdefault(NEW_DRAFT_VERSION_KEY, 0)
    st.caption("NEW DRAFT")
    title = st.text_input(
        "Title",
        key=f"new_title_{version}",
        placeholder="Untitled",
        label_visibility="collapsed",
    )

    with st.expander("Properties", expanded=False):
        post_type = st.selectbox("Post type", POST_TYPE_OPTIONS, key=f"new_post_type_{version}")
        default_categories, default_math = post_type_defaults(post_type)
        left, middle, right = st.columns([1, 1, 0.55])
        with left:
            categories = st.text_input(
                "Categories",
                value=default_categories,
                key=f"new_categories_{version}_{post_type}",
            )
        with middle:
            tags = st.text_input("Tags", key=f"new_tags_{version}")
        with right:
            use_math = st.checkbox("Math", value=default_math, key=f"new_math_{version}_{post_type}")

    body = markdown_editor(
        "",
        key=f"new_body_editor_{version}",
        document_id=f"new-draft-{version}",
        graph_enabled=False,
        published=False,
    )

    draft_path = draft_path_for_title(title)
    st.caption(f"Will save to `{relative(draft_path)}`")

    if not st.button("Create Draft", type="primary"):
        return

    metadata = metadata_from_inputs(title, categories, tags)
    missing = validate_metadata(metadata)
    if missing:
        st.error("Missing required front matter: " + ", ".join(missing))
        return
    if draft_path.exists():
        st.error(f"Draft already exists: `{relative(draft_path)}`")
        return

    save_draft(draft_path, metadata, body, use_math)
    st.session_state[NEW_DRAFT_VERSION_KEY] = version + 1
    set_flash(f"Created `{relative(draft_path)}`")
    st.rerun()


def edit_draft_flow(label_to_path: dict[str, Path]) -> None:
    st.caption("DRAFT")
    path = selected_draft_path(label_to_path, "edit_draft")
    if path is None:
        st.info("Create a draft first.")
        return

    metadata, body = read_draft(path)
    body_without_math = strip_mathjax(body)

    title = st.text_input(
        "Title",
        value=str(metadata.get("title", path.stem)),
        key=f"title_{path.name}",
        label_visibility="collapsed",
    )
    with st.expander("Properties", expanded=True):
        left, middle, right = st.columns([1, 1, 0.55])
        with left:
            categories = st.text_input(
                "Categories",
                value=as_csv(metadata.get("categories", [])),
                key=f"categories_{path.name}",
            )
        with middle:
            tags = st.text_input(
                "Tags",
                value=as_csv(metadata.get("tags", [])),
                key=f"tags_{path.name}",
            )
        with right:
            use_math = st.checkbox("Math", value=has_mathjax(body), key=f"math_{path.name}")

    edited_body = markdown_editor(
        body_without_math,
        key=f"body_editor_{path.name}",
        document_id=relative(path),
        graph_enabled=True,
        published=False,
    )
    updated_metadata = metadata_from_inputs(title, categories, tags, date=str(metadata.get("date", today_text())))
    target_draft = draft_path_for_title(title)
    target_post = post_path_for_title(title)

    with st.expander("File details"):
        st.caption(f"Current draft: `{relative(path)}`")
        st.caption(f"Save target: `{relative(target_draft)}`")
        st.caption(f"Publish target: `{relative(target_post)}`")

    save_col, publish_col, delete_col = st.columns([1, 1, 1])
    with save_col:
        if st.button("Save Draft", type="primary", key=f"save_{path.name}"):
            try:
                saved_path = save_edited_draft(path, updated_metadata, edited_body, use_math)
            except (FileExistsError, GraphValidationError, OSError) as exc:
                st.error(str(exc))
            else:
                set_flash(f"Saved `{relative(saved_path)}`")
                st.rerun()

    with publish_col:
        if st.button("Publish", key=f"publish_{path.name}"):
            try:
                post_path = publish_draft(path, updated_metadata, edited_body, use_math)
            except (FileExistsError, GraphValidationError, OSError, ValueError) as exc:
                st.error(str(exc))
            else:
                set_flash(f"Published `{relative(post_path)}`")
                st.rerun()

    with delete_col:
        delete_graphs, shared_graphs = GRAPH_STORE.draft_graph_delete_summary(path, edited_body)
        if delete_graphs:
            st.caption(f"Also deletes {delete_graphs} private draft graph(s).")
        if shared_graphs:
            st.caption(f"Keeps {shared_graphs} graph(s) shared by other drafts.")
        confirm_delete = st.checkbox("Confirm delete", key=f"confirm_delete_{path.name}")
        if st.button("Delete Draft", disabled=not confirm_delete, key=f"delete_{path.name}"):
            try:
                removed_graphs, _ = GRAPH_STORE.delete_draft(path, edited_body)
            except OSError as exc:
                st.error(str(exc))
            else:
                suffix = f" and {removed_graphs} private graph(s)" if removed_graphs else ""
                set_flash(f"Deleted `{relative(path)}`{suffix}", "warning")
                st.rerun()


def edit_post_flow(label_to_path: dict[str, Path]) -> None:
    st.caption("PUBLISHED POST")
    path = selected_post_path(label_to_path, "edit_post")
    if path is None:
        st.info("No published posts yet.")
        return

    metadata, body = read_post(path)
    body_without_math = strip_mathjax(body)
    current_date = str(metadata.get("date", date_from_post_path(path)))

    title = st.text_input(
        "Title",
        value=str(metadata.get("title", path.stem)),
        key=f"post_title_{path.name}",
        label_visibility="collapsed",
    )
    with st.expander("Properties", expanded=True):
        date_col, categories_col, tags_col, math_col = st.columns([0.75, 1, 1, 0.5])
        with date_col:
            date = st.text_input("Date", value=current_date, key=f"post_date_{path.name}")
        with categories_col:
            categories = st.text_input(
                "Categories",
                value=as_csv(metadata.get("categories", [])),
                key=f"post_categories_{path.name}",
            )
        with tags_col:
            tags = st.text_input(
                "Tags",
                value=as_csv(metadata.get("tags", [])),
                key=f"post_tags_{path.name}",
            )
        with math_col:
            use_math = st.checkbox("Math", value=has_mathjax(body), key=f"post_math_{path.name}")

    edited_body = markdown_editor(
        body_without_math,
        key=f"post_body_editor_{path.name}",
        document_id=relative(path),
        graph_enabled=True,
        published=True,
    )
    updated_metadata = metadata_from_inputs(title, categories, tags, date=date)
    original_title = str(metadata.get("title", path.stem)).strip()
    original_date = str(metadata.get("date", date_from_post_path(path))).strip()
    target_post = path
    if title.strip() != original_title or date.strip() != original_date:
        target_post = post_path_for_date_title(date, title)

    with st.expander("File details"):
        st.caption(f"Current post: `{relative(path)}`")
        st.caption(f"Save target: `{relative(target_post)}`")

    save_col, duplicate_col = st.columns([1, 2])
    with save_col:
        if st.button("Save Published Post", type="primary", key=f"save_post_{path.name}"):
            try:
                saved_path = save_edited_post(path, updated_metadata, edited_body, use_math)
            except (FileExistsError, GraphValidationError, OSError, ValueError) as exc:
                st.error(str(exc))
            else:
                set_flash(f"Saved published post `{relative(saved_path)}`")
                st.rerun()
    with duplicate_col:
        if target_post != path and target_post.exists():
            st.error(f"Target already exists: `{relative(target_post)}`")
        elif target_post != path:
            st.info("Saving will rename this post file.")
        else:
            st.success("Saving will update this post in place.")


def github_sync_flow() -> None:
    try:
        branch = current_branch()
        remote = current_remote()
        status_lines = git_status_lines()
        bundles = changed_publish_bundles()
    except RuntimeError as exc:
        st.error(str(exc))
        return

    st.caption(f"BRANCH `{branch}` · REMOTE `{remote or 'none'}`")
    if status_lines:
        with st.expander("Git status"):
            st.code("\n".join(status_lines), language="text")
    else:
        st.success("No local Git changes.")

    status_by_path = {status_path(line): line[:2].strip() or "modified" for line in status_lines}
    bundle_by_label: dict[str, PublishBundle] = {}
    for bundle in bundles:
        post_status = status_by_path.get(relative(bundle.post), "graph changed")
        graph_note = f" · {len(bundle.graph_ids)} graph(s)" if bundle.graph_ids else ""
        bundle_by_label[f"{post_status} · {relative(bundle.post)}{graph_note}"] = bundle
    st.markdown("### 1. Choose published posts")
    selected_labels = st.multiselect(
        "Changed publish bundles",
        options=list(bundle_by_label),
        default=[],
    )
    selected_paths: list[Path] = []
    seen_paths: set[Path] = set()
    for label in selected_labels:
        for path in bundle_by_label[label].paths:
            if path not in seen_paths:
                selected_paths.append(path)
                seen_paths.add(path)
    if selected_paths:
        st.caption("Will stage only: " + ", ".join(f"`{relative(path)}`" for path in selected_paths))
    st.markdown("### 2. Describe the update")
    commit_message = st.text_area(
        "Commit message",
        value="Update blog posts",
        height=90,
    )

    st.markdown("### 3. Review and publish")
    confirm_sync = st.checkbox("I reviewed the selected post, graph assets, and commit message")

    sync_disabled = not selected_paths or not confirm_sync
    if st.button(
        "Commit and publish to website",
        type="primary",
        disabled=sync_disabled,
        use_container_width=True,
    ):
        try:
            sync_output = sync_selected_posts(selected_paths, commit_message)
            set_flash(f"Synced selected posts to GitHub.\n\n{sync_output}")
            st.rerun()
        except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
            st.error(str(exc))

    with st.expander("Advanced"):
        confirm_commit = st.checkbox("Confirm commit only")
        commit_disabled = not selected_paths or not confirm_commit
        if st.button("Commit Only", disabled=commit_disabled, use_container_width=True):
            try:
                commit_output = commit_selected_posts(selected_paths, commit_message)
                set_flash(f"Committed selected posts.\n\n{commit_output}")
                st.rerun()
            except (RuntimeError, ValueError, subprocess.TimeoutExpired) as exc:
                st.error(str(exc))

        confirm_push = st.checkbox("Confirm push current branch")
        if st.button("Push Current Branch", disabled=not confirm_push, use_container_width=True):
            try:
                push_output = push_current_branch()
            except (RuntimeError, subprocess.TimeoutExpired) as exc:
                st.error(str(exc))
            else:
                set_flash(f"Pushed `{branch}` to `{remote}`.\n\n{push_output}")
                st.rerun()


def main() -> None:
    st.set_page_config(page_title="Sangyeon Cho · Writing Studio", layout="wide")
    st.session_state.setdefault(VIEW_KEY, "writing")
    st.session_state.setdefault(DARK_MODE_KEY, st.context.theme.type == "dark")
    hide_streamlit_chrome()
    apply_app_theme(current_theme())

    drafts = list_drafts()
    posts = list_posts()
    draft_label_to_path = {draft_label(path): path for path in drafts}
    post_label_to_path = {post_label(path): path for path in posts}
    render_sidebar(drafts, posts)
    show_flash()

    if st.session_state[VIEW_KEY] == "writing_guide":
        render_page_intro(
            "Reference",
            "Writing guide",
            "Markdown, math, and editor shortcuts in one quiet reference page.",
        )
        writing_guide_flow()
        return

    if st.session_state[VIEW_KEY] == "github_sync":
        render_page_intro(
            "Publish",
            "Publish to the website",
            "Select finished posts, create one focused commit, and push the current branch.",
        )
        github_sync_flow()
        return

    render_page_intro(
        "Writing studio",
        "Write clearly. Publish calmly.",
        "Draft and edit in a rendered document. Every saved post remains plain Markdown for Jekyll.",
    )
    render_workspace_stats(len(drafts), len(posts))
    st.session_state.setdefault(WRITING_MODE_KEY, "Drafts" if drafts else "New draft")
    writing_mode = st.radio(
        "Document type",
        ("New draft", "Drafts", "Published"),
        horizontal=True,
        key=WRITING_MODE_KEY,
        label_visibility="collapsed",
    )
    st.divider()

    if writing_mode == "New draft":
        new_draft_flow()
    elif writing_mode == "Drafts":
        edit_draft_flow(draft_label_to_path)
    else:
        edit_post_flow(post_label_to_path)


if __name__ == "__main__":
    main()
