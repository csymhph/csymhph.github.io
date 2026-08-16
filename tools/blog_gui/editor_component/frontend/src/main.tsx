import React, { ReactElement, useCallback, useEffect, useReducer, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import { ComponentProps, Streamlit, withStreamlitConnection } from "streamlit-component-lib";
import debounce from "lodash.debounce";
import cytoscape, { Core, EdgeSingular, NodeSingular } from "cytoscape";
import edgehandles from "cytoscape-edgehandles";
import { Crepe } from "@milkdown/crepe";
import { commandsCtx, editorViewCtx } from "@milkdown/kit/core";
import { clearTextInCurrentBlockCommand } from "@milkdown/kit/preset/commonmark";
import "@milkdown/crepe/theme/common/style.css";
import "@milkdown/crepe/theme/frame.css";
import {
  EdgeKind,
  GraphEdge,
  GraphModel,
  GraphNode,
  HistoryState,
  canonicalFigure,
  graphIdFromFigure,
  historyReducer,
  validateGraph,
} from "./causalGraph";
import "./style.css";

cytoscape.use(edgehandles);

interface GraphResponse {
  request_id: string;
  ok: boolean;
  figure?: string;
  graph?: GraphModel;
  error?: string;
}

interface EditorArgs {
  default_value?: string;
  height?: number;
  min_height?: number;
  placeholder?: string;
  throttle_delay?: number;
  readonly?: boolean;
  theme?: "light" | "dark";
  features?: Record<string, boolean>;
  document_id?: string;
  graph_enabled?: boolean;
  graphs?: GraphModel[];
  new_graph_id?: string;
  graph_response?: GraphResponse | null;
}

interface Bookmark {
  from: number;
  to: number;
  graphId?: string;
}

function emptyGraph(id: string): GraphModel {
  return { id, schema_version: 1, alt: "", caption: "", nodes: [], edges: [] };
}

function cloneGraph(graph: GraphModel): GraphModel {
  return structuredClone(graph);
}

function nodeStyle(role: string, observed: boolean): Record<string, string | number> {
  const styles: Record<string, Record<string, string | number>> = {
    standard: { shape: "ellipse", "background-color": "#ffffff", "border-color": "#374151", "border-width": 2 },
    exposure: { shape: "round-rectangle", "background-color": "#e8f2ff", "border-color": "#0057b8", "border-width": 3 },
    outcome: { shape: "diamond", "background-color": "#fff2df", "border-color": "#a34b00", "border-width": 3 },
    adjusted: { shape: "hexagon", "background-color": "#f0eaff", "border-color": "#6542a6", "border-width": 3 },
  };
  return { ...styles[role], "border-style": observed ? "solid" : "dashed" };
}

function graphFromCy(cy: Core, base: GraphModel): GraphModel {
  const nodes: GraphNode[] = cy.nodes().filter((node) => !node.hasClass("eh-ghost-node")).map((element) => {
    const node = element as NodeSingular;
    return {
      id: node.id(),
      label: String(node.data("label") ?? ""),
      x: Math.round(node.position("x") * 100) / 100,
      y: Math.round(node.position("y") * 100) / 100,
      role: (node.data("role") ?? "standard") as GraphNode["role"],
      observed: node.data("observed") !== false,
    };
  });
  const edges: GraphEdge[] = cy.edges().filter((edge) => !edge.hasClass("eh-ghost-edge") && !edge.hasClass("eh-preview")).map((element) => {
    const edge = element as EdgeSingular;
    return {
      id: edge.id(),
      source: edge.source().id(),
      target: edge.target().id(),
      kind: (edge.data("kind") ?? "directed") as EdgeKind,
      label: String(edge.data("label") ?? ""),
    };
  });
  return { ...base, nodes, edges };
}

interface GraphDialogProps {
  initial: GraphModel;
  theme: "light" | "dark";
  pending: boolean;
  serverError: string;
  onCancel: () => void;
  onSave: (graph: GraphModel) => void;
}

function GraphDialog({ initial, theme, pending, serverError, onCancel, onSave }: GraphDialogProps): ReactElement {
  const [history, dispatch] = useReducer(historyReducer, { past: [], present: cloneGraph(initial), future: [] } as HistoryState);
  const graph = history.present;
  const graphRef = useRef(graph);
  const canvasRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<Core | null>(null);
  const edgeHandlesRef = useRef<any>(null);
  const edgeKindRef = useRef<EdgeKind>("directed");
  const [edgeMode, setEdgeMode] = useState<EdgeKind | null>(null);
  const [selected, setSelected] = useState<{ type: "node" | "edge"; id: string } | null>(null);
  const [errors, setErrors] = useState<string[]>([]);
  const [dirty, setDirty] = useState(false);

  useEffect(() => {
    graphRef.current = graph;
    const cy = cyRef.current;
    if (!cy) return;
    for (const node of graph.nodes) {
      const element = cy.getElementById(node.id);
      if (element.nonempty()) element.data({ label: node.label, role: node.role, observed: node.observed });
    }
    for (const edge of graph.edges) {
      const element = cy.getElementById(edge.id);
      if (element.nonempty()) element.data({ label: edge.label, kind: edge.kind });
    }
  }, [graph]);

  const commit = useCallback((next: GraphModel) => {
    graphRef.current = next;
    dispatch({ type: "commit", graph: next });
    setDirty(true);
    setErrors([]);
  }, []);

  useEffect(() => {
    if (!canvasRef.current) return;
    const cy = cytoscape({
      container: canvasRef.current,
      elements: [
        ...initial.nodes.map((node) => ({ data: { id: node.id, label: node.label, role: node.role, observed: node.observed }, position: { x: node.x, y: node.y } })),
        ...initial.edges.map((edge) => ({ data: { id: edge.id, source: edge.source, target: edge.target, kind: edge.kind, label: edge.label } })),
      ],
      layout: { name: "preset" },
      minZoom: 0.25,
      maxZoom: 3,
      wheelSensitivity: 0.18,
      style: [
        { selector: "node", style: { label: "data(label)", color: "#111827", "font-size": 14, "font-weight": 600, width: "label", height: 48, padding: 18, "text-wrap": "wrap", "text-max-width": 130, ...nodeStyle("standard", true) } },
        { selector: 'node[role = "exposure"]', style: nodeStyle("exposure", true) },
        { selector: 'node[role = "outcome"]', style: nodeStyle("outcome", true) },
        { selector: 'node[role = "adjusted"]', style: nodeStyle("adjusted", true) },
        { selector: 'node[observed = false]', style: { "border-style": "dashed" } },
        { selector: "edge", style: { width: 2, "line-color": "#374151", "target-arrow-color": "#374151", "target-arrow-shape": "triangle", "curve-style": "bezier", label: "data(label)", color: "#111827", "font-size": 12, "text-background-color": "#ffffff", "text-background-opacity": 1, "text-background-padding": 3 } },
        { selector: 'edge[kind = "bidirected"]', style: { "source-arrow-color": "#374151", "source-arrow-shape": "triangle" } },
        { selector: ":selected", style: { "overlay-color": "#0071e3", "overlay-opacity": 0.12, "overlay-padding": 8 } },
        { selector: ".eh-preview, .eh-ghost-edge", style: { "line-color": "#0071e3", "target-arrow-color": "#0071e3" } },
      ],
    });
    cyRef.current = cy;
    cy.on("tap", "node", (event) => setSelected({ type: "node", id: event.target.id() }));
    cy.on("tap", "edge", (event) => setSelected({ type: "edge", id: event.target.id() }));
    cy.on("tap", (event) => { if (event.target === cy) setSelected(null); });
    cy.on("dragfree", "node", () => commit(graphFromCy(cy, graphRef.current)));
    cy.on("ehcomplete", (_event, _source: NodeSingular, _target: NodeSingular, addedEdge: EdgeSingular) => {
      addedEdge.data({ kind: edgeKindRef.current, label: "" });
      commit(graphFromCy(cy, graphRef.current));
    });
    const handles = (cy as any).edgehandles({
      canConnect: (source: NodeSingular, target: NodeSingular) => !source.same(target),
      edgeParams: (source: NodeSingular, target: NodeSingular) => ({
        data: { id: `e-${crypto.randomUUID().slice(0, 8)}`, source: source.id(), target: target.id(), kind: edgeKindRef.current, label: "" },
      }),
      snap: true,
      noEdgeEventsInDraw: true,
      disableBrowserGestures: true,
    });
    handles.disable();
    edgeHandlesRef.current = handles;
    if (initial.nodes.length) cy.fit(undefined, 48);
    return () => {
      handles.destroy();
      cy.destroy();
      cyRef.current = null;
    };
  }, [initial.id, commit]);

  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => {
      if (!dirty) return;
      event.preventDefault();
      event.returnValue = "";
    };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);

  const selectEdgeMode = (kind: EdgeKind) => {
    edgeKindRef.current = kind;
    setEdgeMode(kind);
    edgeHandlesRef.current?.enable();
    edgeHandlesRef.current?.enableDrawMode();
  };

  const stopEdgeMode = () => {
    setEdgeMode(null);
    edgeHandlesRef.current?.disableDrawMode();
    edgeHandlesRef.current?.disable();
  };

  const addNode = () => {
    const cy = cyRef.current;
    if (!cy || graph.nodes.length >= 50) return;
    stopEdgeMode();
    const id = `n-${crypto.randomUUID().slice(0, 8)}`;
    const position = cy.extent();
    cy.add({ data: { id, label: `Node ${graph.nodes.length + 1}`, role: "standard", observed: true }, position: { x: (position.x1 + position.x2) / 2, y: (position.y1 + position.y2) / 2 } });
    commit(graphFromCy(cy, graphRef.current));
    setSelected({ type: "node", id });
  };

  const deleteSelected = () => {
    const cy = cyRef.current;
    if (!cy || !selected) return;
    cy.getElementById(selected.id).remove();
    commit(graphFromCy(cy, graphRef.current));
    setSelected(null);
  };

  const arrange = () => {
    const cy = cyRef.current;
    if (!cy) return;
    stopEdgeMode();
    const layout = cy.layout({ name: "breadthfirst", directed: true, spacingFactor: 1.25, padding: 48 });
    layout.one("layoutstop", () => commit(graphFromCy(cy, graphRef.current)));
    layout.run();
  };

  const updateNode = (id: string, patch: Partial<GraphNode>) => {
    const cy = cyRef.current;
    if (!cy) return;
    const current = graphRef.current.nodes.find((node) => node.id === id);
    if (!current) return;
    const next = { ...current, ...patch };
    if (!next.observed) next.role = "standard";
    cy.getElementById(id).data({ label: next.label, role: next.role, observed: next.observed });
    commit(graphFromCy(cy, graphRef.current));
  };

  const updateEdge = (id: string, patch: Partial<GraphEdge>) => {
    const cy = cyRef.current;
    if (!cy) return;
    cy.getElementById(id).data(patch);
    commit(graphFromCy(cy, graphRef.current));
  };

  const undo = () => {
    if (!history.past.length) return;
    const previous = history.past.at(-1)!;
    graphRef.current = previous;
    dispatch({ type: "undo" });
    rebuildCy(cyRef.current, previous);
  };
  const redo = () => {
    if (!history.future.length) return;
    const next = history.future[0];
    graphRef.current = next;
    dispatch({ type: "redo" });
    rebuildCy(cyRef.current, next);
  };

  const close = () => {
    if (!dirty || window.confirm("Discard unsaved graph changes?")) onCancel();
  };

  const save = () => {
    const cy = cyRef.current;
    const latest = cy ? graphFromCy(cy, graphRef.current) : graphRef.current;
    const result = validateGraph(latest);
    if (!result.valid) {
      setErrors(result.errors);
      return;
    }
    onSave(latest);
  };

  const handleDialogKeyDown = (event: React.KeyboardEvent) => {
    const target = event.target as HTMLElement;
    const editingField = /^(INPUT|TEXTAREA|SELECT)$/.test(target.tagName);
    if (event.key === "Escape") {
      event.preventDefault();
      close();
    } else if (!editingField && (event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "z") {
      event.preventDefault();
      event.shiftKey ? redo() : undo();
    } else if (!editingField && (event.key === "Delete" || event.key === "Backspace") && selected) {
      event.preventDefault();
      deleteSelected();
    }
  };

  const selectedNode = selected?.type === "node" ? graph.nodes.find((node) => node.id === selected.id) : undefined;
  const selectedEdge = selected?.type === "edge" ? graph.edges.find((edge) => edge.id === selected.id) : undefined;
  return (
    <div className="graph-overlay" role="dialog" aria-modal="true" aria-labelledby="graph-title" data-theme={theme} onKeyDown={handleDialogKeyDown}>
      <div className="graph-dialog">
        <header className="graph-header">
          <div><p className="graph-kicker">Causal graph</p><h2 id="graph-title">{initial.nodes.length ? "Edit graph" : "Create graph"}</h2></div>
          <button type="button" className="icon-button" aria-label="Close graph editor" onClick={close} autoFocus>×</button>
        </header>
        <div className="graph-toolbar" role="toolbar" aria-label="Graph tools">
          <button type="button" onClick={addNode} disabled={graph.nodes.length >= 50}>Add node</button>
          <button type="button" aria-pressed={edgeMode === "directed"} onClick={() => selectEdgeMode("directed")}>Directed edge</button>
          <button type="button" aria-pressed={edgeMode === "bidirected"} onClick={() => selectEdgeMode("bidirected")}>Bidirected edge</button>
          {edgeMode && <button type="button" onClick={stopEdgeMode}>Stop drawing</button>}
          <button type="button" onClick={arrange}>Top-down</button>
          <button type="button" onClick={() => cyRef.current?.fit(undefined, 48)}>Fit</button>
          <button type="button" onClick={undo} disabled={!history.past.length}>Undo</button>
          <button type="button" onClick={redo} disabled={!history.future.length}>Redo</button>
          <button type="button" onClick={deleteSelected} disabled={!selected}>Delete</button>
        </div>
        {edgeMode && <p className="mode-note">Drag from one node to another to create a {edgeMode} edge.</p>}
        <div className="graph-workspace">
          <div ref={canvasRef} className="graph-canvas" role="application" aria-label="Causal graph canvas" tabIndex={0} />
          <aside className="graph-inspector" aria-label="Selection properties">
            {selectedNode ? (
              <>
                <h3>Node</h3>
                <label>Label<input value={selectedNode.label} onChange={(event) => updateNode(selectedNode.id, { label: event.target.value })} /></label>
                <label>Role<select value={selectedNode.role} disabled={!selectedNode.observed} onChange={(event) => updateNode(selectedNode.id, { role: event.target.value as GraphNode["role"] })}><option value="standard">Standard</option><option value="exposure">Exposure</option><option value="outcome">Outcome</option><option value="adjusted">Adjusted</option></select></label>
                <label className="check-label"><input type="checkbox" checked={selectedNode.observed} onChange={(event) => updateNode(selectedNode.id, { observed: event.target.checked })} />Observed</label>
                {!selectedNode.observed && <p>Latent nodes use a dashed standard shape.</p>}
              </>
            ) : selectedEdge ? (
              <>
                <h3>Edge</h3>
                <label>Kind<select value={selectedEdge.kind} onChange={(event) => updateEdge(selectedEdge.id, { kind: event.target.value as EdgeKind })}><option value="directed">Directed</option><option value="bidirected">Bidirected</option></select></label>
                <label>Label<input value={selectedEdge.label} onChange={(event) => updateEdge(selectedEdge.id, { label: event.target.value })} placeholder="Optional" /></label>
              </>
            ) : <p>Select a node or edge to edit its properties.</p>}
          </aside>
        </div>
        <div className="graph-metadata">
          <label>Alternative text <span aria-hidden="true">*</span><textarea value={graph.alt} onChange={(event) => commit({ ...graphRef.current, alt: event.target.value })} placeholder="Describe the graph and its important relationships." required /></label>
          <label>Caption<textarea value={graph.caption} onChange={(event) => commit({ ...graphRef.current, caption: event.target.value })} placeholder="Optional caption" /></label>
        </div>
        {(errors.length > 0 || serverError) && <div className="graph-errors" role="alert">{serverError && <p>{serverError}</p>}<ul>{errors.map((error) => <li key={error}>{error}</li>)}</ul></div>}
        <footer className="graph-footer"><span>{graph.nodes.length}/50 nodes</span><div><button type="button" onClick={close}>Cancel</button><button type="button" className="primary" onClick={save} disabled={pending}>{pending ? "Saving…" : "Save graph"}</button></div></footer>
      </div>
    </div>
  );
}

function rebuildCy(cy: Core | null, graph: GraphModel): void {
  if (!cy) return;
  cy.elements().remove();
  cy.add([
    ...graph.nodes.map((node) => ({ data: { id: node.id, label: node.label, role: node.role, observed: node.observed }, position: { x: node.x, y: node.y } })),
    ...graph.edges.map((edge) => ({ data: { id: edge.id, source: edge.source, target: edge.target, kind: edge.kind, label: edge.label } })),
  ]);
}

function WritingEditor({ args }: ComponentProps): ReactElement {
  const editorArgs = args as EditorArgs;
  const argsRef = useRef(editorArgs);
  argsRef.current = editorArgs;
  const editorRef = useRef<HTMLDivElement>(null);
  const crepeRef = useRef<Crepe | null>(null);
  const currentMarkdown = useRef(editorArgs.default_value ?? "");
  const bookmarkRef = useRef<Bookmark>({ from: 1, to: 1 });
  const pendingRequest = useRef<string | null>(null);
  const observerRef = useRef<MutationObserver | null>(null);
  const [dialogGraph, setDialogGraph] = useState<GraphModel | null>(null);
  const [pending, setPending] = useState(false);
  const [serverError, setServerError] = useState("");
  const graphMapRef = useRef(new Map<string, GraphModel>());
  for (const graph of editorArgs.graphs ?? []) graphMapRef.current.set(graph.id, graph);

  const emitChange = useRef(debounce((markdown: string) => Streamlit.setComponentValue({ type: "content_change", markdown }), editorArgs.throttle_delay ?? 300));
  useEffect(() => () => emitChange.current.cancel(), []);

  const openGraph = useCallback((graphId?: string) => {
    const crepe = crepeRef.current;
    const latestArgs = argsRef.current;
    if (!crepe || !latestArgs.graph_enabled) return;
    crepe.editor.action((ctx) => {
      const view = ctx.get(editorViewCtx);
      bookmarkRef.current = { from: view.state.selection.from, to: view.state.selection.to, graphId };
    });
    const existing = graphId ? graphMapRef.current.get(graphId) : undefined;
    setDialogGraph(cloneGraph(existing ?? emptyGraph(latestArgs.new_graph_id ?? "")));
    setServerError("");
  }, []);

  const decorateCausalTokens = useCallback(() => {
    editorRef.current?.querySelectorAll<HTMLElement>('span[data-type="html"]').forEach((span) => {
      const value = span.dataset.value ?? "";
      const graphId = graphIdFromFigure(value);
      if (!graphId) return;
      span.classList.add("causal-graph-token");
      span.setAttribute("role", "button");
      span.setAttribute("tabindex", "0");
      span.setAttribute("aria-label", `Edit causal graph ${graphId}`);
      const label = `Causal graph · ${graphId}`;
      if (span.textContent !== label) span.textContent = label;
    });
  }, []);

  useEffect(() => {
    if (!editorRef.current || crepeRef.current) return;
    let disposed = false;
    const initialize = async () => {
      const features = editorArgs.features ?? {};
      const crepe = new Crepe({
        root: editorRef.current!,
        defaultValue: editorArgs.default_value ?? "",
        features: {
          [Crepe.Feature.CodeMirror]: features.codeblock === true,
          [Crepe.Feature.Latex]: features.math === true,
          [Crepe.Feature.Table]: features.table === true,
          [Crepe.Feature.ImageBlock]: false,
          [Crepe.Feature.LinkTooltip]: features.link === true,
          [Crepe.Feature.ListItem]: true,
          [Crepe.Feature.Cursor]: true,
          [Crepe.Feature.BlockEdit]: true,
          [Crepe.Feature.Placeholder]: true,
          [Crepe.Feature.Toolbar]: true,
        },
        featureConfigs: {
          [Crepe.Feature.Placeholder]: { text: editorArgs.placeholder ?? "Start writing…", mode: "doc" },
          [Crepe.Feature.BlockEdit]: {
            buildMenu: (builder: any) => {
              if (!editorArgs.graph_enabled) return;
              builder.getGroup("advanced").addItem("causal-graph", {
                label: "Causal graph",
                icon: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><circle cx="5" cy="12" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="M7.5 11 16 7M7.5 13 16 17" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
                onRun: (ctx: any) => {
                  ctx.get(commandsCtx).call(clearTextInCurrentBlockCommand.key);
                  queueMicrotask(() => openGraph());
                },
              });
            },
          },
        },
      });
      await crepe.create();
      if (disposed) { crepe.destroy(); return; }
      crepeRef.current = crepe;
      if (editorArgs.readonly) crepe.setReadonly(true);
      const handleChange = () => {
        let markdown = crepe.getMarkdown().replace(/<br\s*\/?>/gi, "\n").replace(/&nbsp;/gi, " ").replace(/\r\n?/g, "\n");
        if (markdown === currentMarkdown.current) return;
        currentMarkdown.current = markdown;
        emitChange.current(markdown);
      };
      const observer = new MutationObserver(() => decorateCausalTokens());
      observer.observe(editorRef.current!, { childList: true, subtree: true, characterData: true });
      observerRef.current = observer;
      editorRef.current!.addEventListener("input", handleChange);
      editorRef.current!.addEventListener("dblclick", (event) => {
        const token = (event.target as HTMLElement).closest<HTMLElement>(".causal-graph-token");
        if (token) openGraph(graphIdFromFigure(token.dataset.value ?? "") ?? undefined);
      });
      editorRef.current!.addEventListener("keydown", (event) => {
        const token = (event.target as HTMLElement).closest<HTMLElement>(".causal-graph-token");
        if (token && (event.key === "Enter" || event.key === " ")) { event.preventDefault(); openGraph(graphIdFromFigure(token.dataset.value ?? "") ?? undefined); }
      });
      decorateCausalTokens();
      Streamlit.setComponentReady();
      Streamlit.setFrameHeight(editorArgs.height ?? 640);
    };
    initialize().catch((error) => {
      if (editorRef.current) editorRef.current.innerHTML = `<div class="editor-error">Could not initialize the editor: ${String(error)}</div>`;
      Streamlit.setComponentReady();
    });
    return () => { disposed = true; observerRef.current?.disconnect(); crepeRef.current?.destroy(); crepeRef.current = null; };
  }, []);

  useEffect(() => {
    const response = editorArgs.graph_response;
    if (!response || response.request_id !== pendingRequest.current) return;
    setPending(false);
    if (!response.ok || !response.figure) {
      setServerError(response.error ?? "Could not save the causal graph.");
      return;
    }
    const crepe = crepeRef.current;
    if (!crepe) return;
    try {
      crepe.editor.action((ctx) => {
        const view = ctx.get(editorViewCtx);
        const htmlNode = view.state.schema.nodes.html?.create({ value: response.figure });
        if (!htmlNode) throw new Error("The editor HTML node is unavailable.");
        let transaction = view.state.tr;
        const replacingId = bookmarkRef.current.graphId;
        if (replacingId) {
          let foundPos = -1;
          let foundSize = 0;
          view.state.doc.descendants((node, pos) => {
            if (node.type.name === "html" && graphIdFromFigure(String(node.attrs.value ?? "")) === replacingId) {
              foundPos = pos;
              foundSize = node.nodeSize;
              return false;
            }
            return foundPos < 0;
          });
          if (foundPos < 0) throw new Error("The selected causal graph block is no longer in the document.");
          transaction = transaction.replaceWith(foundPos, foundPos + foundSize, htmlNode);
        } else {
          const max = view.state.doc.content.size;
          const from = Math.max(1, Math.min(bookmarkRef.current.from, max));
          const to = Math.max(from, Math.min(bookmarkRef.current.to, max));
          transaction = transaction.replaceWith(from, to, htmlNode);
        }
        view.dispatch(transaction.scrollIntoView());
      });
    } catch (error) {
      setServerError(`The graph was saved, but could not be inserted: ${String(error)}`);
      return;
    }
    if (response.graph) graphMapRef.current.set(response.graph.id, response.graph);
    const markdown = crepe.getMarkdown();
    currentMarkdown.current = markdown;
    Streamlit.setComponentValue({ type: "content_change", markdown });
    pendingRequest.current = null;
    setDialogGraph(null);
    setServerError("");
    queueMicrotask(decorateCausalTokens);
  }, [editorArgs.graph_response, decorateCausalTokens]);

  const requestSave = (graph: GraphModel) => {
    const requestId = crypto.randomUUID();
    pendingRequest.current = requestId;
    setPending(true);
    setServerError("");
    Streamlit.setComponentValue({ type: "graph_save", request_id: requestId, markdown: crepeRef.current?.getMarkdown() ?? currentMarkdown.current, graph });
  };

  return (
    <div className={`editor-shell${editorArgs.graph_enabled ? " has-actions" : ""}`} data-theme={editorArgs.theme ?? "light"} style={{ height: editorArgs.height ?? 640 }}>
      {editorArgs.graph_enabled && <div className="editor-actions"><button type="button" onClick={() => openGraph()}>Causal graph</button><span>or type <kbd>/</kbd> and choose Causal graph</span></div>}
      <div ref={editorRef} className="crepe-editor" />
      {dialogGraph && <GraphDialog initial={dialogGraph} theme={editorArgs.theme ?? "light"} pending={pending} serverError={serverError} onCancel={() => setDialogGraph(null)} onSave={requestSave} />}
    </div>
  );
}

const ConnectedEditor = withStreamlitConnection(WritingEditor);
createRoot(document.getElementById("root")!).render(<ConnectedEditor />);
