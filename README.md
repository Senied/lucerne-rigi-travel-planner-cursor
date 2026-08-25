# Lucerne & Central Switzerland Travel Planner

A responsive travel planner for Lucerne, Lake Lucerne, Rigi, Pilatus, Titlis, Stoos, Stanserhorn and Bürgenstock.

## Current release: v1.1

- [Open the interactive guide](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.html)
- [Open the 90-page PDF](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.pdf)
- [Download the complete ZIP bundle](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_bundle.zip)

Release records:

- [Release manifest](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_RELEASE_MANIFEST.json)
- [Photo manifest](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_photo_manifest.json)
- [QA report](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_QA_REPORT.md)
- [QA evidence](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_QA_EVIDENCE.json)
- [SHA-256 checksums](releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1_SHA256SUMS.txt)

## Open locally

```bash
cd lucerne-rigi-modular-travel-planner-site
python -m http.server 18902 --bind 127.0.0.1
```

Then visit [http://127.0.0.1:18902/](http://127.0.0.1:18902/).

The exact canonical v1.1 artifacts live in `releases/`. The `guide/` directory is an unchanged compatibility mirror of the v1.1 HTML and PDF, with no presentation rewrite layered over the guide. The accepted v1.0 release remains preserved in `releases/` and is available from the site under “Earlier edition.”

Run `powershell -ExecutionPolicy Bypass -File scripts/verify-site.ps1` for the repeatable static checks.
