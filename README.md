# Whose Words? — handoff notes

An interactive perspective piece about communicating through a speech brain–computer
interface (BCI). The viewer assembles a reply one word at a time, is offered an
"almost right" AI completion, and must choose between accepting a near-miss (fast) or
correcting it (truer, but it drains an energy meter). It closes with honest reflection
and a grounded, cited facts panel.

> The interactive part is an **evocation, not a real BCI**. No brain signals are involved.
> Real research and figures are cited in the "What is real / what isn't" panel.

## Files

- **`Whose Words.dc.html`** — the SOURCE. Read and edit this one.
- **`index.html`** — the self-contained ~1MB build (fonts + runtime inlined), renamed from
  `Whose Words.html` so it deploys as a site root (Netlify / GitHub Pages serve `index.html`).
  Runs offline by double-clicking. Do NOT hand-edit; it's generated from the source — after a
  rebuild, copy the bundler's `Whose Words.html` output over `index.html`.
- **`support.js`** — the small runtime the source depends on (see below). Don't edit.

## How the source file is structured (read this first)

`Whose Words.dc.html` is a **"Design Component" (DC)**, not plain HTML. It has three parts:

1. **Template** — the markup between the `<x-dc>` … `</x-dc>` tags. It uses a light syntax:
   - `{{ name }}` — a value supplied by the logic class (dotted paths only, no expressions).
   - `<sc-if value="{{ flag }}">…</sc-if>` — conditional block.
   - `<sc-for list="{{ arr }}" as="item">…</sc-for>` — repeat block.
   - `style-hover="…"`, `style-focus="…"` — pseudo-state inline styles.
2. **Logic** — the `class Component extends DCLogic { … }` block. Plain JS, React-class-style
   (`state`, `setState`, lifecycle). `renderVals()` returns every value/handler the template reads.
3. **Props metadata** — the JSON on the `<script data-dc-script>` tag (the tweakable knobs:
   `startEnergy`, `openingEffort`, `insistCost`).

`support.js` is what turns those three parts into a live component in the browser. If you
just want to see it run, open `index.html` instead — no runtime needed.

## Where the motion lives

All motion is **computed in real time from logic**, not frame-to-frame tweening:

- **`startTurn(i)`** — the silence/latency beat: waits, then starts a live seconds timer.
- **`animateResolve(word, color, done)`** — the signal-to-language motif: cycles random
  glyphs, then settles into the word. Latency **grows as energy drops**:
  `latency = 760 + (100 − energy) × 9`, capped at 2200ms (so a low battery literally slows
  the conversation). Reduced-motion skips the flicker.
- **`acceptOffer()`** — the AI's fast "resolve", deliberately quicker than your own decoding.
- **`decodeNext()` / `insistOffer()`** — the slow lane and the fatigue-gated refusal.
- CSS `@keyframes ww-breathe` / `ww-rise` are in the `<helmet>` block at the top of the template.
- A **reduced-motion** toggle (top-right) removes all animation; it also respects the OS
  `prefers-reduced-motion` setting on load.

## The data

The conversation is the **`TURNS`** array near the top of the logic class: each entry has
`heard` (what your daughter says), `intent` (your true sentence), `forced` (how many words
you decode before the AI offers to finish), and `ai` (the near-miss completion). Edit that
array to change the script.

## Common tasks

- **Change the script/copy** → edit the `TURNS` array (logic) and the intro/reflection strings.
- **Tune the bargain** → `startEnergy`, `openingEffort`, `insistCost` (props JSON, read via
  `this.props.x ?? default`).
- **Port to a normal React / vanilla app** → the logic class is already React-class-shaped;
  lift `state` + `renderVals()` into a component and translate the `<sc-if>`/`<sc-for>`/`{{ }}`
  template into JSX. Drop `support.js` once ported.

## Accessibility (part of the subject — keep it)

WCAG-AA contrast, full keyboard operation, visible focus rings, `role="meter"` + `aria-label`
on the meters, `aria-live` on the composed reply, and the reduced-motion toggle. Preserve these.
