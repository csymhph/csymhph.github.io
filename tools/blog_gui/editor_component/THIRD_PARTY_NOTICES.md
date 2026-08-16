# Writing Studio editor dependencies

The Writing Studio frontend is built ahead of time. The files under `build/`
are checked into the repository so running the local Streamlit app does not
require Node.js or an npm install.

Direct runtime dependencies are pinned in `frontend/package.json` and
`frontend/package-lock.json`:

- Milkdown Crepe and Milkdown Kit 7.15.1 — MIT license
- Cytoscape.js 3.34.0 — MIT license
- Cytoscape.js edgehandles 4.0.1 — MIT license
- React and React DOM 18.3.1 — MIT license
- Streamlit Component Lib 2.0.0 — Apache-2.0 license
- lodash.debounce 4.0.8 — MIT license

The causal graph editor UI, v1 validation contract, canonical figure
serialization, and static SVG exporter are project-owned code. DAGitty and its
GPL SVG exporter are not bundled or copied.

Upstream sources:

- <https://github.com/Milkdown/milkdown>
- <https://github.com/cytoscape/cytoscape.js>
- <https://github.com/cytoscape/cytoscape.js-edgehandles>
- <https://github.com/facebook/react>
- <https://github.com/streamlit/streamlit-component-template>
- <https://github.com/lodash/lodash>
