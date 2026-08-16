export const GRAPH_ID_PATTERN = /^cg-\d{8}-[a-z0-9]{8}$/;
export const MAX_NODES = 50;

export type NodeRole = "standard" | "exposure" | "outcome" | "adjusted";
export type EdgeKind = "directed" | "bidirected";

export interface GraphNode {
  id: string;
  label: string;
  x: number;
  y: number;
  role: NodeRole;
  observed: boolean;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  kind: EdgeKind;
  label: string;
}

export interface GraphModel {
  id: string;
  schema_version: 1;
  alt: string;
  caption: string;
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export function validateGraph(graph: GraphModel): ValidationResult {
  const errors: string[] = [];
  if (!GRAPH_ID_PATTERN.test(graph.id)) errors.push("Invalid causal graph ID.");
  if (graph.schema_version !== 1) errors.push("schema_version must be 1.");
  if (!graph.alt.trim()) errors.push("Alternative text is required.");
  if (!graph.nodes.length) errors.push("Add at least one node.");
  if (graph.nodes.length > MAX_NODES) errors.push(`Causal graphs support at most ${MAX_NODES} nodes.`);

  const ids = new Set<string>();
  const labels = new Set<string>();
  for (const node of graph.nodes) {
    if (!/^[A-Za-z0-9_-]{1,64}$/.test(node.id) || ids.has(node.id)) errors.push(`Invalid or duplicate node ID: ${node.id}`);
    ids.add(node.id);
    const label = node.label.normalize("NFC").trim();
    if (!label) errors.push(`Node ${node.id} needs a label.`);
    const key = label.toLocaleLowerCase();
    if (labels.has(key)) errors.push(`Duplicate node label: ${label}`);
    labels.add(key);
    if (!Number.isFinite(node.x) || !Number.isFinite(node.y)) errors.push(`Node ${node.id} needs finite coordinates.`);
    if (!node.observed && node.role !== "standard") errors.push(`Latent node ${label} must use the standard role.`);
  }

  const edgeIds = new Set<string>();
  const edgeKeys = new Set<string>();
  const directed: Array<[string, string]> = [];
  for (const edge of graph.edges) {
    if (!/^[A-Za-z0-9_-]{1,64}$/.test(edge.id) || edgeIds.has(edge.id)) errors.push(`Invalid or duplicate edge ID: ${edge.id}`);
    edgeIds.add(edge.id);
    if (!ids.has(edge.source) || !ids.has(edge.target)) errors.push(`Edge ${edge.id} refers to a missing node.`);
    if (edge.source === edge.target) errors.push(`Self-edge is not allowed: ${edge.id}`);
    const pair = edge.kind === "bidirected" ? [edge.source, edge.target].sort().join("|") : `${edge.source}|${edge.target}`;
    const key = `${edge.kind}|${pair}`;
    if (edgeKeys.has(key)) errors.push(`Duplicate ${edge.kind} edge between ${edge.source} and ${edge.target}.`);
    edgeKeys.add(key);
    if (edge.kind === "directed") directed.push([edge.source, edge.target]);
  }
  if (hasDirectedCycle([...ids], directed)) errors.push("Directed edges must form an acyclic graph.");
  return { valid: errors.length === 0, errors };
}

export function hasDirectedCycle(nodes: string[], edges: Array<[string, string]>): boolean {
  const adjacency = new Map(nodes.map((id) => [id, [] as string[]]));
  const indegree = new Map(nodes.map((id) => [id, 0]));
  for (const [source, target] of edges) {
    adjacency.get(source)?.push(target);
    indegree.set(target, (indegree.get(target) ?? 0) + 1);
  }
  const queue = nodes.filter((id) => indegree.get(id) === 0).sort();
  let visited = 0;
  while (queue.length) {
    const id = queue.shift()!;
    visited += 1;
    for (const target of (adjacency.get(id) ?? []).sort()) {
      indegree.set(target, (indegree.get(target) ?? 0) - 1);
      if (indegree.get(target) === 0) queue.push(target);
    }
    queue.sort();
  }
  return visited !== nodes.length;
}

export function escapeXml(value: string, attribute = false): string {
  const escaped = value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  return attribute ? escaped.replace(/"/g, "&quot;").replace(/'/g, "&apos;") : escaped;
}

export function canonicalFigure(graph: GraphModel): string {
  const lines = [
    `<figure class="causal-figure" data-causal-graph="${graph.id}">`,
    `  <img src="/assets/causal-graphs/${graph.id}.svg" alt="${escapeXml(graph.alt.trim(), true)}">`,
  ];
  if (graph.caption.trim()) lines.push(`  <figcaption>${escapeXml(graph.caption.trim())}</figcaption>`);
  lines.push("</figure>");
  return lines.join("\n");
}

export function graphIdFromFigure(value: string): string | null {
  const match = value.match(/<figure\s+class="causal-figure"\s+data-causal-graph="(cg-\d{8}-[a-z0-9]{8})">/);
  return match?.[1] ?? null;
}

export function insertFigureAtMarkdownOffset(markdown: string, figure: string, offset: number, replacingId?: string): string {
  if (replacingId) {
    const escapedId = replacingId.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const pattern = new RegExp(`<figure\\s+class="causal-figure"\\s+data-causal-graph="${escapedId}">[\\s\\S]*?<\\/figure>`);
    if (pattern.test(markdown)) return markdown.replace(pattern, figure);
  }
  const safeOffset = Math.max(0, Math.min(offset, markdown.length));
  const before = markdown.slice(0, safeOffset).replace(/\s*$/, "");
  const after = markdown.slice(safeOffset).replace(/^\s*/, "");
  return [before, figure, after].filter(Boolean).join("\n\n");
}

export function graphToSvg(graph: GraphModel): string {
  const checked = validateGraph(graph);
  if (!checked.valid) throw new Error(checked.errors.join(" "));
  const nodes = [...graph.nodes].sort((a, b) => a.id.localeCompare(b.id));
  const edges = [...graph.edges].sort((a, b) => a.id.localeCompare(b.id));
  const minX = Math.min(...nodes.map((node) => node.x)) - 72;
  const minY = Math.min(...nodes.map((node) => node.y)) - 72;
  const maxX = Math.max(...nodes.map((node) => node.x)) + 72;
  const maxY = Math.max(...nodes.map((node) => node.y)) + 72;
  const width = Math.max(240, maxX - minX);
  const height = Math.max(180, maxY - minY);
  const byId = new Map(nodes.map((node) => [node.id, node]));
  const lines = [
    `<?xml version="1.0" encoding="UTF-8"?>`,
    `<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 ${width} ${height}">`,
    `  <title id="title">${escapeXml(graph.alt.trim())}</title>`,
    `  <desc id="desc">Static causal graph. Directed arrows show causal paths; double-headed arrows show bidirected relationships.</desc>`,
    `  <rect width="${width}" height="${height}" fill="#ffffff"/>`,
    `  <defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#24272b"/></marker></defs>`,
    `  <g class="edges" fill="none" stroke="#24272b" stroke-width="2">`,
  ];
  for (const edge of edges) {
    const source = byId.get(edge.source)!;
    const target = byId.get(edge.target)!;
    const start = edge.kind === "bidirected" ? ` marker-start="url(#arrow)"` : "";
    lines.push(`    <line data-edge="${escapeXml(edge.id, true)}" x1="${source.x - minX}" y1="${source.y - minY}" x2="${target.x - minX}" y2="${target.y - minY}"${start} marker-end="url(#arrow)"/>`);
    if (edge.label) lines.push(`    <text>${escapeXml(edge.label)}</text>`);
  }
  lines.push("  </g>", '  <g class="nodes">');
  for (const node of nodes) {
    const dash = node.observed ? "" : ' stroke-dasharray="7 5"';
    lines.push(`    <g data-node="${escapeXml(node.id, true)}"${dash}><title>${escapeXml(node.label)}</title></g>`);
  }
  lines.push("  </g>", "</svg>", "");
  return lines.join("\n");
}

export interface HistoryState {
  past: GraphModel[];
  present: GraphModel;
  future: GraphModel[];
}

export type HistoryAction =
  | { type: "commit"; graph: GraphModel }
  | { type: "undo" }
  | { type: "redo" }
  | { type: "reset"; graph: GraphModel };

export function historyReducer(state: HistoryState, action: HistoryAction): HistoryState {
  if (action.type === "commit") return { past: [...state.past, state.present], present: action.graph, future: [] };
  if (action.type === "undo" && state.past.length) return { past: state.past.slice(0, -1), present: state.past.at(-1)!, future: [state.present, ...state.future] };
  if (action.type === "redo" && state.future.length) return { past: [...state.past, state.present], present: state.future[0], future: state.future.slice(1) };
  if (action.type === "reset") return { past: [], present: action.graph, future: [] };
  return state;
}
