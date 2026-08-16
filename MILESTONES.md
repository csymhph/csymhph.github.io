# Project Milestones

This document is the high-level status board for `csymhph.github.io`.
Use `progress.md` for chronological implementation notes and verification
details. Update this file when a milestone changes state, scope, dependency, or
completion criteria.

## Status summary

| Milestone | Status | Outcome |
| --- | --- | --- |
| M0. Project foundation | Complete | Repository rules, direction, progress tracking, and local environment established |
| M1. Design system | Complete | Apple-inspired, accessibility-conscious design rules documented |
| M2. Multipage visual demo | Complete | Approved navigation, page hierarchy, and light/dark visual direction demonstrated |
| M3. Local Writing Studio | Complete | Local drafting, editing, publishing, Git sync, and macOS launch flow working |
| M4. Production Jekyll redesign | Complete | Production layouts are live; Pages build and desktop/mobile browser checks passed |
| M4.1. Causal Graph Authoring | In progress | Local implementation and automated tests are complete; browser and release validation remain |
| M5. Cloud Writing Studio | Deferred | Move authoring to a private Streamlit Community Cloud app for arbitrary-device access |
| M6. Integrated release and operations | Not started | Connect the production site, cloud editor, publishing flow, and operating documentation |

The public Jekyll site now uses the approved visual system. The files under
`design-demo/` remain historical prototypes rather than production templates.

## M0. Project foundation

**Status:** Complete

Delivered:

- Established project instructions in `AGENTS.md`.
- Added the concise product/content direction in `EDITING_DIRECTION.md`.
- Added chronological work tracking in `progress.md`.
- Preserved the Jekyll + Minima + Markdown publishing model.
- Created and recorded the `vibe_csymhph_github_io` Python 3.11 environment for
  local Writing Studio work.

Completion criteria:

- Project-specific rules, environment, verification expectations, and durable
  work records exist at the repository root.

## M1. Design system

**Status:** Complete

Delivered:

- Reviewed the supplied Apple design-principles material and its linked
  resources against current authoritative guidance.
- Added `DESIGN_SYSTEM.md` as the visual and interaction authority.
- Defined information architecture, semantic color and type roles, responsive
  behavior, accessibility constraints, motion rules, and implementation phases.
- Explicitly retained an academic, content-first identity rather than copying a
  product-marketing page.

Completion criteria:

- Future public-site design decisions have documented principles and measurable
  validation requirements.

## M2. Multipage visual demo

**Status:** Complete

Delivered:

- Added separate Home, Publications, Blog, Hobbies, and Post demos under
  `design-demo/`.
- Replaced anchor scrolling with conventional page-to-page navigation.
- Added persistent light/dark appearance selection with system preference as
  the initial default.
- Demonstrated responsive layouts, content hierarchy, focus treatment, reading
  width, and a growing blog archive structure.
- Added a prototype Writing Studio action.

Completion criteria:

- All demo pages open directly, local links resolve, navigation is consistent,
  and the visual direction is ready to translate into Jekyll templates.

Follow-up:

- Perform one manual light-appearance pass in the preferred browser while doing
  the production translation.

## M3. Local Writing Studio

**Status:** Complete

Delivered:

- Added Streamlit draft creation, post editing, front matter handling, preview,
  MathJax support, and guarded deletion.
- Added the themed Crepe Markdown editor and matching light/dark appearance.
- Added narrow Git status, commit, and push controls for selected `_posts`
  files.
- Redesigned the interface as `Sangyeon Cho · Writing Studio` using the same
  visual language as the site demo.
- Added an idempotent local launcher and the `csymhph-blog://open` macOS URL
  handler, bound to `127.0.0.1` only.
- Documented the local launch and security boundary in
  `tools/blog_gui/LAUNCHING.md`.

Completion criteria:

- The app runs in the recorded Conda environment, passes Streamlit AppTest, can
  complete the local draft-to-publish flow, and reuses one healthy local server.

Long-term role:

- Retain the local launcher as a development and fallback path after cloud
  authoring is introduced.

## M4. Production Jekyll redesign

**Status:** Complete

Objective:

- Translate the approved multipage demo into the real Jekyll + Minima site
  without disrupting the Markdown-centered publishing model.

Planned work:

- [x] Inventory the production structure and preserve the existing factual content.
- [x] Add semantic design tokens and shared foundations in `assets/main.scss`.
- [x] Implement the production header, footer, current-page navigation, and
      light/dark appearance control.
- [x] Apply the approved Home, Publications, Blog, Hobbies, and Post hierarchy.
- [x] Add responsive handling for code, math, tables, media, and long-form content at
      narrow widths.
- [x] Validate keyboard access, focus, contrast, reduced motion, 200% zoom, and
      target responsive widths.
