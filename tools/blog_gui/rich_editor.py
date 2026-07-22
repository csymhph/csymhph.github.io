from __future__ import annotations

import hashlib
import importlib.util
import shutil
from pathlib import Path
from typing import Any

import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / ".streamlit" / "blog_gui_components" / "streamlit_crepe_themed"
PATCH_VERSION = "theme-v3"

THEME_CSS = r"""
.crepe-container {
  color-scheme: light;
}

.crepe-container[data-theme="dark"] {
  color-scheme: dark;
  background: #101114 !important;
}

.crepe-container[data-theme="dark"] .milkdown {
  --crepe-color-background: #101114;
  --crepe-color-on-background: #f5f5f7;
  --crepe-color-surface: #202329;
  --crepe-color-surface-low: #191b20;
  --crepe-color-on-surface: #f5f5f7;
  --crepe-color-on-surface-variant: #b2b6bf;
  --crepe-color-outline: #5b616c;
  --crepe-color-primary: #66aaf5;
  --crepe-color-secondary: #343841;
  --crepe-color-on-secondary: #f5f5f7;
  --crepe-color-inverse: #e8eaed;
  --crepe-color-on-inverse: #16181d;
  --crepe-color-inline-code: #94c5ff;
  --crepe-color-error: #ff6b6b;
  --crepe-color-hover: #292d34;
  --crepe-color-selected: #343e4b;
  --crepe-color-inline-area: #292d34;
}

.crepe-container[data-theme="dark"] .milkdown-code-block,
.crepe-container[data-theme="dark"] .cm-editor,
.crepe-container[data-theme="dark"] .cm-scroller,
.crepe-container[data-theme="dark"] .cm-gutters,
.crepe-container[data-theme="dark"] .cm-activeLine,
.crepe-container[data-theme="dark"] .cm-activeLineGutter {
  background: var(--crepe-color-surface) !important;
  color: var(--crepe-color-on-surface) !important;
}

.crepe-container[data-theme="dark"] .cm-gutterElement,
.crepe-container[data-theme="dark"] .cm-line,
.crepe-container[data-theme="dark"] .cm-content,
.crepe-container[data-theme="dark"] .cm-cursor {
  color: var(--crepe-color-on-surface) !important;
  border-color: var(--crepe-color-on-surface) !important;
}

.crepe-container[data-theme="dark"] .cm-selectionBackground,
.crepe-container[data-theme="dark"] .cm-content ::selection {
  background: var(--crepe-color-selected) !important;
}

.crepe-container[data-theme="light"] .milkdown-code-block,
.crepe-container[data-theme="light"] .cm-editor,
.crepe-container[data-theme="light"] .cm-scroller,
.crepe-container[data-theme="light"] .cm-gutters,
.crepe-container[data-theme="light"] .cm-activeLine,
.crepe-container[data-theme="light"] .cm-activeLineGutter {
  background: #f7f7f7 !important;
  color: #1c1c1c !important;
}

.crepe-container[data-theme="light"] .cm-gutterElement,
.crepe-container[data-theme="light"] .cm-line,
.crepe-container[data-theme="light"] .cm-content,
.crepe-container[data-theme="light"] .cm-cursor {
  color: #1c1c1c !important;
  border-color: #1c1c1c !important;
}

.crepe-container[data-theme="light"] .cm-selectionBackground,
.crepe-container[data-theme="light"] .cm-content ::selection {
  background: #d5d5d5 !important;
}
"""


def _source_build_dir() -> Path:
    spec = importlib.util.find_spec("streamlit_crepe")
    if spec is None or not spec.submodule_search_locations:
        raise RuntimeError("streamlit-crepe is not installed. Recreate the project Conda environment.")
    return Path(next(iter(spec.submodule_search_locations))) / "frontend" / "build"


def _patched_bundle(source: str) -> str:
    css_marker = "/*$vite$:1*/"
    component_before = (
        'className:"crepe-container","data-auto-height":s?"true":"false",'
        'style:{height:s?"auto":t.height,minHeight:s?a:void 0,'
        'backgroundColor:"#ffffff",'
    )
    component_after = (
        'className:"crepe-container","data-auto-height":s?"true":"false",'
        '"data-theme":t.theme==="dark"?"dark":"light",'
        'style:{height:s?"auto":t.height,minHeight:s?a:void 0,'
        'backgroundColor:t.theme==="dark"?"#101114":"#ffffff",'
    )

    if source.count(css_marker) != 1:
        raise RuntimeError("Could not locate the Crepe CSS insertion point.")
    if source.count(component_before) != 1:
        raise RuntimeError("Could not locate the Crepe container theme hook.")

    source = source.replace(css_marker, THEME_CSS + css_marker, 1)
    return source.replace(component_before, component_after, 1)


def _ensure_themed_build() -> Path:
    source_dir = _source_build_dir()
    bundle_name = "streamlit-crepe.umd.js"
    source_bundle = source_dir / bundle_name
    source_hash = hashlib.sha256(source_bundle.read_bytes()).hexdigest()
    signature = f"{PATCH_VERSION}:{source_hash}"
    marker = CACHE_DIR / ".theme-patch"

    if marker.exists() and marker.read_text(encoding="utf-8") == signature:
        return CACHE_DIR

    if CACHE_DIR.exists():
        shutil.rmtree(CACHE_DIR)
    shutil.copytree(source_dir, CACHE_DIR)

    target_bundle = CACHE_DIR / bundle_name
    patched = _patched_bundle(target_bundle.read_text(encoding="utf-8"))
    target_bundle.write_text(patched, encoding="utf-8")
    marker.write_text(signature, encoding="utf-8")
    return CACHE_DIR


_component_func = components.declare_component(
    "themed_crepe_editor",
    path=str(_ensure_themed_build()),
)


def themed_markdown_editor(
    default_value: str = "",
    *,
    height: int = 640,
    placeholder: str = "",
    features: dict[str, bool] | None = None,
    throttle_delay: int = 300,
    theme: str = "light",
    key: str | None = None,
) -> str:
    component_value: Any = _component_func(
        default_value=default_value,
        height=height,
        min_height=400,
        placeholder=placeholder,
        readonly=False,
        features=features or {},
        throttle_delay=throttle_delay,
        theme="dark" if theme == "dark" else "light",
        key=key,
    )
    return component_value or default_value
