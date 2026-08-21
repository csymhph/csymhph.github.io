# M4.2 rebuild demo

Working demos for M4.2, the thesis-driven site rebuild. Not production
templates, and not published: `design-demo` is in `_config.yml`'s exclude list,
so nothing here reaches the public site.

The M2 prototypes in the parent directory are a separate, earlier record. This
subdirectory exists so they are not overwritten.

## Files

| File | What it is |
| --- | --- |
| `index.html` | Current demo. Single page, six anchored sections, the decision-framed claim, and the causal / uncertainty / explainability areas. |
| `local-preview.html` | UTF-8 local preview wrapper for `index.html`; open it through a local static server. |
| `variant-marginal-headings.html` | Rejected layout: section headings set in a left margin rail. Kept because the reasoning against it is worth seeing — the rail sits empty beside long lists, so it distributes the emptiness rather than removing it. |
| `variant-pre-decision-framing.html` | The state before the research areas changed: the trust-centred claim, and time-series analysis as the third area instead of explainability. |

## What the demo is for

It applies M4.2 phases B, D, E, and F together so the design can be judged before
any of it touches the live site. The appendix at the bottom of each page states
what it is testing and what is still unsettled.

Two things in `index.html` are placeholders and must not be copied to the live
site as they stand:

- the portrait, an empty slot;
- the three hobby descriptions, which say on their face that they are
  placeholders.

The two News entries were also written for the demo. One date has already been
corrected once; verify both before they go live.

## Opening these locally

These files are in Artifact format: page content only, with no `<!doctype>`,
`<html>`, `<head>`, or `<body>` wrapper, because the Artifact host supplies that
skeleton at publish time. They still open directly in a browser, but there is no
`<meta charset>`, so if the em dashes and middots render as mojibake, add
`<meta charset="utf-8">` at the top of a local copy rather than editing these —
keeping them byte-identical to what was published means republishing the same
path updates the same Artifact URL and preserves its version history.

Published at `https://claude.ai/code/artifact/e6239c7e-d13a-419d-a5f7-218020c9bb3b`
(private to the owner's account).

For the local preview server, open `local-preview.html`. It fetches the
byte-identical Artifact source and renders it as UTF-8 without modifying the
published demo file.
