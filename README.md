# Lucerne & Central Switzerland Travel Planner

A responsive trip-planning website and full guide for Lucerne, Lake Lucerne, Rigi, Pilatus, Titlis, Stoos, Stanserhorn, Bürgenstock and additional Central Switzerland excursions.

## Current traveler files

- [Website](index.html)
- [Interactive guide](guide/index.html)
- [Printable guide](guide/Lucerne_Central_Switzerland_Travel_Guide_2026.pdf)

The website presents the current guide without technical labels or version language. Earlier editions remain available through the quiet “Earlier editions” section and are preserved in `releases/`.

## Open locally

```powershell
python -m http.server 18902 --bind 127.0.0.1
```

Then open `http://127.0.0.1:18902/`.

The current guide is generated from the preserved expanded source by `scripts/build-traveler-guide.py`. Run `powershell -ExecutionPolicy Bypass -File scripts/verify-site.ps1` for repeatable static checks.
