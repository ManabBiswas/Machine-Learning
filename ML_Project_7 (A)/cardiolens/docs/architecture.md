# CardioLens — Multi-Page Architecture

Status: **approved for build**. Companion to `design.md`. This covers
routing, page structure, and how new pages share state/layout with the
existing working tool.

---

## 1. Routing

Adding `react-router-dom` (v6). One shared layout (`AppShell`) wraps all
routes so `TopNav`, `ScrollRail`, `ThemeProvider`, and `Footer` persist
across navigation instead of remounting per page.

```
/                  Home        — hero, how it works, model transparency, CTA
/assess            Assess      — the existing tool (PatientForm + ResultPanel)
/insights          Insights    — expanded history/dashboard (grows HistoryTable)
/about             About       — methodology, dataset, label-convention note,
                                  notebook summary, limitations/disclaimer
```

`/assess` is the existing `App.tsx` content, extracted as-is into a
route — no functional changes, just relocated. This is the one page
that must not regress; everything else is new surface area around it.

## 2. Why these four pages (and not more)

- **Home** exists to earn trust before asking for real inputs —
  explains what the tool does and shows the model is honest about its
  own accuracy, before the person starts typing vitals.
- **Assess** is unchanged in function — the whole reason the rest of
  this exists.
- **Insights** gives the "recent predictions" data a real home instead
  of being a strip at the bottom of the tool page — room for the
  totals/high-risk-count stats to breathe and for future charting.
- **About** is where the label-inversion fix and methodology live —
  genuinely useful for a placement portfolio: it shows you can find and
  document a real bug, not just style a form. Pulls directly from
  `notebooks/` and `reports/metrics.json`.

No auth, no user accounts, no settings page — out of scope, would add
complexity with no current requirement.

## 3. Shared layout and state

```
<ThemeProvider>
  <BrowserRouter>
    <AppShell>              -- TopNav + ScrollRail + Footer, persistent
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/assess" element={<Assess />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </AppShell>
  </BrowserRouter>
</ThemeProvider>
```

- `usePrediction` and `useDashboardData` stay page-local to `Assess` /
  `Insights` respectively — no new global state manager needed. The API
  layer (`src/api/`) is already the single source of truth; pages just
  call into it.
- `ScrollRail` reads scroll position via a small shared hook
  (`useScrollProgress`), mounted once in `AppShell`, so it's one
  implementation across all four pages rather than four copies.
- Route change → `ScrollRail` resets progress and re-measures the new
  page's height; no state leaks between pages.

## 4. File structure additions

```
frontend/src/
├── pages/
│   ├── Home.tsx
│   ├── Assess.tsx        (existing App.tsx content, relocated)
│   ├── Insights.tsx
│   └── About.tsx
├── components/
│   ├── layout/
│   │   ├── AppShell.tsx
│   │   ├── TopNav.tsx     (replaces TopBar — adds route links)
│   │   ├── ScrollRail.tsx
│   │   └── Footer.tsx
│   ├── landing/
│   │   ├── Hero.tsx
│   │   ├── HowItWorks.tsx
│   │   └── StatShowcase.tsx
│   ├── interaction/
│   │   ├── MagneticButton.tsx
│   │   ├── TiltCard.tsx
│   │   └── GlowPanel.tsx
│   └── (existing form/results/history/layout — unchanged)
├── hooks/
│   ├── useScrollProgress.ts   (new)
│   └── (existing usePrediction, useDashboardData — unchanged)
└── App.tsx                    (becomes the router + AppShell mount only)
```

Nothing in `api/`, `types/`, or `context/` needs to change — this
redesign is purely additive at the routing/component layer.

## 5. Deployment impact

Still a static SPA — Vercel/Netlify build is unaffected. One addition
needed: `vercel.json` rewrite already handles client-side routing
(`"rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]`),
so deep links like `/insights` won't 404 on refresh. Netlify would need
the equivalent `_redirects` file if we ever move off Vercel — noting
this now so it isn't a surprise later.

## 6. Build order

1. Introduce `react-router-dom`, extract current `App.tsx` into
   `pages/Assess.tsx` behind `/assess` — verify zero regression before
   adding anything new (this is the checkpoint that matters most).
2. `AppShell` + `TopNav` + `Footer` — shared chrome, both themes.
3. `ScrollRail` + `useScrollProgress` — cross-page motif from
   `design.md` §4.
4. `Home` — hero (SVG heart), `HowItWorks`, `StatShowcase`, CTA into
   `/assess`.
5. `Insights` — expanded history page.
6. `About` — methodology / label-fix writeup, pulling from
   `reports/metrics.json` and the notebooks.
7. Interaction primitives (`MagneticButton`, `TiltCard`, `GlowPanel`)
   applied across both new and existing pages.
8. Light theme pass — confirm "Day Clinic" palette end-to-end, not just
   spot-checked.
9. `design:design-critique` pass on the full site, both themes.
