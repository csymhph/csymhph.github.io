# Site Design System

## Status and scope

This document is the design authority for the public Jekyll site. Every rule
below is derived from the thesis in the next section, or from the survey of
comparable sites recorded further down. A rule with no derivation does not
belong here.

This version replaces an earlier "Apple-Inspired Site Design System". That
framing was retired on 2026-08-21 for a specific reason, recorded so it is not
reintroduced: Apple's design philosophy is built for product surfaces, and an
academic homepage is a document. The old document had to forbid the natural
consequences of its own premise in four separate places — no product-marketing
hero, no marketing page, no branded splash area, no ornamental gradients — and
the premise still leaked through as a 96px page title. When a design system
spends that much of its length fencing out its own stated authority, the
authority is wrong. The old document also ranked its own Apple source last of
five in its conflict order while keeping it in the title, which was the tell.

What was kept from the old document: the source-conflict ordering, treating copy
and focus states and dark mode and responsive behavior as design rather than
polish, honest empty states, never signalling status by color alone, and phased
work with per-phase completion criteria. Those were good and are restated here.

## Thesis

> This site is a **document that makes one claim**. The claim is a research
> question stated in one sentence that a visitor can repeat in their own words
> after forty seconds. Everything else on the site is evidence for that claim.
>
> For the next several years the evidence cannot be the publication list, because
> at this career stage no publication list differentiates. So the site optimises
> for three things, in order: the claim arrives fast, the site stays visibly
> current, and nothing on it overstates what exists.

Three consequences follow immediately and are not negotiable inside this
document:

1. A page that looks impressive but leaves the visitor unable to restate the
   research question has failed, regardless of its craft.
2. Staleness is the primary failure mode, not ugliness. A design that is
   expensive to update will become false.
3. Visual volume must not exceed content volume. Thin content under large
   display type reads as thinner, not larger.

## Evidence base

Twelve comparable sites were read on 2026-08-21 and are listed under Sources.
Eight were established researchers; four were peers at or near this career
stage; one was a recent graduate now in a faculty post. The findings that
constrain this document:

- **Single column, sans-serif body, no card grids: 12 of 12.** No site had a
  hero. Only one used cards, and there they carried the author's own research
  figures rather than decoration. This is the strongest pattern in the survey.
- **Density tracks quantity.** The sites with the largest publication records are
  visibly dense; the sites with short or curated lists are airy. Airiness is what
  you use when you have little. It is not a licence for display type.
- **Dated news is near-universal, and its absence predicts staleness.** Eleven of
  twelve carried dated items; one senior site stamps an explicit last-updated
  date. The single surveyed peer site with no news section was also the only one
  whose most recent item was two years old.
- **A one-sentence statement is universal, but its kind tracks career stage.**
  Established researchers state a position. Peers state a keyword list. The one
  recent graduate who states a genuine position is the one who just placed well.
  This is the cheapest available differentiation precisely because peers do not
  do it.
- **Selectivity is the peer norm and short lists are not hidden.** Surveyed peers
  showed two, three, and six "selected" entries. None attempted completeness.
- **Some essentials are stage-dependent.** A portrait appeared on all four peer
  sites but only five of eight senior sites — the three senior sites without one
  belong to people whose names are already known, so the portrait is doing
  identification work that fame later replaces. Google Scholar appeared on three
  of four peer sites but only three of eight senior sites, for the same reason:
  it is the aggregator that proves a short record exists. A CV PDF appeared on
  most sites at both stages. ORCID appeared on one site out of twelve.
- **Serif body text: zero of twelve.** The print-document analogy governs
  structure, not typeface.
- **Using one's own research subject as visual language is a bet, not a norm.**
  One site in twelve does it, and that author's contribution is itself visual
  explanation. A researcher whose entire field is causal graphs has no diagram on
  his homepage. This remains available as differentiation but must be argued for
  case by case, not assumed.
- **The direct peer baseline is a template.** al-folio and academicpages dominate
  at this stage; one surveyed peer site credits al-folio in its footer. A
  hand-built site is therefore already differentiating, and its advantage is the
  ability to *not* inherit features that do not fit. The same surveyed site
  carries a keyboard search shortcut above two publications.

