# Project Milestones

This document is the high-level status board for `csymhph.github.io`.
Use `progress.md` for chronological implementation notes and verification
details. Update this file when a milestone changes state, scope, dependency, or
completion criteria.

## Status summary

| Milestone | Status | Outcome |
| --- | --- | --- |
| M0. Project foundation | Complete | Repository rules, direction, progress tracking, and local environment established |
| M1. Design system | Superseded | Apple-inspired rules; premise retired 2026-08-21 and replaced by the thesis-driven `DESIGN_SYSTEM.md` |
| M2. Multipage visual demo | Complete | Approved navigation, page hierarchy, and light/dark visual direction demonstrated |
| M3. Local Writing Studio | Complete | Local drafting, editing, publishing, Git sync, and macOS launch flow working |
| M4. Production Jekyll redesign | Complete | Production layouts are live; Pages build and desktop/mobile browser checks passed |
| M4.1. Causal Graph Authoring | In progress | Released as `f476628` and pushed; browser pass part-done with two defects fixed and one open |
| M4.2. Thesis-driven site rebuild | In progress | Production translation and automated checks complete; manual visual pass and owner-supplied assets remain |
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

**Status:** In progress — released to `main` as commit `f476628` and pushed; the
manual browser pass is part-done (paused 2026-08-17) with one open defect and
some checks outstanding

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
- [x] Manually verify cursor insertion, graph re-editing, edge drag, the
      required alternative-text gate, and the dark Studio appearance in a
      browser. Done 2026-08-17 by driving Edge over the DevTools Protocol.
- [x] Fix the clipped Writing Studio title field: the enlarged input was cut off
      by Streamlit's fixed-height, `overflow: hidden` wrapper.
- [x] Fix `addNode` stacking every new node on one point, which made nodes
      impossible to tell apart, select, or connect.
- [ ] Fix the open re-editing defect: reopening a saved graph leaves the edge
      source node and its edges invisible because Cytoscape keeps a stale
      memoised `takesUpSpace()`. The model, saving, and the published SVG are
      all correct, so this is display-only. See `progress.md` for the
      investigation and the reverted fix attempt.
- [ ] Manually verify the light Studio appearance, narrow screens, 200% zoom,
      keyboard/focus inside the graph editor, and node-drag coordinate
      persistence.
- [ ] Manually verify publish promotion, which moves the post body, private
      JSON, and SVG together.
- [x] Release M4.1 separately. Committed as `f476628` and pushed; `main` is in
      sync with `origin/main`.
- [ ] Verify a published SVG's alternative text and caption on the live site.
      Blocked until a post actually contains a graph — no file exists yet under
      `assets/causal-graphs/`.

Completion criteria:

- A saved draft or published post can create and re-edit a valid graph at the
  current cursor, failed saves preserve content and selection, publishing
  promotes JSON/SVG/body atomically, and the public result is a readable static
  SVG with alternative text and an optional caption.

## M4.2. Thesis-driven site rebuild

**Status:** In progress — production translation and automated verification are
complete; the owner-supplied portrait/CV/LinkedIn targets and a manual browser
pass remain

Objective:

Rebuild the public site against the rewritten `DESIGN_SYSTEM.md`, whose thesis is
that the site is a document making one claim, that staleness is the primary
failure mode, and that visual volume must not exceed content volume. The rebuild
is judged by that document's positive criteria 1–7, not by the accessibility
floors alone.

This is a revision of M4's production site, not a new site. Preserve Jekyll +
Minima + Markdown, add no frameworks, and keep the Writing Studio untouched.

### Phase ordering and dependencies

Phase A precedes everything. Phase B precedes E and F, because untokenised type
would have to be redone after any markup change. Phase C precedes E. Phases D and
G depend only on B. Three phases are gated on material only the site owner can
supply; those gates are named in the phases themselves so the rest can proceed.

### Phase A — Baseline capture

- [ ] Record the before-state at 320, 390, 768, and 1440 CSS pixels in light and
      dark mode.
- [x] Record the current measurements the rebuild will be judged against: the
      count of `font-size` declarations and distinct values, the largest rendered
      heading, and the measured contrast of every boundary token.
- [x] Assess the current site against positive criteria 1–7 and record which
      already pass.

The screenshot item remains open because workspace policy forbids the agent from
controlling a browser or browser tab. The source-measurable baseline is recorded
in `../progress.md` at all four target widths.

