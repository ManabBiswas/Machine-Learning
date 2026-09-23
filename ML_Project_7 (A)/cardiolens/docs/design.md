# CardioLens — Design System

Status: **approved for build**. This is the source of truth for the
multi-page redesign — colors, type, motion, and page structure. Update
this file first if any of these decisions change; don't let the code
drift silently ahead of it.

---

## 1. Design principles

1. **Clinical instrument, not marketing gloss.** Numbers read like lab
   equipment output (monospace), structure reads like a real tool. The
   landing pages exist to earn trust in the tool, not to be a SaaS
   brochure.
2. **Motion is restrained and asymmetric.** A heartbeat isn't a sine
   wave — it's lub-DUB, pause, repeat. Every recurring animation in
   this app should reference that rhythm rather than generic
   ease-in-out loops.
3. **Two themes, two moods — not one theme inverted.** Dark and light
   mode use different accent hue families entirely (see §2). Both must
   independently feel premium and intentional; light mode is not an
   afterthought.
4. **Respect `prefers-reduced-motion` everywhere** — hero draw-in,
   scroll reveals, the scroll rail, counters, hover tilt. No exceptions.
5. **The tool is still the point.** However polished the new pages get,
   the assessment form and result panel keep working exactly as they
   do today — this is additive, not a rewrite of the working core.

---

## 2. Color system

### Dark — "Night Signal"
Cyan/teal signal against near-black ink, coral pulse for risk. This is
the palette already shipped in `index.css`; kept as-is.

| Token | Value | Use |
|---|---|---|
| `--bg` | `#070b12` | page background |
| `--surface` | `#0e1520` | panels |
| `--surface-raised` | `#131b29` | elevated panels, cards |
| `--border` / `--border-strong` | `#1e2a3c` / `#2a3a52` | dividers |
| `--text` / `--text-muted` | `#e7edf5` / `#8a97ac` | copy |
| `--signal` | `#35d0c0` | primary accent, low risk, links, active states |
| `--signal-2` | `#5b7fff` | secondary accent, gradients |
| `--pulse` | `#ff6b5b` | high risk, alerts |
| `--caution` | `#f5a623` | moderate risk |

### Light — "Day Clinic"
Deliberately a **different hue family**, not a lightened version of the
above: warm paper background, deep indigo primary, muted gold
secondary, clinical red for risk. Reads editorial/medical-premium
rather than "dark mode with the brightness turned up."

| Token | Value | Use |
|---|---|---|
| `--bg` | `#f7f5f1` | warm paper background |
| `--surface` | `#ffffff` | panels |
| `--surface-raised` | `#ffffff` | elevated panels (shadow does the lifting, not color) |
| `--border` / `--border-strong` | `#e3ddd1` / `#cfc6b4` | dividers |
| `--text` / `--text-muted` | `#1c1a15` / `#6b6459` | copy |
| `--signal` | `#3450a3` | primary accent, low risk, links, active states |
| `--signal-2` | `#c98a2c` | secondary accent, gradients (muted gold, not blue) |
| `--pulse` | `#c4432e` | high risk, alerts |
| `--caution` | `#b5790f` | moderate risk |

Both themes keep the same **token names** (`--signal`, `--pulse`,
`--caution`, etc.) so components never branch on theme — only the CSS
custom property values change per `[data-theme]`. This is already the
pattern in `index.css`; we're extending the palette, not the mechanism.

Risk-tier color mapping stays theme-agnostic at the component level:
`low → var(--signal)`, `moderate → var(--caution)`, `high → var(--pulse)`.

---

## 3. Typography

Unchanged from the current build — this already reads premium and is
staying:

- **Display / headings:** Sora (600–700)
- **Body / UI:** Inter (400–600)
- **Data / numeric readouts:** IBM Plex Mono — used for every real
  number (vitals, gauge %, stat strip, history table, scroll-counted
  stats). This is a meaningful distinction, not decoration — it marks
  "this number came from real computation."

