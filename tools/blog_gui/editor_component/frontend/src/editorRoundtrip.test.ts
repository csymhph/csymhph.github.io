import { afterEach, describe, expect, it } from "vitest";
import { Crepe } from "@milkdown/crepe";
import { editorViewCtx } from "@milkdown/kit/core";
import { GraphModel, canonicalFigure } from "./causalGraph";

class ResizeObserverStub {
  observe(): void {}
  unobserve(): void {}
  disconnect(): void {}
}

Object.defineProperty(globalThis, "ResizeObserver", { value: ResizeObserverStub, configurable: true });

const graph: GraphModel = {
  id: "cg-20260801-ab12cd34",
  schema_version: 1,
  alt: "X causes Y",
  caption: "Example graph",
  nodes: [{ id: "x", label: "X", x: 20, y: 20, role: "exposure", observed: true }],
  edges: [],
};

const editors: Crepe[] = [];
afterEach(() => {
  for (const editor of editors.splice(0)) editor.destroy();
  document.body.replaceChildren();
});

describe("Milkdown figure round trip", () => {
  it("preserves the canonical causal figure between paragraphs", async () => {
    const root = document.createElement("div");
    document.body.append(root);
    const figure = canonicalFigure(graph);
    const markdown = `First paragraph.\n\n${figure}\n\nSecond paragraph.`;
    const editor = new Crepe({
      root,
      defaultValue: markdown,
      features: {
        [Crepe.Feature.CodeMirror]: false,
        [Crepe.Feature.Latex]: false,
        [Crepe.Feature.Table]: false,
        [Crepe.Feature.ImageBlock]: false,
      },
    });
    editors.push(editor);
    await editor.create();
    const serialized = editor.getMarkdown();
    expect(serialized.trimEnd()).toBe(markdown);
    expect(serialized).toContain(figure);
  });

  it("serializes an inserted figure without changing surrounding paragraphs", async () => {
    const root = document.createElement("div");
    document.body.append(root);
    const figure = canonicalFigure(graph);
    const editor = new Crepe({ root, defaultValue: "First paragraph.\n\nSecond paragraph." });
    editors.push(editor);
    await editor.create();
    editor.editor.action((ctx) => {
      const view = ctx.get(editorViewCtx);
      const htmlNode = view.state.schema.nodes.html.create({ value: figure });
      const paragraph = view.state.schema.nodes.paragraph.create();
      const blockPosition = view.state.doc.child(0).nodeSize;
      const withEmptyParagraph = view.state.tr.insert(blockPosition, paragraph);
      view.dispatch(withEmptyParagraph.insert(blockPosition + 1, htmlNode));
    });
    const serialized = editor.getMarkdown();
    expect(serialized.trimEnd()).toBe(`First paragraph.\n\n${figure}\n\nSecond paragraph.`);
  });
});
