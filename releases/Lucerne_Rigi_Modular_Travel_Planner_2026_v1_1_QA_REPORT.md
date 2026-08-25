# Lucerne, Rigi and Central Switzerland Modular Travel Planner 2026 — QA report

Release: **v1.1 · 2026-08-24**  
Verdict: **PASS — release-ready**

This is an additive Lucerne v1.1 release. The accepted v1.0 files remain intact and are recorded as the canonical predecessor lineage.

## Compatibility and expansion gates

- The modular builder remains exactly L1-L7: 7 core dossiers and 7 builder choices.
- Each L1-L7 module-section outerHTML hash matches the accepted Lucerne v1.0 predecessor.
- The separate catalogue contains 41 unique LX entries; no LX entry is selectable as a core module.
- P001-P021 match every v1.0 photo identity/provenance record; P022-P030 are additive.
- All 101 Lucerne v1.0 external-directory URLs remain present in v1.1.

## Release checks

- Interactive HTML: 19,675 words, 30 stable photo IDs, and 206 exact external-directory targets.
- PDF: 90 A4 pages, 20,209 extracted words, 206 external URLs, and 71 valid internal destinations.
- Browser QA passed at desktop, 390 px and 320 px with no document overflow, broken images, broken fragments, duplicate element IDs or console errors.
- Every Lucerne PDF page was rendered at 200 dpi and visually reviewed; smallest recorded text was 6.49 pt.
- Live link audit: hard failures=0; access controlled=3, rate limited=5, reachable=198.

## Independent review team

1. Official Lucerne 2026 excursion-discovery auditor — Jason - discovery-landscape subagent (PASS)
2. Central Switzerland regional-operator source auditor — Huygens - final-source subagent, accepted by release orchestrator (PASS_WITH_NOTES)
3. Transport, seasonality and safety verifier — Hypatia - transport-and-safety subagent (PASS)
4. Lucerne v1.0 compatibility and lineage auditor — Plato - predecessor-lineage subagent (PASS)
5. Excursion-tiering and day-trip feasibility reviewer — Wegener - final-tiering subagent (PASS)
6. Image-rights and stable-photo-ID auditor — lucerne_final_photos - independent photo subagent (PASS)
7. Renderer, accessibility and interaction auditor — Release orchestrator - versioned Playwright matrix (PASS)
8. Every-page PDF visual reviewer — lucerne_final_pdf - independent PDF subagent (PASS)
9. Desktop and mobile layout reviewer — lucerne_mobile_quick - independent responsive subagent (PASS)
10. Package, checksum and external-link reviewer — lucerne_final_package - independent release subagent (PASS_WITH_NOTES)

## Operational boundary

Timetables, fares, closures, weather, snow, lifts, boats, ticket inventory and access restrictions remain live conditions. The planner marks booking and feasibility gates; exact journeys must be regenerated for the selected travel date.

## Machine-readable evidence

The companion QA evidence JSON contains the browser assertions, PDF-page checks, link audit, compatibility regression results and review register. The release manifest and SHA256SUMS bind the package to this exact Lucerne release.