## Derived rules

### 1. The claim comes first

- The first screen states, in this order: name, current role and affiliation, and
  the one-sentence claim. Nothing may precede them.
- The claim is a sentence with a verb, not a list of fields. Keyword lists may
  appear *after* it as secondary structure, never in its place.
- The claim is one sentence. If it needs two, the second is a concrete example,
  not a qualification.

### 2. Document, not application

- One column. One reading measure of about 68 characters for prose; wider only
  for lists, tables, and figures.
- Sans-serif system stack for body text. Hierarchy comes from size, weight, and
  space — not from boxes, borders, shadows, or fills.
- Cards are permitted only when a card carries a figure or an independently
  linkable object. A card must never be the container for an ordinary section.
- No hero. No splash. No decorative graphic that does not carry information.

### 3. Visual volume is proportional to content volume

- Type sizes are capped by the scale in the Visual system section. The cap
  applies to every heading on every page, including page titles.
- A section with one entry is a sentence, not a section. Either feed it or fold
  it into an adjacent section.
- Whitespace is the tool for small content sets; large type is not.

### 4. Freshness is a design surface

- Every record, news item, and post carries a visible date.
- **Every dated list runs newest first.** News, projects, education, posts, and
  publications all reverse-chronological, without exception. A list that runs
  oldest-first buries the current state at the bottom, which defeats the whole
  point of showing dates. Where entries carry a status rather than a date —
  in progress, under review, published — the section keeps whatever order the
  source Markdown already uses, so the visible list and its source cannot
  disagree.
- The site keeps a dated news list. It is the mechanism by which maintenance
  becomes visible, and it is load-bearing rather than decorative.
- Content that has gone stale is labelled stale rather than quietly left. An
  explicit "not updated since X" is honest; an undated stale page is not.
- Adding a news item or a record must require editing one Markdown file and
  nothing else. Any structure that raises this cost is a design defect.

### 5. Honesty is part of the aesthetic

- Never invent or upgrade publication status, dates, affiliations, roles, or
  outcomes. Label in-progress, under review, preprint, non-archival, equal
  contribution, and corresponding authorship exactly.
- **The Causality Lab affiliation is current, not incoming.** Corrected by the
  owner on 2026-08-21: he is already a member of Sanghack Lee's Causality Lab at
  the SNU Graduate School of Data Science, and only the degree programme changes
  in September 2026. The former production site stated `incoming Ph.D. student`
  in four places and thereby framed the lab membership itself as not yet begun.
  State the current affiliation first and the degree transition second, as two
  separate facts.
- A CV, paper, code, or profile action appears only when its target exists. Never
  ship a "coming soon" affordance; omit the affordance instead.
- Prefer an omitted section to a section of placeholder copy. Text describing
  what a section could someday contain must never reach the public site.
- Do not add analytics, tracking, cookie banners, remote fonts, or third-party
  scripts without explicit approval.

### 6. Where character comes from

Restraint alone collapses into genericism, so the sources of character are named
here and are the designer's responsibility to actually use:

1. the one-sentence claim;
2. which few works appear first, and in what order — selection is voice;
3. how the surrounding prose and captions are written;
4. one deliberate typographic decision, owned and consistent;
5. at most one recurring visual motif, and only if it is argued for.

Character does not come from color, effects, or novel layout. It also does not
come from "the Hobbies page" alone; that was the old document's way of excusing
the design from having any.

### 7. Stage-appropriate essentials

Required now, because the survey shows it does identification work at this stage
while the name is not yet known: a portrait.

Contact and profile links, decided by the owner on 2026-08-21:

- **Contact and links are two separate things.** `Contact` labels the email
  address and nothing else — a CV and a LinkedIn profile are not ways to contact
  someone. The two links sit on their own line below, unlabelled, because `CV`
  and `LinkedIn` already name themselves and a label over them would add nothing.
  Both are repeated in the footer.
- No buttons anywhere. That leaves the theme toggle as the only control whose
  boundary is its sole indicator — so `--border-control` still matters, for that
  one case.