- [x] Run and inspect the GitHub Pages build after the approved commit/push.

Completion criteria:

- Production pages match the approved direction, factual claims remain
  verified, no page requires unintended horizontal scrolling, light and dark
  appearances work, and the Jekyll build succeeds.

## M4.1. Causal Graph Authoring

**Status:** In progress — local implementation and automated verification complete;
manual browser and release validation pending

Objective:

- Add a causal-graph block to the local Writing Studio while publishing only a
  static, accessible SVG to the public site.

Delivered locally:

- [x] Replaced the runtime-patched `streamlit-crepe` wrapper with a repository-
      owned Milkdown/Crepe Streamlit component and checked-in production build.
- [x] Added Cytoscape.js and edgehandles with directed and bidirected edge
      creation, node roles, observed/latent state, labels, layout, fit,
      undo/redo, deletion, required alternative text, and optional captions.
- [x] Added the v1 JSON validator, safe graph IDs, directed-cycle detection,
      deterministic fixed-white SVG export, XML escaping, and canonical figure
      serialization.
- [x] Added private draft graph storage, atomic draft-to-post promotion,
      published graph updates, shared-draft protection, and non-destructive
      orphan handling.
- [x] Added graph-aware publish bundles so a graph-only update selects its SVG
      and private JSON source without staging unrelated paths.
- [x] Added Python and frontend unit coverage and retained build artifacts so
      launching the Studio does not require npm.
- [ ] Manually verify cursor insertion, graph re-editing, focus, drag/zoom,
      light/dark Studio appearance, and narrow-screen behavior in a browser.
- [ ] After separately approved commits and pushes, verify the GitHub Pages
      build and a published SVG's alternative text and caption.

Completion criteria:

- A saved draft or published post can create and re-edit a valid graph at the
  current cursor, failed saves preserve content and selection, publishing
  promotes JSON/SVG/body atomically, and the public result is a readable static
  SVG with alternative text and an optional caption.

## M5. Cloud Writing Studio

**Status:** Deferred by user decision; resume later

Objective:

- Make the Writing Studio available from arbitrary devices through a private
  Streamlit Community Cloud app while keeping the public blog on GitHub Pages.

User preparation when resumed:

- [ ] Connect the `csymhph` GitHub account at `share.streamlit.io`.
- [ ] Preferably create a private `csymhph/blog-drafts` repository.
- [ ] Create a fine-grained GitHub token restricted to the site repository and,
      if used, the draft repository, with `Contents: Read and write` only and a
      lifetime of no more than 90 days.
- [ ] Enter credentials only in Streamlit Secrets; never commit them or paste
      them into project files or chat.
- [ ] Deploy `tools/blog_gui/app.py` from `main` using Python 3.11 and immediately
      restrict the app to approved viewers.

Implementation work when resumed:

- [ ] Separate local and cloud storage/publishing backends.
- [ ] Replace cloud-side filesystem persistence and Git subprocesses with the
      GitHub API.
- [ ] Add persistent cross-device draft autosave and stale-version conflict
      detection.
- [ ] Add mobile-friendly image upload and repository asset handling.
- [ ] Add an application-level administrator email check in addition to
      Streamlit private-app access.
- [ ] Show saving, commit, GitHub Pages build, and published states.
- [ ] Treat Streamlit local storage as temporary and keep GitHub as the durable
      source of truth.

Completion criteria:

- An authorized user can safely create, resume, edit, and publish a post from a
  new desktop or mobile browser; secrets never reach the repository or browser;
  unauthorized viewers cannot access authoring actions; and publication updates
  the GitHub Pages site.

## M6. Integrated release and operations

**Status:** Not started; depends on M4, M4.1, and M5

Planned work:

- [ ] Replace the production Writing Studio action with the verified private
      Streamlit HTTPS URL while retaining the local URL handler only for local
      development.
- [ ] Verify the complete public-site-to-editor-to-publish flow on desktop and
      mobile.
- [ ] Document deployment, secret rotation, recovery, and local fallback.
- [ ] Verify GitHub Pages successfully builds and publishes the updated site.
- [ ] Follow `gitpolicy.md` before any requested commit, push, branch, or pull
      request operation.

Completion criteria:

- The public site is stable and accessible, the private authoring flow works
  across devices, operational recovery steps are documented, and the deployed
  result has been manually checked.

## Current recommended sequence

1. Complete M4's separately approved release and browser validation.
2. Complete M4.1's manual browser pass, then release and validate it separately.
3. Resume M5 when Streamlit account, draft-storage choice, and repository token
   are ready.
4. Complete M6 only after all production surfaces have been independently
   verified.

Avoid combining M4, M4.1, and M5 into one large unverified release. They can be
built and tested independently before the final integration.
