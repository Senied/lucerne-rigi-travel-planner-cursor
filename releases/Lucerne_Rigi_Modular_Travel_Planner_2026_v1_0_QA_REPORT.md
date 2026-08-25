# Lucerne, Rigi and Central Switzerland Modular Travel Planner 2026 — QA report

Release: **v1.0 · 2026-08-24**  
Verdict: **PASS — release-ready**

This is the first release in this guide's own additive lineage. It does not replace or overwrite the accepted Foroglio guide.

## What was verified

- Interactive HTML: 9,327 words, 7 standalone modules, 7 accommodation dossiers, 21 stable photo IDs and 101 exact external-directory targets.
- PDF: 57 A4 pages, 9,571 extracted words, 101 external URLs, 52 valid internal destinations, footers on every page, no blank pages and no outside-page blocks.
- Browser QA: desktop, 390 px and 320 px; zero document overflow, no broken images/fragments/duplicate IDs, no console errors, and passing search, module builder, source filter, budget, checklist and accessible lightbox tests.
- PDF typography: smallest recorded text 6.49 pt; every page rendered at 200 dpi and visually inspected.
- Live external-link audit: 101 targets, hard failures=0; rate limited=5, reachable=96.
- Photo provenance: every image has a stable ID, creator, licence, Commons source, local binary hash and occurrence list; all binaries are unique.

## Independent review team

Ten focused review roles were used, with independent content, data, rendering, visual and package checks:

1. Lucerne primary-source and operations researcher
2. Milan primary-source and operations researcher
3. Accommodation, safety and image-rights auditor
4. Lucerne dataset and internal-consistency auditor
5. Milan dataset and internal-consistency auditor
6. Renderer, accessibility and preflight auditor
7. Lucerne independent release reviewer
8. Milan independent release reviewer
9. Every-page visual and interaction reviewer
10. Package, checksum and external-link reviewer

## Corrections closed before release

- Repaired the low-contrast safety cards and protected route/comparison tables from weak page breaks.
- Replaced P017 with a Commons-verified Klingenstock-Fronalpstock ridge photograph from Canton Schwyz.
- Recaptioned P013 precisely as Mount Titlis seen from Gross Spannort.
- Retained complete 320 px navigation labels in a two-row scrollable section panel.

## Link-audit interpretation

HTTP 2xx/3xx responses are recorded as reachable. HTTP 429 responses are retained as rate-limited rather than declared broken. Session-based operator checkouts may reject automated probes; where this occurred, the first-party operator page that publishes the checkout was separately verified and recorded in the evidence JSON.

## Operational boundary

Timetables, fares, closures, weather, lift/boat operation, ticket inventory and room availability remain live conditions. The guide deliberately labels planning anchors, booking gates, live-status links and no-go conditions; users must regenerate exact journeys and recheck operators for their selected date.

## Machine-readable evidence

The companion QA evidence JSON preserves the full browser assertions, PDF-page checks, per-link audit results, correction log and review-role register. The release manifest and SHA256SUMS file bind the packaged files to this exact release.