New landing pages introduce larger display sizes for the hero (fluid
`clamp()` sizing, ~48–72px) — same family, no new fonts.

---

## 4. Motion system

### The heartbeat curve
Every "pulse" animation (hero heart, scroll-rail blip, gauge glow) uses
an asymmetric easing that mimics lub-DUB rather than a symmetric sine:
quick contraction, brief hold, slower release, longer rest. Implemented
as a custom cubic-bezier / anime.js easing, defined once and reused —
not hand-tuned per component.

### Hero heart (2D SVG)
- Anatomical-ish silhouette path, stroke-drawn on first load
  (`stroke-dashoffset` animation via anime.js), ~1.8–2.2s.
- After draw-in, continuous idle pulse on the heartbeat curve.
- Soft layered blur/glow behind the path for depth — no 3D mesh.
- Glow color shifts through `--signal → --caution → --pulse` as the
  "How it works" section scrolls past, foreshadowing the risk-tier
  language used later in the real tool.

### Scroll rail (persistent, cross-page)
- Thin vertical line, desktop only (hidden below `md` breakpoint —
  replaced by a simple top progress bar on mobile instead of forcing
  the rail into a cramped viewport).
- Traces down as the page scrolls (`stroke-dashoffset` mapped to
  scroll progress, not JS-animated frame-by-frame — CSS/scroll-timeline
  where supported, rAF-throttled fallback otherwise).
- Small blip marker at current position; blip color follows the same
  section-based tint as the hero heart, so the rail visually continues
  the hero's language down the whole page.
- Lives in the shared page layout (see architecture.md), not
  reimplemented per route.

### Scroll reveals
- Sections fade/rise in on entry (`opacity 0→1`, `y: 16px→0`), staggered
  by ~60–80ms per child — short and subtle, not a slideshow.
- Stat numbers (accuracy, F1, totals) count up from 0 on first reveal
  only — never re-trigger on repeat scroll past.

### Hover / interaction
- **Magnetic buttons:** primary CTAs shift a few px toward the cursor
  within a small radius, spring back on leave.
- **Cursor-following border glow:** panels (form, result, stat strip)
  get a soft radial highlight at the cursor position via a CSS
  variable updated on `pointermove`, not a JS-repainted gradient.
- **Card tilt:** subtle (3–5°) perspective tilt on stat/history rows,
  capped and damped — never full 3D-card-flip territory.
- All hover effects: same intensity in both themes, colors swap via
  tokens automatically.

### Page transitions
- Route changes cross-fade + slight vertical settle (~200ms), not a
  hard cut — reinforces "one continuous instrument," not separate
  disconnected pages.

---

## 5. Component inventory (new + reused)

**Reused as-is:** `PatientForm`, `ResultPanel`, `RiskGauge`,
`DriverBars`, `HistoryTable`, `NumberField`, `SelectField`,
`ThemeContext`.

**New:**
- `AppShell` — persistent layout: `TopNav` (now with route links) +
  `ScrollRail` + page `<Outlet>` + `Footer`.
- `Hero` — 2D SVG heart + headline + scroll cue.
- `ScrollRail` — the persistent motif described above.
- `HowItWorks` — 3-step scroll-revealed sequence.
- `StatShowcase` — larger, animated version of the existing
  `StatStrip` for the landing/about pages (the compact `StatStrip`
  stays as-is for the in-app header).
- `MagneticButton`, `TiltCard`, `GlowPanel` — small reusable
  interaction primitives, used across both new and existing panels so
  the whole app feels like one hover language, not landing-page-only
  polish.

---

## 6. What we are explicitly not doing

- No 3D/WebGL — decided in favor of 2D SVG for the hero (see chat log
  in `/areas/cardiolens.md` memory for the reasoning).
- No generic gradient-blob backgrounds or glassmorphism-everywhere —
  flagged as the cliché to actively avoid; confirm with
  `design:design-critique` before shipping.
- No new fonts, no new icon library beyond what's already in use —
  keep the bundle honest.