Done when the before-state and the failing criteria are recorded in
`../progress.md` without any factual claim on the site being changed.

### Phase B — Tokens, type scale, and boundary contrast

- [x] Add the five type tokens and map every `font-size` in `assets/main.scss`
      onto one of them.
- [x] Cap `h1` at `clamp(1.75rem, 4vw, var(--type-title))`, replacing the current
      5.8rem home title, 6rem page title, 4.4rem narrow-screen page title, and
      5.2rem article title.
- [x] Split the single `--line` token into `--separator` and `--border-control`,
      and apply `--border-control` to the theme toggle and the secondary button,
      which are currently perceivable only through a 1.34:1 border.
- [x] Leave all markup and content untouched in this phase.

Done when no `font-size` value exists outside the five tokens, no rendered
heading exceeds 36px, both control borders measure at least 3:1 in light and dark
mode, the Jekyll build is clean, and every page is structurally unchanged.

Verify with a declaration inventory, recomputed contrast ratios, a Jekyll build,
and a visual pass at the four widths.

### Phase C — One source for identity

- [x] Replace the third research area. The set is now causal inference,
      uncertainty quantification, and **explainability**; time-series analysis is
      out as a peer area and moves into the causal inference description as the
      longitudinal setting. Two of the five works are attribution papers, which
      the old set did not name at all, while time-series appeared in one. See the
      areas section of `DESIGN_SYSTEM.md`.
- [x] Define the areas once in `_config.yml` and render them on Home. The retired
      Publications page is excluded from the public build instead of retaining a
      second research-area surface.
- [x] Rewrite the area descriptions so each one states what it settles about an
      action, rather than describing a field. The areas are the answer to the
      claim, not a keyword list beside it.
- [x] Add a config key for the settled claim sentence.
      The homepage eyebrow reading `Causality · Uncertainty · Explanation` is
      removed with every other eyebrow in Phase E, but note that it was the
      accurate statement and the areas list was the inaccurate one.

Done when the areas are defined in exactly one place, the public Home renders
from it, and no competing area list remains in the public build.

The claim gate was cleared by the site owner on 2026-08-21. The final sentence
is recorded in `DESIGN_SYSTEM.md` and can be added with the config key.

### Phase D — Single page, navigation, and blog dormancy

- [x] Collapse the public site to one page. Fold `publications.md` and
      `hobbies.md` into sections of `index.md`, ordered per the Home list in
      `DESIGN_SYSTEM.md`, with Hobbies last.
- [x] Replace the navigation with in-page anchors for every substantive section:
      `Research interests`, `Works`, `Research projects`, `News`, `Education`,
      and `Hobbies`, with the site name linking to the top. Labels must match the
      section headings exactly. Drop the current-page state from
      `_includes/header.html`; there is one page.
- [x] Add `scroll-margin-top` to anchor targets and apply smooth scrolling only
      under `prefers-reduced-motion: no-preference`. Add no scroll-spy script.
- [x] Keep real anchor targets as a no-JavaScript fallback, but prevent same-page
      navigation from persisting fragments in the URL or history. Reload Home at
      the top rather than restoring the last section.
- [x] Do not retain or redirect `/publications/` and `/hobbies/`; the owner does
      not require backward compatibility for those URLs.
- [x] Remove the blog anchor, the writing section, and the post counter, so no
      route leads to an empty archive.
- [x] Leave `_posts`, the post layout, post typography, `mathjax.html`, and the
      Writing Studio in place and working.

Done when the public site is one page, every navigation label matches the heading
it targets, no route reaches an empty archive, and the post machinery still
builds. Verification used Jekyll's `--unpublished` mode in a temporary output
directory, which exercises every dormant post without modifying source files.

This reverses M2's move from anchor scrolling to page-to-page navigation. See the
Information architecture section of `DESIGN_SYSTEM.md` for why.

### Phase E — Homepage hierarchy

- [x] Put name, role, and the claim in the first screen, with nothing before them.
- [x] Remove the profile card, which restates the introduction paragraph
      sentence for sentence and carries no additional information.
- [x] Resolve the one-item News section: feed it or fold it. A section with one
      entry is a sentence.
- [x] Keep the research-areas block on Home only.
- [x] Remove every eyebrow and section label sitewide, including the five on Home
      that restate the heading beneath them and the one above the name that
      introduced a research area appearing nowhere else. Drop the label role from
      the stylesheet so it cannot return.
