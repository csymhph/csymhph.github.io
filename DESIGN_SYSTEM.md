# Apple-Inspired Site Design System

## Status and scope

This document is the design authority for the public Jekyll site. It translates
Apple's design philosophy into rules for a small academic homepage; it is not a
request to copy Apple product pages or platform UI.

The site's purpose is to help a visitor quickly understand:

1. who Sangyeon Cho is,
2. what he studies and works on,
3. which work and writing are worth opening, and
4. how to contact him.

When visual novelty conflicts with those tasks, the tasks win.

## Source assessment

The supplied
[Apple Design Principles repository](https://github.com/hosseini-rtr/apple-design-principles)
is a useful orientation: keep interfaces simple, study real products, and focus
on experience rather than decoration. It is not a detailed or authoritative
design specification. Its third-party Figma link targets an old iOS 14 kit, and
the Design+Code and Sketch App Sources links are learning/resource catalogs, not
rules for an academic website.

Use this source order when guidance conflicts:

1. the site's purpose and verified visitor needs;
2. current Apple Human Interface Guidelines and accessibility guidance;
3. familiar web conventions and WCAG;
4. observations from current Apple web pages;
5. the supplied repository and third-party resource sites.

The current Apple principles are Purpose, Agency, Responsibility, Familiarity,
Flexibility, Simplicity, Craft, and Delight. The HIG also emphasizes hierarchy,
harmony, and consistency. The local rules below combine both sets.

## Local design principles

### 1. Purpose: make the academic identity immediate

- The first viewport must establish name, current role and affiliation, research
  focus, and a direct contact path.
- Give research, publications/projects, and writing more prominence than hobbies
  or decorative biography.
- Every section and component must answer a visitor question. Remove components
  that exist only to make the page look busier.

### 2. Agency: let visitors move directly

- Keep global navigation visible, conventional, and shallow: Home,
  Publications, Blog, Hobbies.
- Use descriptive link labels. Do not use `Click here`, hidden hover-only
  actions, forced carousels, modal introductions, or scroll-jacking.
- Open normal links in the same tab. Let the visitor choose a new tab.
- A CV, paper, code repository, or email action is shown only when a real target
  exists.

### 3. Responsibility: be accurate, private, and lightweight

- Do not invent publication status, dates, affiliations, metrics, or project
  outcomes. Mark incomplete information clearly.
- Do not add analytics, tracking, cookie banners, remote fonts, or third-party
  scripts without an explicit need and user approval.
- Do not import Apple logos, product art, SF Symbols, or downloaded Apple font
  files. Use a system-font stack and project-owned assets.
- Write useful alternative text for meaningful images and empty alternative text
  for purely decorative images.

### 4. Familiarity: use normal web behavior

- Links must look interactive in more than one state; text links remain
  recognizable without relying on color alone.
- Use semantic headings in order, lists for collections, and native links and
  buttons for actions.
- Keep one visual and behavioral treatment for each repeated role: navigation
  item, metadata, section heading, card/list row, tag, and call to action.
- Preserve the Jekyll + Minima + Markdown publishing model.

### 5. Flexibility: adapt without losing identity

- Design mobile-first and verify at 320, 390, 768, 1024, and 1440 CSS pixels.
- No page may require horizontal scrolling at 320 CSS pixels or 200% browser
  zoom.
- Text, navigation, cards, tables, code blocks, and math must reflow or scroll in
  their own appropriate container.
- Respect `prefers-color-scheme`, `prefers-reduced-motion`, and visible keyboard
  focus. Content must remain understandable when CSS, images, or motion are
  unavailable.

### 6. Simplicity: reduce, then style

- Prefer whitespace, alignment, typography, and concise copy over decoration.
- Use cards only when a boundary communicates a real grouping or action. Do not
  put every section in a rounded rectangle.
- Avoid ornamental gradients, glassmorphism, parallax, autoplay, large branded
  splash areas, and decorative icon sets.
- Progressive disclosure is allowed only for genuinely secondary information;
  essential identity and navigation stay visible.

### 7. Craft: use a small, explicit visual system

- Put site-wide styles in `assets/main.scss`. Add a layout/include override only
  when Minima's markup cannot express the required semantics or structure.
- Use semantic CSS custom properties rather than scattering raw color, spacing,
  radius, and shadow values.
- Keep components visually aligned to a shared content grid.
- Treat copy, front matter, focus states, dark mode, and responsive behavior as
  part of the design, not post-polish.

### 8. Delight: be human, not theatrical

- Let personality come from precise language, selected work, and the Hobbies
  page rather than decorative effects.
- Micro-interactions may confirm hover, focus, or activation, but must be quiet,
  fast, and unnecessary for comprehension.
- One distinctive accent and excellent typography are enough for the first
  version.

## Visual system

These are implementation constraints. Exact candidate color values can change
after contrast testing, but their semantic roles must remain.

### Typography

- UI/body stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  Helvetica, Arial, sans-serif`.
- Code stack: `ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`.
- Do not self-host SF Pro. Apple devices will naturally use the local system
  face; other devices get their familiar system face.
- Body text starts at 17px with roughly 1.6 line height. Do not use Light, Thin,
  or Ultralight for reading text.
- Long-form text is limited to about 68 characters per line. Wider page areas
  are reserved for lists, grids, figures, and tables.
- Use a compact, fluid type scale with no more than five public roles: display,
  page title, section title, body, and metadata.

### Color

- Define semantic roles for canvas, surface, primary text, secondary text,
  separator, accent, accent-hover, focus, and code background.
- Start from a neutral near-white canvas, near-black primary text, restrained
  gray surfaces, and one blue/cobalt accent. Color must not compete with content.
- Meet WCAG AA contrast: at least 4.5:1 for normal text and 3:1 for large text and
  meaningful non-text UI boundaries.
- Dark mode must remap semantic roles; it must not merely invert the page.
- Never communicate publication status, navigation state, or interaction by
  color alone. Add text, underline, weight, shape, or position.

### Spacing and geometry

- Use the spacing set `4, 8, 12, 16, 24, 32, 48, 64, 96px`; do not introduce
  one-off gaps without a documented reason.
- Reading content uses a narrow measure inside a wider shell. The shell should
  have responsive side padding rather than a fixed desktop gutter.
- Use no more than three corner-radius roles: small controls/tags, grouped
  surfaces, and featured media. Avoid fully rounded pills for ordinary text.
- Prefer a subtle separator over a shadow. Use shadows only when elevation
  explains layering or interaction.

### Interaction and motion

- Interactive targets are at least 44 by 44 CSS pixels on touch layouts, or have
  equivalent surrounding clickable space.
- Every interactive element needs hover, active, and `:focus-visible` states.
- Motion must explain feedback or state change. Prefer color, opacity, and small
  transforms lasting about 120–220ms.
- Under `prefers-reduced-motion: reduce`, remove nonessential transitions and
  transforms. Never use blinking, looping, or scroll-driven decorative motion.
- Do not add JavaScript for visual polish alone.

### Images and media

- Prefer authentic portrait, research, project, or hobby material over generic
  stock imagery. Do not block the redesign while no suitable image exists.
- Preserve aspect ratio, provide explicit dimensions where practical, and serve
  appropriately compressed files.
- A portrait is optional and may not displace the name, role, research summary,
  or contact action in the first viewport.

## Information architecture by page

### Home

Use this order:

1. compact introduction: name, role/affiliation, one-sentence research focus;
2. primary actions: email and GitHub, plus CV only when available;
3. research interests expressed as a concise sentence or short structured list;
4. selected work/projects with verified role and status;
5. latest news and latest writing;
6. a quiet contact/footer close.

Avoid a product-marketing hero. The introduction may use large type and generous
space, but it must remain compact enough to reveal substantive content nearby.

### Publications

- Prefer a readable chronological list over a visual card grid.
- When entries exist, show title first, then authors, venue/status, year, and
  verified links in that order.
- While the list is empty, use a brief honest status message; do not simulate
  publication cards.

### Blog

- Optimize for scanning: title is primary; date and category are secondary.
- Keep the entire list usable on narrow screens. Metadata stacks before it
  becomes cramped.
- Tags/categories use restrained text or subtle labels; avoid a field of pills.
- Article pages prioritize reading width, code/math overflow handling, heading
  hierarchy, and link visibility.

### Hobbies

- Keep the global system and typography, but allow a warmer editorial tone.
- Add imagery or richer sections only when authentic content is available.
- This page is the preferred place for personality; it must not dilute the
  academic focus of Home.

### Header and footer

- Header: name/site mark at the leading edge, four links at the trailing edge,
  a clear current-page state, and a simple mobile pattern.
- Footer: one contact path, GitHub, and a short copyright line. Avoid a sitemap
  that repeats the full header without need.
- Sticky or translucent navigation is optional and must prove that it improves
  navigation without hiding anchors, reducing contrast, or consuming too much
  mobile space.

## Implementation plan

### Phase 0 — baseline and content decisions

- Capture desktop and mobile screenshots of every public page.
- Inventory current content and flag claims that need correction or confirmation,
  including affiliation, project dates/roles, publication status, and contact
  preference.
- Record current page weight, Lighthouse results, and keyboard path if the local
  preview can run.

Done when the before-state and unresolved content questions are recorded without
changing factual claims.

### Phase 1 — foundations in `assets/main.scss`

- Replace one-off styling with semantic tokens for type, color, spacing, width,
  radius, border, focus, and motion.
- Establish body typography, reading measure, responsive shell, link/focus
  behavior, media defaults, code/math overflow, and system dark mode.
- Normalize the existing blog styles to use the same tokens.

Done when the existing pages remain structurally intact, work at all target
widths, pass contrast checks, and look coherent in light and dark mode.

### Phase 2 — navigation and site frame

- Reorder navigation to Home, Publications, Blog, Hobbies.
- First try to style Minima's existing header/footer. Add narrow `_includes` or
  `_layouts` overrides only if semantic current-page state, mobile behavior, or
  footer structure cannot be achieved otherwise.
- Verify skip navigation, keyboard focus order, anchor offsets, and 44px mobile
  targets.

Done when navigation is conventional, keyboard-complete, and stable from 320px
through wide desktop layouts.

### Phase 3 — homepage hierarchy

- Restructure `index.md` into the approved Home order using semantic sections.
- Tighten the introduction and headings while preserving only verified facts.
- Add selected work, latest news, and latest-writing treatments using simple
  lists or at most one purposeful grid.

Done when a first-time visitor can identify person, role, research focus, current
work, and contact path without hunting.

### Phase 4 — collection and reading pages

- Convert Publications into a durable bibliography pattern that also supports an
  honest empty state.
- Refine Blog list behavior and post typography without changing Markdown as the
  source of truth.
- Give Hobbies a light editorial treatment only to the extent supported by real
  content.

Done when repeated content roles are consistent and long text, tags, code, math,
and links work at narrow widths and 200% zoom.

### Phase 5 — validation and restraint pass

- Run the Jekyll build. Do not add Ruby dependencies merely to validate unless
  the user separately approves local build tooling.
- Test keyboard-only navigation, screen-reader landmarks/heading order, visible
  focus, 200% zoom, reduced motion, light/dark appearance, and no-horizontal-
  scroll behavior.
- Check WCAG AA contrast and run Lighthouse plus an automated accessibility scan
  when a preview is available.
- Compare final screenshots with the baseline and remove any decoration that does
  not improve hierarchy, comprehension, or interaction.

Done when the build succeeds, there are no critical automated accessibility
errors, core pages have no horizontal overflow, and remaining untested risks are
explicitly documented.

## Definition of done for the redesign

- Jekyll builds without errors and GitHub Pages-compatible structure is retained.
- Name, role, research focus, and contact are apparent in the first Home viewport
  at 390px and desktop widths.
- All pages work at 320px and 200% zoom without page-level horizontal scrolling.
- Body copy is at least 16px, reading measure stays near 68 characters, and text
  contrast meets WCAG AA.
- All navigation and actions work by keyboard with visible focus; touch targets
  are at least 44px where applicable.
- Reduced-motion and system dark-mode preferences are respected.
- No remote font, tracking script, heavy framework, or decorative JavaScript is
  added.
- Page content remains Markdown-centered and factual claims remain verified.

## Primary references

- [Supplied Apple Design Principles repository](https://github.com/hosseini-rtr/apple-design-principles)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Apple design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles)
- [Apple layout guidance](https://developer.apple.com/design/human-interface-guidelines/layout)
- [Apple typography guidance](https://developer.apple.com/design/human-interface-guidelines/typography)
- [Apple accessibility guidance](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [Apple color guidance](https://developer.apple.com/design/human-interface-guidelines/color)
- [Apple motion guidance](https://developer.apple.com/design/human-interface-guidelines/motion)
- [Apple writing guidance](https://developer.apple.com/design/human-interface-guidelines/writing)
- [Apple UI design dos and don'ts](https://developer.apple.com/design/tips/)
- [Apple Design Resources](https://developer.apple.com/design/resources/)
- [Apple homepage, used only as an observational reference](https://www.apple.com/)

Last source review: 2026-07-20.