- **CV and LinkedIn are the only two links the site will carry.** They are part
  of the intended design and belong in any mockup; on the live site each appears
  once its target exists, per rule 5.
- **Google Scholar and GitHub are deliberately not used.** Recorded against the
  survey rather than in agreement with it: Scholar appeared on three of four peer
  sites and is the aggregator that proves a short record exists. The owner's
  decision stands; this note exists so the tradeoff is visible rather than
  looking like an oversight.
- ORCID is not used, which matches the survey — it appeared on one site of twelve.

The publication list is short and is not disguised, but no curation adjective
appears in the heading; see rule 9.

### 8. Normal web behavior

- Global navigation is visible, conventional, and shallow. Descriptive link
  labels only. Links open in the same tab.
- Links look interactive in more than one state and are distinguishable without
  relying on color alone.
- Semantic headings in document order, lists for collections, native links and
  buttons for actions. One visual treatment per repeated role.
- Preserve the Jekyll + Minima + Markdown publishing model. No frameworks, no
  build tooling beyond local preview, no JavaScript for visual polish.

### 9. Academic register

Headings and labels use academic vocabulary, not portfolio vocabulary. Raised by
the site owner on 2026-08-21: `Areas of work`, `Work`, and `Projects` read as a
design portfolio rather than a researcher's site.

Current heading set:

| Section | Heading |
|---|---|
| Research areas | Research interests |
| Papers, preprints, theses | Works |
| Funded and collaborative work | Research projects |
| Dated updates | News |
| Degrees | Education |

Headings state what the section is and nothing more. No `Selected`, no curation
adjective, no scope qualifier. Rule 7 already frames the list as selected in
prose where that needs saying; the heading is not the place for it.

Heading vocabulary is the owner's voice. Nothing in this table is inferred from
the site survey or proposed on design grounds — record what the owner asked for
and change it only when the owner says so.

Two related copy rules:

- **Author lists are written in full.** Surname-only abbreviation makes distinct
  coauthors indistinguishable — two of the current papers have two different
  Chos — and it drops the equal-contribution and corresponding-author markers.
  Wherever `*` or `†` appears, the footnote defining them appears too.
- Venue names are given in full on first use rather than abbreviated to an
  acronym a reader outside the subfield cannot expand.

## Visual system

Exact values may change after re-testing, but the roles and the measured floors
may not.

### Typography

- Body stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica,
  Arial, sans-serif`. Code stack: `ui-monospace, SFMono-Regular, Menlo, Consolas,
  monospace`. No self-hosted or remote fonts.
- **Exactly five type roles, each a token. Every `font-size` in the stylesheet
  resolves to one of them.** Values verified at a 1.21–1.29 ratio:

  | Token | rem | px | Role |
  |---|---|---|---|
  | `--type-title` | 2.25 | 36 | every `h1`, home and subpages alike |
  | `--type-section` | 1.75 | 28 | `h2` |
  | `--type-sub` | 1.375 | 22 | `h3` |
  | `--type-body` | 1.0625 | 17 | prose, list rows |
  | `--type-meta` | 0.875 | 14 | dates, labels, categories, footnotes |

- `h1` may be fluid but is capped: `clamp(1.75rem, 4vw, var(--type-title))`. The
  previous 5.8–6rem page titles are the specific thing this cap exists to
  prevent.
- Body line height about 1.6. Never Light, Thin, or Ultralight for reading text.
- **No eyebrows or section labels.** A section is introduced by its `h2` and
  nothing else. Decided 2026-08-21 from the demo: the five labels in use —
  Research, Selected, Current and past, Updates, Training — each restated the
  heading directly beneath it, which is the same duplication rule 5 and the
  Home architecture already forbid. There is no small-caps label role in this
  system, so the case that produced a fourth research area named `Explanation`
  above the name cannot recur.
- This bans **section** labels, not **field** labels. A short label naming what a
  value is — `Contact` above an email address — carries information the value
  alone does not, and is allowed. The test is whether the label restates a
  heading: `Selected` above `Works` does, `Contact` above an address does not.

### Color

- Semantic roles only: canvas, surface, surface-strong, text, muted, separator,
  control border, accent, accent-hover, accent-soft, on-accent, focus, code
  background. No raw values outside the token block.
- Neutral near-white canvas, near-black text, restrained gray surfaces, one blue
  accent. Color must not compete with content.
- **Two distinct boundary tokens.** A decorative separator between content blocks
  may be subtle. A border that is the *only* indicator of an interactive control
  must meet 3:1. Conflating them is what left the theme toggle and the secondary
  button at 1.34:1.

  | Token | Light | Dark | Measured |
  |---|---|---|---|
  | `--separator` | `#d8dbe0` | `#343841` | decorative only; no floor |
  | `--border-control` | `#828b98` | `#6a7280` | 3.33:1 / 3.45:1 light; 3.89:1 / 3.25:1 dark |

