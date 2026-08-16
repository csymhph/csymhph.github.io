import { describe, expect, it } from "vitest";
import {
  GraphModel,
  canonicalFigure,
  escapeXml,
  graphIdFromFigure,
  graphToSvg,
  historyReducer,
  insertFigureAtMarkdownOffset,
  validateGraph,
} from "./causalGraph";

const graph = (): GraphModel => ({
  id: "cg-20260801-ab12cd34",
  schema_version: 1,
  alt: '처치 "X"와 결과 Y',
  caption: "A < B & C",
  nodes: [
    { id: "x", label: "처치 X", x: 40, y: 40, role: "exposure", observed: true },
    { id: "y", label: "Outcome & Y", x: 40, y: 180, role: "outcome", observed: true },
    { id: "u", label: "U <latent>", x: 180, y: 40, role: "standard", observed: false },
  ],
  edges: [
    { id: "e1", source: "x", target: "y", kind: "directed", label: "β < 1" },
    { id: "e2", source: "u", target: "y", kind: "bidirected", label: "" },
  ],
});

describe("causal graph validation", () => {
  it("accepts Unicode, roles, and bidirected edges", () => {
    expect(validateGraph(graph())).toEqual({ valid: true, errors: [] });
  });

  it("blocks cycles, duplicate edges, duplicate labels, and latent roles", () => {
    const invalid = graph();
    invalid.nodes[1].label = "처치 x";
    invalid.nodes[2].role = "adjusted";
    invalid.edges.push(
      { id: "e3", source: "x", target: "y", kind: "directed", label: "" },
      { id: "e4", source: "y", target: "x", kind: "directed", label: "" },
    );
    const errors = validateGraph(invalid).errors.join(" ");
    expect(errors).toContain("Duplicate node label");
    expect(errors).toContain("Latent node");
    expect(errors).toContain("Duplicate directed edge");
    expect(errors).toContain("acyclic");
  });
});

describe("serialization", () => {
  it("escapes XML and round-trips the canonical figure ID", () => {
    expect(escapeXml('<&"', true)).toBe("&lt;&amp;&quot;");
    const figure = canonicalFigure(graph());
    expect(figure).toContain('alt="처치 &quot;X&quot;와 결과 Y"');
    expect(figure).toContain("A &lt; B &amp; C");
    expect(graphIdFromFigure(figure)).toBe(graph().id);
  });

  it("inserts at a bookmarked position and replaces an existing figure", () => {
    const figure = canonicalFigure(graph());
    const inserted = insertFigureAtMarkdownOffset("First.\n\nSecond.", figure, 8);
    expect(inserted.indexOf("First.")).toBeLessThan(inserted.indexOf("<figure"));
    expect(inserted.indexOf("<figure")).toBeLessThan(inserted.indexOf("Second."));
    const updatedGraph = { ...graph(), caption: "Updated" };
    const replaced = insertFigureAtMarkdownOffset(inserted, canonicalFigure(updatedGraph), 0, graph().id);
    expect(replaced).toContain("Updated");
    expect(replaced.match(/<figure/g)).toHaveLength(1);
  });

  it("creates deterministic SVG with a white background and escaped text", () => {
    const first = graphToSvg(graph());
    expect(graphToSvg(graph())).toBe(first);
    expect(first).toMatchSnapshot();
    expect(first).toContain('fill="#ffffff"');
    expect(first).toContain("β &lt; 1");
    expect(first).toContain('marker-start="url(#arrow)"');
  });
});

describe("history reducer", () => {
  it("supports undo, redo, and clears redo after a new commit", () => {
    const initial = graph();
    const changed = { ...initial, caption: "Changed" };
    let state = { past: [] as GraphModel[], present: initial, future: [] as GraphModel[] };
    state = historyReducer(state, { type: "commit", graph: changed });
    state = historyReducer(state, { type: "undo" });
    expect(state.present.caption).toBe(initial.caption);
    state = historyReducer(state, { type: "redo" });
    expect(state.present.caption).toBe("Changed");
    state = historyReducer(state, { type: "undo" });
    state = historyReducer(state, { type: "commit", graph: { ...initial, alt: "New" } });
    expect(state.future).toHaveLength(0);
  });
});
