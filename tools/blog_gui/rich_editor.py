from __future__ import annotations

from pathlib import Path
from typing import Any

import streamlit.components.v1 as components


BUILD_DIR = Path(__file__).with_name("editor_component") / "build"
if not (BUILD_DIR / "index.html").exists():
    raise RuntimeError(
        "The Writing Studio editor build is missing. Run `npm run build` in "
        "tools/blog_gui/editor_component/frontend."
    )


_component_func = components.declare_component("writing_studio_editor", path=str(BUILD_DIR))


def themed_markdown_editor(
    default_value: str = "",
    *,
    height: int = 640,
    placeholder: str = "",
    features: dict[str, bool] | None = None,
    throttle_delay: int = 300,
    theme: str = "light",
    document_id: str = "",
    graph_enabled: bool = False,
    graphs: list[dict[str, Any]] | None = None,
    new_graph_id: str = "",
    graph_response: dict[str, Any] | None = None,
    key: str | None = None,
) -> dict[str, Any]:
    component_value: Any = _component_func(
        default_value=default_value,
        height=height,
        min_height=400,
        placeholder=placeholder,
        readonly=False,
        features=features or {},
        throttle_delay=throttle_delay,
        theme="dark" if theme == "dark" else "light",
        document_id=document_id,
        graph_enabled=graph_enabled,
        graphs=graphs or [],
        new_graph_id=new_graph_id,
        graph_response=graph_response,
        key=key,
        default={"type": "content_change", "markdown": default_value},
    )
    if isinstance(component_value, str):
        return {"type": "content_change", "markdown": component_value}
    if isinstance(component_value, dict):
        return component_value
    return {"type": "content_change", "markdown": default_value}