- Contrast floors: 4.5:1 normal text, 3:1 large text, 3:1 for any meaningful
  non-text UI boundary. Current text tokens measure 16.28:1, 6.02:1, and 6.65:1
  and are fine.
- Dark mode remaps roles; it does not invert the page. Define the full light
  palette on bare `:root`, then override under `prefers-color-scheme` and under
  an explicit `[data-theme]` so a manual toggle wins in both directions.
- Never communicate status, navigation state, or interaction by color alone.

### Spacing and geometry

- Spacing set `4, 8, 12, 16, 24, 32, 48, 64, 96px`. No one-off gaps without a
  recorded reason.
- Reading content sits in a narrow measure inside a wider shell with responsive
  side padding.
- At most three corner-radius roles: small controls, grouped surfaces, featured
  media. No pills for ordinary text.
- Prefer a separator over a shadow. Shadows only where elevation explains
  layering.

### Interaction and motion

- Touch targets at least 44×44px, or equivalent surrounding clickable area.
- Every interactive element has hover, active, and `:focus-visible` states.
- Motion explains feedback or state change only: color, opacity, small
  transforms, 120–220ms. Under `prefers-reduced-motion: reduce`, remove
  nonessential transitions. Never blinking, looping, or scroll-driven motion.

### Images and media

- A portrait is required at this career stage and is placed so it does not
  displace name, role, claim, or contact in the first screen.
- Prefer authentic portrait, research, and project material. No stock imagery.
- Preserve aspect ratio, give explicit dimensions where practical, compress
  appropriately. Meaningful images get useful alternative text; decorative images
  get empty alternative text.
- A figure from the author's own work is the strongest available image and is
  preferred over any decorative alternative — but see the note in the evidence
  base: making research diagrams the site's visual signature is a bet that must
  be argued, not assumed.

## Information architecture

**The public site is one page.** Decided 2026-08-21 from the demo. Every section
lives on the home page, and navigation entries are in-page anchors rather than
links to separate pages. Navigation links every substantive section: `Research
interests`, `Works`, `Research projects`, `News`, `Education`, and `Hobbies`;
the site name at the leading edge returns to the top. The blog is dormant; see
below.

This reverses M2, which replaced anchor scrolling with page-to-page navigation.
Recorded so the reversal is not mistaken for drift. Two reasons it is now the
better fit:

- The survey supports it at this content volume. Four of the twelve sites are a
  single page with anchors — one of them navigates entirely through a bracketed
  anchor row. The sites with genuine multi-page navigation carry lab, teaching,
  and group pages that this site does not have.
- One page is one file to maintain, which is what rule 4 asks for. Separate
  pages multiplied the places a fact could drift, and every drift this project
  has hit came from exactly that.

Two consequences follow:

- Navigation labels must match the section headings they point at, exactly. A
  `Publications` entry that lands on a section headed `Works` is a defect.
- Sections are ordered so the academic material comes first and Hobbies is last,
  per rule 6 and the Hobbies note below. There is no current-page state to show,
  since there is only one page; do not add scroll-spy JavaScript to invent one.
- The retired `/publications/` and `/hobbies/` routes are removed without
  redirects. The owner does not require backward compatibility for them.

Anchor targets carry `scroll-margin-top` so a jumped-to heading is not flush
against the viewport edge, and smooth scrolling is applied only under
`prefers-reduced-motion: no-preference`.