- [x] Apply the heading set from rule 9: Research interests, Works, Research
      projects, News, Education. The current `Areas of work`, `Work`, and
      `Projects` are portfolio vocabulary.
- [x] Write publication author lists in full. Surname-only abbreviation makes
      distinct coauthors indistinguishable — two of the papers have two different
      Chos — and drops the equal-contribution and corresponding-author markers.
      Keep the footnote that defines those markers wherever they appear.
- [x] Correct the affiliation framing. `incoming Ph.D. student` appears in
      `_config.yml`'s description and `job`, the homepage introduction, the
      profile card, and the education row, which frames the Causality Lab
      membership as not yet begun. The membership is current; only the degree
      programme changes in September 2026.
- [x] Write the email address as plain text in the introduction and the footer.
      Remove the Email, Google Scholar, and GitHub actions; the site keeps no
      buttons. Add the portrait when an image exists, and CV and LinkedIn when
      their targets exist. See rule 7.

Done when criteria 1 through 3 pass on a cold read-through and no section
restates another.

Gated: the portrait image file, the LinkedIn profile URL, and the CV PDF.
Rule 5 forbids shipping any of these as a placeholder or a "coming soon", so each
action stays absent until its target exists.

### Phase F — Publications and Hobbies

- [x] Keep the Works list direct: no `Selected` qualifier and no introductory
      sentence explaining that the visible list is short.
- [x] Add per-entry links wherever a public artifact genuinely exists; add none
      where it does not.
- [x] Remove the duplicated public research-areas surface by excluding the
      retired Publications page from the build.
- [x] Replace the four Hobbies placeholder cards, whose copy currently describes
      what the cards could someday contain, with real content.

Done when repeated content roles are consistent and no placeholder copy remains
on any public page.

The owner settled the current Hobbies content as the three names Calligraphy,
Piano, and Baseball. No descriptive copy was invented.

### Content TODOs

- [ ] After the contract is executed, add the new AFINIT project expected to
      begin in October 2026. Do not publish it before contract execution.

### Phase G — Validation and restraint pass

- [x] Test all seven positive criteria at source/build level, including the
      semantic-hierarchy and one-file-edit tests.
- [ ] Complete the manual CSS-disabled visual read-through in a browser.
- [ ] Test every browser-only floor: keyboard path with visible focus, 320px and
      200% zoom without horizontal scrolling, and light/dark appearance.
- [x] Verify reduced-motion rules and light/dark control-boundary contrast from
      generated CSS.
- [x] Run the Jekyll build with Homebrew Ruby 3.3.
- [ ] Compare final screenshots with the Phase A visual record.
- [x] Remove any remaining decoration that does not improve hierarchy,
      comprehension, or interaction.
- [ ] Follow `gitpolicy.md` before any requested commit, push, branch, or pull
      request operation.

Automated validation covers the generated hierarchy, anchors, routes, type
tokens, theme behavior, contrast, reduced-motion rules, dormant post rendering,
YAML, JavaScript syntax, build output, and whitespace. Browser-only checks stay
open because this workspace forbids agent control of browsers and tabs.

Done when all seven positive criteria hold, every floor passes, and any untested
risk is recorded explicitly in `../progress.md`.

Completion criteria:

- The rewritten design system's positive criteria 1–7 all hold, the floors all
  pass, the site carries no placeholder copy or dead-end route, and the type and
  boundary systems are token-driven with no value outside them.

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

1. M4 and M4.1 are both released and pushed. Nothing further is pending on the
   release side.
2. Manually review the implemented M4.2 page at the target widths, both
   appearances, keyboard focus, and 200% zoom. Supply the portrait, CV, and
   LinkedIn targets when ready; the live templates omit them safely until then.
3. Finish M4.1's manual browser pass and resolve the open reopened-graph display
   defect. Independent of M4.2 — the Studio is authoring tooling, not a public
   surface — so either order works.
4. Resume M5 when Streamlit account, draft-storage choice, and repository token
   are ready.
5. Complete M6 only after all production surfaces have been independently
   verified.

Avoid combining M4.1, M4.2, and M5 into one large unverified release. They can be
built and tested independently before the final integration. Within M4.2, Phase B
must land before E and F, or the type work will have to be redone after the
markup changes.