### Home

1. Name, role and affiliation, and the one-sentence claim.
2. Contact: the labelled email address, with CV and LinkedIn beneath the
   portrait. See rule 7.
3. Research interests as short structured support for the claim — not in place
   of it.
4. Works: the full list of papers, preprints, and the thesis.
5. Research projects with verified role and status.
6. Dated news.
7. Education.
8. Hobbies, last.
9. A quiet footer close.

The introduction may use the largest type role and generous space, but must stay
compact enough that substantive content is visible nearby. Sections 3 through 6
must not restate each other; a profile card that repeats the introduction
sentence for sentence carries no information and does not belong.

### Works

- A readable list, ordered as rule 4 requires. No card grid.
- Per entry, in order: status or venue, title, authors with contribution markers,
  then verified links.
- Author lists in full; see rule 9.
- **A paper under review is labelled `Under review` and does not name its
  venue.** The venue name is added once the outcome is known.

  This is a presentation choice, not a compliance requirement. Checked against
  the [NeurIPS 2026 Main Track
  Handbook](https://neurips.cc/Conferences/2026/MainTrackHandbook) on
  2026-08-21, which states that "the existence of non-anonymous preprints (on
  arXiv or other online repositories, **personal websites**, social media) will
  not result in rejection", and draws the line elsewhere: "while having a
  nonanonymized preprint alone is not a violation of the double-blind reviewing
  policy, aggressive advertising of papers under submission may be deemed a
  violation." A quiet list entry carrying title, authors, and status is not
  aggressive advertising, so the title and author list stay. Keeping the venue
  out is simply how a pending result is stated honestly.

  Non-archival workshop entries are unaffected: the same handbook permits "dual
  submissions to nonarchival workshops".
- One list only. When this was a separate page the same four entries appeared
  both there and on Home, which is the duplication the single-page architecture
  removes.
- A short list is stated plainly, never padded, and carries no curation
  adjective in its heading.

### Hobbies

- The last section on the page, not a separate page. Same type and color system,
  warmer prose permitted.
- Real content only. The four interests currently appear as names alone, because
  the live site's card descriptions are placeholder copy about what the cards
  could someday hold, and rule 5 forbids shipping that. Names alone is the
  honest state until real material exists.
- Imagery and richer treatment only once authentic material exists. This section
  must not dilute the academic material above it.

### Blog — dormant

The blog is out of the architecture as of 2026-08-21 by the site owner's
decision, and the three existing posts remain unpublished stubs. The Jekyll post
machinery, layouts, post typography, and the Writing Studio stay in place so it
can return without rework.

While dormant: no navigation anchor, no writing section, and no post counter. An empty archive behind a nav item advertises emptiness, which rule 5
forbids. Reinstating the blog is a deliberate decision, not a side effect of
publishing one post — the surveyed peer set contains no blogs at all, so this is
an open opportunity with a real maintenance cost, not an oversight to correct.

### Header and footer

- Header: name at the leading edge linking to the top, anchor nav at the
  trailing edge, simple mobile pattern. No current-page state; there is one page.
- Footer: the email contact path, CV and LinkedIn, and a short copyright.
- Sticky or translucent navigation must prove it improves navigation without
  hiding anchors or reducing contrast.

## Definition of done

### Positive criteria — the actual goals

These are the tests the design is trying to pass. All must hold.

1. A stranger in the field can restate the research question in their own words
   after forty seconds on Home.
2. A stranger outside the field can say what phenomenon is being studied.
3. The single strongest piece of work is reachable in one click from the top of
   Home.
4. Every dated item on the site is either current or visibly marked as not.
5. With CSS disabled the page loses its beauty but loses no information and no
   hierarchy.
6. Adding a news item, a record, or a publication is a one-file Markdown edit.
7. Every `font-size` in the stylesheet resolves to one of the five type tokens,
   and no rendered heading exceeds 36px.

### Floors — necessary, not sufficient

Failing any of these is a defect. Passing all of them is not success; criteria
1–7 decide that.

- Jekyll builds without errors and the GitHub Pages-compatible structure holds.
- No page-level horizontal scrolling at 320px or 200% zoom.
- Body copy at least 16px, reading measure near 68 characters, text contrast at
  WCAG AA, control boundaries at 3:1.
- All navigation and actions work by keyboard with visible focus; 44px touch
  targets where applicable.
- `prefers-reduced-motion` and system dark mode respected.
- No remote font, tracking script, framework, or decorative JavaScript.
- Content stays Markdown-centered and factual claims stay verified.

## Open decisions

### The claim sentence — decided 2026-08-21

Superseded 2026-08-21. Three earlier candidates — trust-centred,
decision-centred, interpretation-centred — were discarded once the owner stated
the actual through-line: the interest is **decision-making**, with an emphasis
on reliable use in complex real-world settings.

Final wording:

> I study how machine learning can support reliable decision-making in complex
> real-world settings.

The sentence is deliberately broader than policy alone. The three research
areas below explain what reliable support requires rather than turning the
claim itself into a keyword list. It becomes the single source for the site
description and the homepage introduction.

### The three research areas

Decided 2026-08-21: **causal inference, uncertainty quantification,
explainability.** Time-series analysis was removed as a peer area.

They are not three parallel interests. They are the three conditions an
ML-informed policy decision has to meet, which is why the claim above is a
question and these are its answer:

| Area | What it settles about an action |
|---|---|
| Causal inference | whether the action changes the outcome — validity |
| Uncertainty quantification | how wrong the estimate can be — safety |
| Explainability | why the model says this, and what defends the decision — justifiability |

Why time-series went, argued from the record rather than from taste:

- Of the five works, **two are explicitly attribution papers** — attribution is
  explainability, and the old list did not name that area at all.
- Time-series appears in **one** of the five, the thesis, and there it is the
  setting rather than the question. The owner's own reading: applications
  eventually have to account for time. That makes it a setting, so it now lives
  inside the causal inference description as longitudinal and time-varying
  treatment, exactly as conformal prediction lives inside uncertainty
  quantification rather than beside it.
- The framing also absorbs the off-policy evaluation work, which sat furthest
  from every earlier claim candidate and is now a direct instance.

Note for the record: the homepage eyebrow read `Causality · Uncertainty ·
Explanation`, and an earlier pass flagged `Explanation` as a stray fourth area to
delete. The eyebrow was right and the areas list was wrong. Prefer checking a
disagreement against the publication record before resolving it toward whichever
side appears more often.

### Research areas as a single source

The former site wrote the areas out in `_config.yml`, `index.md`, and
`publications.md`, and they drifted apart four times. They are now defined once
in `_config.yml` and rendered on Home, so the next drift is impossible rather
than merely corrected.

## Sources

Source order when guidance conflicts:

1. the thesis and verified visitor needs;
2. the surveyed evidence base below;
3. WCAG and familiar web conventions;
4. current accessibility and typography guidance;
5. individual taste.

Comparable sites read 2026-08-21. Established: [Sanghack
Lee](https://www.sanghacklee.me/), [Elias Bareinboim](https://causalai.net/),
[Aaditya Ramdas](https://web.stanford.edu/~aramdas/), [Ryan
Tibshirani](https://www.stat.berkeley.edu/~ryantibs/), [Anastasios
Angelopoulos](https://angelopoulos.ai/), [Andrej Karpathy](https://karpathy.ai/),
[Lilian Weng](https://lilianweng.github.io/), [Chris
Olah](https://colah.github.io/). Recent graduate: [Ying
Jin](https://ying531.github.io/). Peer stage: [Jungsoo
Kim](https://mephistonovel.github.io/), [Yesong
Choe](https://lovelyesong.github.io/), [Kyuseong
Choi](https://kyuseongchoi5.github.io/), [Jordan
Lekeufack](https://jordylek.github.io/).

Peer-stage template baseline:
[al-folio](https://github.com/alshedivat/al-folio), academicpages.

Accessibility reference: WCAG 2.2, in particular 1.4.3 text contrast and 1.4.11
non-text contrast.

Last source review: 2026-08-21.
