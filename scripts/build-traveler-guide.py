from __future__ import annotations

import base64
import io
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "releases" / "Lucerne_Rigi_Modular_Travel_Planner_2026_v1_1.html"
GUIDE = ROOT / "guide" / "index.html"
ARCHIVE = ROOT / "releases" / "Lucerne_Central_Switzerland_Travel_Guide_2026_v1_2.html"
PHOTO_DIR = ROOT / "guide" / "assets" / "photos"

PHOTO_SLUGS = {
    "P001": "chapel-bridge",
    "P002": "lucerne-old-town",
    "P003": "musegg-wall",
    "P004": "lion-monument",
    "P005": "lake-lucerne",
    "P006": "rigi-kulm",
    "P007": "rigi-railway",
    "P008": "rigi-kaltbad",
    "P009": "weggis-waterfront",
    "P010": "pilatus-summit",
    "P011": "pilatus-railway",
    "P012": "pilatus-cableway",
    "P013": "titlis-mountain",
    "P014": "titlis-rotair",
    "P015": "engelberg-village",
    "P016": "stoos-funicular",
    "P017": "fronalpstock-ridge",
    "P018": "burgenstock",
    "P019": "hammetschwand-lift",
    "P020": "stanserhorn-cabrio",
    "P021": "stans-village",
    "P022": "seelisberg",
    "P023": "altdorf-tell-monument",
    "P024": "einsiedeln-abbey",
    "P025": "zug-old-town",
    "P026": "melchsee-frutt",
    "P027": "brienzer-rothorn",
    "P028": "glasi-hergiswil",
    "P029": "devils-bridge",
    "P030": "bern-old-town",
}

DAY_IDS = {
    "module-builder": "trip-builder",
    "module-l1": "day-lucerne",
    "module-l2": "day-rigi",
    "module-l3": "day-pilatus",
    "module-l4": "day-titlis",
    "module-l5": "day-stoos",
    "module-l6": "day-stanserhorn",
    "module-l7": "day-burgenstock",
}

DAY_NAMES = {
    "L1": "Lucerne",
    "L2": "Rigi",
    "L3": "Pilatus",
    "L4": "Titlis",
    "L5": "Stoos",
    "L6": "Stanserhorn",
    "L7": "Bürgenstock",
}


TRAVEL_JS = r"""(() => {
  "use strict";

  const guideSlug = document.documentElement.dataset.guide || "lucerne-guide";
  const storage = {
    get(key) { try { return window.localStorage.getItem(key); } catch (_) { return null; } },
    set(key, value) { try { window.localStorage.setItem(key, value); } catch (_) {} },
    remove(key) { try { window.localStorage.removeItem(key); } catch (_) {} },
  };

  const sidebar = document.querySelector(".sidebar");
  const guideNav = sidebar?.querySelector("nav");
  const menuToggle = document.querySelector(".guide-menu-toggle");
  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!sidebar || !menuToggle || !guideNav) return;
    sidebar.classList.remove("nav-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.textContent = "Menu";
    if (restoreFocus) menuToggle.focus();
  };
  const openMenu = () => {
    if (!sidebar || !menuToggle || !guideNav) return;
    sidebar.classList.add("nav-open");
    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.textContent = "Close";
    requestAnimationFrame(() => guideNav.querySelector("a")?.focus());
  };
  menuToggle?.addEventListener("click", () => {
    if (menuToggle.getAttribute("aria-expanded") === "true") closeMenu({ restoreFocus: true });
    else openMenu();
  });
  guideNav?.querySelectorAll("a").forEach(link => link.addEventListener("click", () => closeMenu()));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && menuToggle?.getAttribute("aria-expanded") === "true") {
      closeMenu({ restoreFocus: true });
    }
  });
  document.addEventListener("pointerdown", event => {
    if (menuToggle?.getAttribute("aria-expanded") !== "true") return;
    if (!sidebar?.contains(event.target)) closeMenu();
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 1100) closeMenu();
  });

  const search = document.querySelector("#guideSearch");
  const searchStatus = document.querySelector("#searchStatus");
  const searchable = [...document.querySelectorAll("main > section[id]")];
  const updateSearch = () => {
    const term = search?.value.trim().toLowerCase() || "";
    let matches = 0;
    searchable.forEach(section => {
      const hit = !term || section.textContent.toLowerCase().includes(term);
      section.hidden = !hit;
      if (hit) matches += 1;
    });
    if (searchStatus) searchStatus.textContent = term ? `${matches} sections found` : "";
  };
  search?.addEventListener("input", updateSearch);
  search?.addEventListener("keydown", event => {
    if (event.key === "Escape" && search.value) {
      search.value = "";
      updateSearch();
    }
  });

  const dayPlanInputs = [...document.querySelectorAll(".module-card input[type='checkbox']")];
  const builderDays = document.querySelector("#builderDays");
  const builderText = document.querySelector("#builderText");
  const updateBuilder = () => {
    const selected = dayPlanInputs.filter(input => input.checked);
    const days = selected.reduce((total, input) => total + Number(input.dataset.days || 1), 0);
    if (builderDays) builderDays.textContent = `${days} day${days === 1 ? "" : "s"} selected`;
    if (builderText) {
      builderText.textContent = selected.length
        ? selected.map(input => input.dataset.title || input.value).join(" · ")
        : "Choose one or more day plans to build a shorter trip.";
    }
  };
  dayPlanInputs.forEach(input => input.addEventListener("change", updateBuilder));
  document.querySelector("#builderClear")?.addEventListener("click", () => {
    dayPlanInputs.forEach(input => { input.checked = false; });
    updateBuilder();
  });

  document.querySelectorAll(".check input[type='checkbox']").forEach((input, index) => {
    const key = `${guideSlug}-check-${input.dataset.key || index}`;
    input.checked = storage.get(key) === "1";
    input.addEventListener("change", () => storage.set(key, input.checked ? "1" : "0"));
  });
  document.querySelector("#resetChecks")?.addEventListener("click", () => {
    document.querySelectorAll(".check input[type='checkbox']").forEach((input, index) => {
      input.checked = false;
      storage.remove(`${guideSlug}-check-${input.dataset.key || index}`);
    });
  });

  const budgetInputs = [...document.querySelectorAll(".budget input[type='number']")];
  const budgetTotal = document.querySelector("#budgetTotal");
  const updateBudget = () => {
    const total = budgetInputs.reduce((sum, input) => sum + (Number(input.value) || 0), 0);
    const decimals = Math.abs(total - Math.round(total)) > 0.0001 ? 2 : 0;
    if (budgetTotal) budgetTotal.textContent = `${total.toFixed(decimals)} ${budgetTotal.dataset.currency || ""}`.trim();
  };
  budgetInputs.forEach(input => input.addEventListener("input", updateBudget));
  updateBudget();

  const photos = window.TRAVEL_PHOTOS || {};
  const photoKeys = Object.keys(photos);
  const printMode = new URLSearchParams(window.location.search).has("print");
  document.querySelectorAll("img[data-photo-src]").forEach((img, index) => {
    const photo = photos[img.dataset.photoSrc];
    if (!photo) return;
    img.src = printMode ? photo.printSrc : photo.src;
    if (!printMode) {
      img.srcset = photo.srcset;
      img.sizes = img.closest(".photo-atlas") ? "(min-width: 900px) 34vw, 90vw" : "(min-width: 900px) 42vw, 90vw";
    }
    img.loading = printMode || index < 4 ? "eager" : "lazy";
    img.decoding = "async";
  });
  document.querySelectorAll("[data-cover-photo]").forEach(cover => {
    const photo = photos[cover.dataset.coverPhoto];
    if (photo) cover.style.backgroundImage = `url("${printMode ? photo.printSrc : photo.src}")`;
  });

  const lightbox = document.querySelector("#lightbox");
  const lightboxImage = document.querySelector("#lightboxImage");
  const lightboxCaption = document.querySelector("#lightboxCaption");
  const lightboxSource = document.querySelector("#lightboxSource");
  let currentKey = null;
  let returnFocus = null;
  const backgroundNodes = [document.querySelector(".app"), document.querySelector(".footer")].filter(Boolean);
  const showPhoto = key => {
    const photo = photos[key];
    if (!photo || !lightbox) return;
    currentKey = key;
    lightboxImage.src = photo.src;
    lightboxImage.srcset = photo.srcset;
    lightboxImage.alt = photo.caption;
    lightboxCaption.textContent = `${photo.caption} · ${photo.creator}`;
    lightboxSource.href = photo.pageUrl;
  };
  const openLightbox = (key, trigger) => {
    if (!photos[key] || !lightbox) return;
    returnFocus = trigger;
    showPhoto(key);
    lightbox.classList.add("open");
    lightbox.setAttribute("aria-hidden", "false");
    backgroundNodes.forEach(node => { node.inert = true; });
    document.body.style.overflow = "hidden";
    document.querySelector("#lightboxClose")?.focus();
  };
  const closeLightbox = () => {
    if (!lightbox) return;
    lightbox.classList.remove("open");
    lightbox.setAttribute("aria-hidden", "true");
    backgroundNodes.forEach(node => { node.inert = false; });
    document.body.style.overflow = "";
    returnFocus?.focus();
  };
  const shiftPhoto = delta => {
    const index = photoKeys.indexOf(currentKey);
    if (index < 0) return;
    showPhoto(photoKeys[(index + delta + photoKeys.length) % photoKeys.length]);
  };
  document.querySelectorAll(".photo-open").forEach(button => {
    button.addEventListener("click", () => openLightbox(button.dataset.photo, button));
  });
  document.querySelector("#lightboxClose")?.addEventListener("click", closeLightbox);
  document.querySelector("#lightboxPrev")?.addEventListener("click", () => shiftPhoto(-1));
  document.querySelector("#lightboxNext")?.addEventListener("click", () => shiftPhoto(1));
  lightbox?.addEventListener("click", event => { if (event.target === lightbox) closeLightbox(); });
  document.addEventListener("keydown", event => {
    if (!lightbox?.classList.contains("open")) return;
    if (event.key === "Escape") closeLightbox();
    if (event.key === "ArrowLeft") shiftPhoto(-1);
    if (event.key === "ArrowRight") shiftPhoto(1);
    if (event.key !== "Tab") return;
    const focusable = [...lightbox.querySelectorAll("button:not([disabled]),a[href]")].filter(el => el.offsetParent !== null);
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  const sourceSearch = document.querySelector("#sourceSearch");
  const sourceCards = [...document.querySelectorAll(".source-link")];
  sourceSearch?.addEventListener("input", () => {
    const term = sourceSearch.value.trim().toLowerCase();
    sourceCards.forEach(card => { card.hidden = !!term && !card.textContent.toLowerCase().includes(term); });
  });

  if ("IntersectionObserver" in window && guideNav) {
    const links = [...guideNav.querySelectorAll("a[href^='#']")];
    const byId = new Map(links.map(link => [link.getAttribute("href").slice(1), link]));
    const observer = new IntersectionObserver(entries => {
      entries.filter(entry => entry.isIntersecting).forEach(entry => {
        links.forEach(link => link.classList.remove("active"));
        byId.get(entry.target.id)?.classList.add("active");
      });
    }, { rootMargin: "-18% 0px -72% 0px" });
    searchable.forEach(section => observer.observe(section));
  }

  updateBuilder();
})();
"""


POLISH_CSS = r"""
:root {
  --focus: #d5b678;
}

.skip-link {
  position: fixed;
  left: 18px;
  top: 14px;
  z-index: 2000;
  transform: translateY(-180%);
  padding: 10px 14px;
  border-radius: 10px;
  background: #ffffff;
  color: #0b2b21;
  font-weight: 800;
}

.skip-link:focus { transform: translateY(0); }

:where(a, button, input):focus-visible {
  outline: 3px solid var(--focus);
  outline-offset: 3px;
}

.guide-menu-toggle {
  display: none;
  min-width: 74px;
  padding: 9px 12px;
  border: 1px solid #5b7a6e;
  border-radius: 10px;
  background: transparent;
  color: #ffffff;
  font-weight: 800;
  cursor: pointer;
}

.photo-card figcaption { align-items: center; }
.photo-card figcaption span { font-weight: 700; }
.photo-meta { font-size: 11px; line-height: 1.55; }
.catalogue-notes { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.catalogue-notes .card { box-shadow: none; }
.excursion-head { grid-template-columns: auto 1fr; }
.excursion-head .status-pill { grid-column: 1; }
.excursion-head > div { grid-column: 2; grid-row: 1 / span 2; }
.excursion-sources h5 { margin: 18px 0 8px; font-size: 12px; letter-spacing: .08em; text-transform: uppercase; }
.print-footer { display: none; }

@media (max-width: 1100px) {
  .app { display: block; }
  .sidebar {
    position: sticky;
    top: 0;
    height: auto;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto minmax(76px, auto);
    align-items: center;
    gap: 10px 14px;
    padding: 12px 16px;
    overflow: visible;
    box-shadow: 0 10px 30px rgba(5, 20, 15, .18);
  }
  .brand { margin: 0; min-width: 0; font-size: 19px; }
  .brand small { display: block; margin-top: 3px; font-size: 9px; }
  .search { width: min(330px, 38vw); margin-left: auto; }
  .guide-menu-toggle { display: inline-flex; align-items: center; justify-content: center; }
  .sidebar nav,
  .sidebar .side-actions {
    display: none;
    grid-column: 1 / -1;
  }
  .sidebar.nav-open nav {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    max-height: min(62vh, 570px);
    margin: 0;
    padding: 8px;
    overflow: auto;
    border: 1px solid #42665a;
    border-radius: 14px;
    background: #0c2b21;
  }
  .sidebar.nav-open .side-actions {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .section { scroll-margin-top: 106px; }
  .catalogue-notes { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (max-width: 720px) {
  .sidebar {
    grid-template-columns: minmax(0, 1fr) auto;
  }
  .search { grid-column: 1 / -1; grid-row: 2; width: 100%; margin: 0; }
  .sidebar nav,
  .sidebar .side-actions { grid-column: 1 / -1; }
  .sidebar.nav-open nav { grid-template-columns: 1fr; }
  .cover { min-height: 690px; }
  .cover-content { padding: 72px 20px 54px; }
  .cover h1 { font-size: clamp(43px, 13vw, 58px); }
  .deck { font-size: 19px; }
  .cover-meta { gap: 8px; }
  .cover-meta span { font-size: 12px; }
  .facts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .catalogue-notes { grid-template-columns: 1fr; }
  .section-head,
  .module-head { align-items: flex-start; }
  .section-head h2,
  .module-head h2 { font-size: clamp(34px, 10vw, 44px); }
  .excursion-card { padding: 18px; }
  .excursion-details div { grid-template-columns: 1fr; gap: 3px; }
  .photo-grid,
  .photo-grid.two { grid-template-columns: 1fr; }
}

@media print {
  @page { size: A4; margin: 13mm 15mm 18mm; }
  html, body { background: #ffffff !important; }
  body { font-size: 9.8pt; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .skip-link,
  .guide-menu-toggle { display: none !important; }
  .section { padding-top: 8mm; padding-bottom: 8mm; }
  .cover { height: 250mm; min-height: 250mm; }
  .cover-content { padding: 27mm 17mm; }
  .cover h1 { font-size: 43pt; }
  .deck { font-size: 15.5pt; }
  .module-section { break-before: page; }
  #trip-builder + .section { break-before: auto; }
  .catalogue-section { break-before: page; }
  .catalogue-notes { display: grid !important; grid-template-columns: repeat(2, 1fr) !important; }
  .catalogue-group { break-before: page; margin-top: 0; }
  .catalogue-group > header,
  .catalogue-group:not([aria-labelledby="catalogue-plan-ready"]) > header {
    min-height: 0 !important;
    height: auto !important;
    max-height: none !important;
    display: block !important;
    justify-content: initial !important;
    margin: 0 0 5mm;
    padding: 6mm !important;
    border: 1px solid #d7c38f;
    border-radius: 3mm;
    break-after: avoid !important;
    page-break-after: avoid !important;
  }
  .catalogue-group > header::before { content: none !important; display: none !important; }
  .excursion-sources { display: none !important; }
  .excursion-card { break-inside: avoid-page; page-break-inside: avoid; padding: 5mm; margin-bottom: 5mm; }
  .excursion-details div { break-inside: avoid; }
  .excursion-sources .button { padding: 4pt 6pt; font-size: 7.3pt; }
  .photo-card { break-inside: avoid; page-break-inside: avoid; }
  .photo-meta { min-height: 0 !important; font-size: 6.8pt; }
  .photo-atlas { break-before: page; }
  .link-directory { break-before: page; }
  .source-link { padding: 6pt; break-inside: avoid; }
  .source-link a { font-size: 8pt; }
  .source-link span { font-size: 6.7pt; }
  h2, h3, h4 { break-after: avoid; }
  .print-footer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: -12mm;
    display: flex;
    justify-content: space-between;
    padding-top: 2mm;
    border-top: .3mm solid #c9d2cc;
    color: #59675f;
    font: 7.5pt Arial, sans-serif;
  }
}
"""


def replace_inner(tag, html: str) -> None:
    fragment = BeautifulSoup(html, "html.parser")
    tag.clear()
    for child in list(fragment.contents):
        tag.append(child)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "excursion"


def export_photos(soup: BeautifulSoup) -> dict[str, dict[str, object]]:
    photo_script = next(script for script in soup.find_all("script") if (script.string or "").startswith("window.PHOTO_DATA="))
    raw = photo_script.string or ""
    records = json.loads(raw[len("window.PHOTO_DATA=") :].rstrip(";"))
    PHOTO_DIR.mkdir(parents=True, exist_ok=True)
    clean_records: dict[str, dict[str, object]] = {}
    for old_key, record in records.items():
        key = PHOTO_SLUGS[old_key]
        encoded = record["src"].split(",", 1)[1]
        original = base64.b64decode(encoded)
        (PHOTO_DIR / f"{key}-print.jpg").write_bytes(original)
        image = Image.open(io.BytesIO(original)).convert("RGB")
        for width in (640, 1280):
            derivative = image.copy()
            if derivative.width > width:
                derivative.thumbnail((width, 4000), Image.Resampling.LANCZOS)
            derivative.save(PHOTO_DIR / f"{key}-{width}.webp", "WEBP", quality=83, method=6)
        clean_records[key] = {
            "src": f"assets/photos/{key}-1280.webp",
            "srcset": f"assets/photos/{key}-640.webp 640w, assets/photos/{key}-1280.webp 1280w",
            "printSrc": f"assets/photos/{key}-print.jpg",
            "caption": record["caption"],
            "creator": record["creator"],
            "pageUrl": record["pageUrl"],
        }
    photo_script.string = "window.TRAVEL_PHOTOS=" + json.dumps(clean_records, ensure_ascii=False, separators=(",", ":")) + ";"
    return clean_records


def clean_text(value: str) -> str:
    if not value.strip():
        return value
    leading = value[: len(value) - len(value.lstrip())]
    trailing = value[len(value.rstrip()) :]
    text = value.strip()
    text = text.replace("\u2010", "-").replace("\u2011", "-").replace("\u2012", "-").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"\bL1\s*-\s*L7\b", "all seven day plans", text, flags=re.I)
    text = re.sub(r"\bL2\s*-\s*L7\b", "the six mountain days", text, flags=re.I)
    for code, name in DAY_NAMES.items():
        text = re.sub(rf"\b{code}\b", name, text)
    text = re.sub(r"\bLX\d{1,3}\b\s*[·:.-]?\s*", "", text)
    text = re.sub(r"\bP\d{1,3}(?:-O\d{1,2})?\b\s*[·:.-]?\s*", "", text)
    text = re.sub(r"\bL\d{3}\b\s*[·:.-]?\s*", "", text)
    replacements = [
        (r"\bGO\s*/\s*caution\s*/\s*NO-GO\s+gate\b", "Conditions to check"),
        (r"\bGO\s*/\s*CAUTION\s*/\s*NO-GO\s+gates\b", "conditions to check"),
        (r"\bStandalone verdict\b", "At a glance"),
        (r"\bIt is only a GO after checking\b", "Choose it only after checking"),
        (r"\bNO-GO in closure\b", "Stop if closed"),
        (r"\bPLAN-READY\b", "STRAIGHTFORWARD"),
        (r"\bCONDITIONAL\b", "CHECK FIRST"),
        (r"\bINSPIRATION\b", "LONGER JOURNEY"),
        (r"\bplan-ready\b", "straightforward"),
        (r"\bconditional\b", "check-first"),
        (r"\binspiration\b", "longer journey"),
        (r"\bdecision gates\b", "decision checks"),
        (r"\btimetable gates\b", "timetable checks"),
        (r"\bday-before gate\b", "day-before check"),
        (r"\bweather gate\b", "weather check"),
        (r"\bhard gate\b", "deciding condition"),
        (r"\badvance gate\b", "check ahead"),
        (r"\bgates\b", "conditions"),
        (r"\bgate\b", "condition"),
        (r"\bverified\b", "confirmed"),
        (r"\bunverified\b", "unchecked"),
        (r"\bverification\b", "confirmation"),
        (r"\bverify\b", "check"),
        (r"\baudited\b", "independent"),
        (r"\baudit\b", "check"),
        (r"\bprovenance\b", "credits"),
        (r"\bdossiers\b", "guides"),
        (r"\bdossier\b", "guide"),
        (r"\bmodules\b", "day plans"),
        (r"\bmodule\b", "day plan"),
        (r"\bmodular\b", "flexible"),
        (r"\bcontrolling sources?\b", "official information"),
        (r"\bcontrolling and operational sources\b", "Official information"),
        (r"\bdiscovery lineage\b", "Planning links"),
        (r"\bsource lineage\b", "source information"),
        (r"\bresearch cut-?off\b", "information date"),
        (r"\bphoto atlas\b", "photo guide"),
        (r"\brights record\b", "source credits"),
        (r"\bphoto[- ]?ids?\b", "photographs"),
        (r"\bmanifest\b", "record"),
        (r"\bsha-?256\b|\bchecksum\b|\bbinary hash\b", "source detail"),
        (r"\bQA\b", ""),
        (r"\brelease(?:d|s)?\b", "edition"),
        (r"\bv(?:ersion\s*)?\d+(?:\.\d+)+\b", ""),
        (r"\bRigi\s+Rigi\b", "Rigi"),
        (r"\bPilatus\s+Pilatus\b", "Pilatus"),
        (r"\bTitlis\s+Engelberg(?:\s+and|-)\s*TITLIS\b", "Engelberg and Titlis"),
        (r"\bStoos\s+Stoos\b", "Stoos"),
        (r"\bStanserhorn\s+Stanserhorn\b", "Stanserhorn"),
        (r"\bBürgenstock\s+Bürgenstock\b", "Bürgenstock"),
        (r"\bcore day plans?\b", "day plans"),
        (r"\bcore-day plan\b", "day plan"),
        (r"\bstandalone core\b", "complete day-plan set"),
        (r"\bcore legs?\b", "essential connections"),
        (r"\bcore lift closure\b", "essential lift closure"),
        (r"\bcore closure\b", "essential connection closure"),
        (r"\bcore promise\b", "default recommendation"),
        (r"\bcore guide\b", "main guide"),
        (r"\bcore Big Six\b", "six main mountain days"),
        (r"\bcity core\b", "city centre"),
        (r"\bcore transport closure\b", "essential transport closure"),
        (r"\bcore risk\b", "main risk"),
        (r"\bthe core visit\b", "the main visit"),
        (r"\bLX atlas\b", "additional excursions"),
        (r"\bLX\b", "additional excursions"),
        (r"\batlas\b", "collection"),
        (r"\brecords\b", "entries"),
        (r"\bTier before distance\b", "Practical fit before distance"),
        (r"\bprice snapshot\b", "price reference"),
        (r"\bsnapshot\b", "reference"),
        (r"\bHiker edition\b", "Hiking-focused plan"),
        (r"\bComplete fair-weather edition\b", "All seven days"),
        (r"\bthis edition\b", "the guide"),
        (r"\bconditions pass\b", "conditions are suitable"),
        (r"\bmountain system pass\b", "mountain system is operating"),
        (r"\boperating hub\b", "base"),
        (r"\bplanning envelope\b", "time to allow"),
        (r"\bGolden window\b", "Pilatus full-loop season"),
        (r"\bdecision matrix\b", "comparison"),
        (r"\s*-\s*checked 24 Aug(?:ust)?(?: 2026)?", ""),
        (r"\bchecked 24 Aug(?:ust)?(?: 2026)?\s*-\s*recheck\b", "confirm current timetable"),
        (r"\bcaptured official combined excursion\b", "official combined ticket"),
        (r"\bcaptured options\b", "listed options"),
        (r"\bcaptured combined product\b", "combined ticket"),
        (r"\bplanner-designed route\b", "suggested route"),
        (r"\bplanner estimate\b", "approximate distance"),
        (r"\bplanner allowance\b", "suggested time"),
        (r"\bplanning anchors\b", "suggested sequence"),
        (r"\bsourceable\b", "well-documented"),
        (r"\bseat inventory\b", "seat availability"),
        (r"\bOfficial tourism product cross-check\b", "Official Lucerne Pilatus round-trip product"),
        (r"\bschematic orientation map\s*-\s*not operational routing\b", "route overview in Google Maps"),
    ]
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.I)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\s+[·-]\s*$", "", text)
    return leading + text.strip() + trailing


def build() -> None:
    soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
    photos = export_photos(soup)

    soup.html["data-guide"] = "lucerne-central-switzerland"
    soup.html.attrs.pop("data-excursion-prefix", None)
    soup.title.string = "Lucerne & Central Switzerland Travel Guide"
    description = soup.find("meta", attrs={"name": "description"})
    description["content"] = "A complete guide to Lucerne, Lake Lucerne, Rigi, Pilatus, Titlis, Stoos, Stanserhorn, Bürgenstock and additional Central Switzerland excursions."
    for meta in soup.find_all("meta", attrs={"name": re.compile(r"release|version", re.I)}):
        meta.decompose()
    for style in soup.find_all("style"):
        if style.string:
            cleaned_style = re.sub(
                r'--guide-footer\s*:\s*"[^"]*"',
                '--guide-footer:"Lucerne & Central Switzerland"',
                style.string,
            )
            cleaned_style = cleaned_style.replace("min-height:230mm", "min-height:0")
            cleaned_style = cleaned_style.replace("justify-content:flex-end;break-after:page", "justify-content:flex-start;break-after:avoid")
            cleaned_style = cleaned_style.replace('content:"NEXT DECISION TIER"', 'content:""')
            style.string = cleaned_style

    polish = soup.new_tag("style", id="traveler-polish")
    polish.string = POLISH_CSS
    soup.head.append(polish)

    skip = soup.new_tag("a", href="#main-content", attrs={"class": "skip-link"})
    skip.string = "Skip to main content"
    soup.body.insert(0, skip)
    main = soup.select_one(".main")
    main["id"] = "main-content"
    main["tabindex"] = "-1"

    for old_id, new_id in DAY_IDS.items():
        element = soup.find(id=old_id)
        if element:
            element["id"] = new_id
        for anchor in soup.find_all("a", href=f"#{old_id}"):
            anchor["href"] = f"#{new_id}"

    cover = soup.select_one(".cover")
    cover["id"] = "top"
    cover.attrs.pop("data-photo-id", None)
    cover_image = cover.select_one("[data-cover-photo]")
    cover_image["data-cover-photo"] = PHOTO_SLUGS[cover_image["data-cover-photo"]]
    cover.select_one(".eyebrow").string = "Independent travel guide · Central Switzerland"
    cover.select_one(".deck").string = "A clear, date-flexible guide to seven complete day plans and 41 additional excursions across lakes, historic towns, family destinations and mountain routes."
    cover_metas = cover.select(".cover-meta")
    replace_inner(cover_metas[0], "<span>Seven complete day plans</span><span>41 additional excursions</span><span>Rail, boat and mountain routes</span><span>Photographs with source credits</span>")
    cover_metas[1].decompose()
    cover_photo_button = cover.select_one(".photo-open")
    cover_photo_button["data-photo"] = "lucerne-old-town"
    cover_photo_button["aria-label"] = "Open photograph: Lucerne Old Town on the Reuss"
    cover_photo_button.string = "View cover photograph"
    pdf_link = cover.select_one(".pdf-link")
    pdf_link["href"] = "Lucerne_Central_Switzerland_Travel_Guide_2026.pdf"
    pdf_link.string = "Open printable guide"

    overview_facts = soup.select_one(".main > section:nth-of-type(2) .facts")
    replace_inner(overview_facts, """
      <div><strong>7</strong><span>complete day plans</span></div>
      <div><strong>41</strong><span>additional excursions</span></div>
      <div><strong>30</strong><span>destination photographs</span></div>
      <div><strong>3 groups</strong><span>simple to longer journeys</span></div>
      <div><strong>Rail-first</strong><span>default regional travel</span></div>
      <div><strong>Check live</strong><span>weather, transport and access</span></div>
    """)

    sidebar = soup.select_one(".sidebar")
    sidebar.select_one(".brand").clear()
    replace_inner(sidebar.select_one(".brand"), "Lucerne + Central Switzerland<small>Travel guide</small>")
    nav = sidebar.find("nav")
    nav["id"] = "guide-navigation"
    nav_labels = {
        "#how-to-use": "Journey overview",
        "#master-map": "Map",
        "#trip-builder": "Build your trip",
        "#compatibility": "Compare day plans",
        "#day-lucerne": "Lucerne city and lake",
        "#day-rigi": "Rigi",
        "#day-pilatus": "Pilatus",
        "#day-titlis": "Titlis",
        "#day-stoos": "Stoos",
        "#day-stanserhorn": "Stanserhorn",
        "#day-burgenstock": "Bürgenstock",
        "#excursion-catalogue": "More excursions",
        "#hotels": "Accommodation",
        "#transport": "Transport",
        "#localities": "Place profiles",
        "#budget": "Budget",
        "#safety": "Safety and access",
        "#packing": "Before you go",
        "#photo-atlas": "Photo guide",
        "#all-links": "Travel links",
    }
    for link in nav.find_all("a", href=True):
        if link["href"] in nav_labels:
            link.string = nav_labels[link["href"]]
    menu = soup.new_tag("button", attrs={
        "class": "guide-menu-toggle",
        "type": "button",
        "aria-controls": "guide-navigation",
        "aria-expanded": "false",
    })
    menu.string = "Menu"
    sidebar.select_one(".brand").insert_after(menu)
    guide_search = soup.find(id="guideSearch")
    guide_search["placeholder"] = "Search places, routes and practical advice"
    guide_search["autocomplete"] = "off"
    for link in sidebar.select(".side-actions a"):
        if "pdf" in link.get_text(" ", strip=True).lower():
            link["href"] = "Lucerne_Central_Switzerland_Travel_Guide_2026.pdf"
            link.string = "Open printable guide"
        else:
            link.string = "Travel links"

    heading_changes = {
        "Build your own trip": "Build your trip",
        "Compatibility and decision matrix": "Compare the day plans",
        "Extended excursion catalogue": "More excursions",
        "Accommodation dossiers": "Accommodation",
        "Transport and distance matrix": "Transport and distances",
        "Safety, access and decision gates": "Safety and access",
        "Photo atlas and rights record": "Photo guide",
        "Complete visible link directory": "Travel links",
    }
    for heading in soup.find_all(["h1", "h2", "h3", "h4"]):
        text = " ".join(heading.get_text(" ", strip=True).split())
        if text in heading_changes:
            heading.string = heading_changes[text]

    overview = soup.find(id="how-to-use")
    overview.select_one(".section-head p").string = "Seven complete day plans, one base and flexible timing."
    overview.select_one(".lead").string = (
        "Use Lucerne as the base, then choose each day according to the date, weather, transport, "
        "trail and accessibility conditions. The seven complete day plans can be used on their own. "
        "The 41 additional excursions are grouped as straightforward choices, check-first choices "
        "and longer journeys that benefit from more time or an overnight stay."
    )
    overview_cards = overview.select(".cards .card")
    replace_inner(overview_cards[0], "<h3>Let one condition decide</h3><p>If an essential connection is closed, weather is unsafe or the last descent is too tight, use the named alternative.</p>")
    replace_inner(overview_cards[1], "<h3>Enjoy the journey</h3><p>Boats, cogwheel railways, funiculars and cableways are part of the experience. Keep the exact pier, stop and transfer walk.</p>")
    replace_inner(overview_cards[2], "<h3>Check practical fit</h3><p>A direct train can make a distant city easy, while a nearby cableway or cave may depend on one booking, season or live condition.</p>")
    overview_callout = overview.select_one("aside.callout")
    replace_inner(overview_callout, "<h4>Check again before departure</h4><p>For every mountain day, confirm the dated SBB journey, operator timetable and facilities, MeteoSwiss warnings, webcam, trail status, reservation or boarding time, last descent and mobility restrictions. Prices, rooms and attraction capacity can change.</p>")

    map_title = soup.select_one("#master-map svg title")
    if map_title:
        map_title.string = "Lucerne and Central Switzerland destination map"
    for code_label in soup.select("#master-map text.small"):
        code_label.decompose()

    trip_builder = soup.find(id="trip-builder")
    trip_builder.select_one(".section-head p").string = "Every plan can be used on its own."
    combo_copy = [
        ("Choose one", "Lucerne for a city-and-lake day, Rigi for the classic loop, or a mountain plan whose conditions are suitable."),
        ("Essential pair", "Combine Lucerne city and lake with Rigi. Keep Rigi for the clearer day."),
        ("Classic trio", "Combine Lucerne, Rigi and Pilatus during the Pilatus full-loop season; use Stanserhorn instead when the full loop is unavailable."),
        ("Mountain contrast", "Combine Lucerne, Rigi, Pilatus and Stanserhorn to balance longer circuits with a compact mountain day."),
        ("High-country set", "Add Titlis only after checking the 2026 construction schedule, boarding capacity and mobility restrictions."),
        ("Hiking-focused plan", "Add Stoos only for suitable hikers and dry, stable ridge conditions."),
        ("All seven days", "Use every day plan only when Bürgenstock's Cliff Walk and Hammetschwand Lift, and each selected mountain system, are operating."),
    ]
    for article, (title, copy) in zip(trip_builder.select(".combo-grid article"), combo_copy):
        article.find("h4").string = title
        article.find("p").string = copy

    comparison = soup.find(id="compatibility")
    comparison.select_one("table caption").string = "Day plan comparison"
    comparison_headers = ["Day plan", "Minimum", "From Lucerne", "Car-free", "Weather sensitivity", "Check ahead"]
    for heading, label in zip(comparison.select("thead th"), comparison_headers):
        heading.string = label

    catalogue = soup.find(id="excursion-catalogue")
    catalogue.select_one(".section-head p").string = "Forty-one additional ideas, grouped by how easily they fit a Lucerne-based trip."
    catalogue.select_one(".lead").string = "Use these excursions to widen the trip without understating distance, reservations, seasonal limits or the value of an overnight stay."
    replace_inner(catalogue.select_one(".facts"), """
      <div><strong>41</strong><span>additional excursions</span></div>
      <div><strong>18</strong><span>straightforward choices</span></div>
      <div><strong>18</strong><span>check-first choices</span></div>
      <div><strong>5</strong><span>longer journeys</span></div>
    """)
    notes = catalogue.select_one(".catalogue-notes")
    replace_inner(notes, """
      <article class="card"><h3>Start with the seven complete days</h3><p>Lucerne, Rigi, Pilatus, Titlis, Stoos, Stanserhorn and Bürgenstock remain the simplest complete choices from one lake base.</p></article>
      <article class="card"><h3>Check the exact timetable</h3><p>Travel ranges are useful for orientation, but SBB and each operator should be checked for the precise date, accessibility need and final return.</p></article>
      <article class="card"><h3>Check every connection</h3><p>A running train does not prove that the connecting boat, bus, cableway, trail, cave or museum is available. Keep one simpler alternative.</p></article>
      <article class="card"><h3>Match the route to the day</h3><p>Mountain paths, caves, winter routes and water activities need the named official route, live conditions and appropriate equipment.</p></article>
      <article class="card"><h3>Give distant places enough time</h3><p>Zurich, Bern, Basel, Interlaken, Rhine Falls and Lugano can work as long days. The farthest destinations are often better with an overnight stay.</p></article>
    """)
    callout = catalogue.select_one("aside.callout")
    replace_inner(callout, "<h4>Choose by practical fit</h4><p><strong>Straightforward</strong> choices still need a dated timetable and opening check. <strong>Check first</strong> choices depend on one decisive connection, booking or condition. <strong>Longer journeys</strong> deserve more time or specialist planning.</p>")
    photo_lead = catalogue.select_one(".catalogue-photo-lead")
    photo_lead.find("h3").string = "Places at a glance"
    photo_lead.find("p").string = "These photographs introduce additional lake, town, mountain and cultural destinations. Creator and source details appear in the Photo guide."

    group_copy = {
        "catalogue-plan-ready": ("Straightforward additions", "Credible Lucerne outings after checking the dated timetable, opening and weather."),
        "catalogue-conditional": ("Check timing and conditions", "Strong ideas whose access, trail, booking, season or connection can change the day."),
        "catalogue-inspiration": ("Longer journeys", "Places best approached with an overnight stay, extra time or specialist competence."),
    }
    for group_id, (title, summary) in group_copy.items():
        heading = soup.find(id=group_id)
        if heading:
            heading.string = title
            heading.find_next_sibling("p").string = summary

    status_copy = {
        "PLAN-READY": "Straightforward",
        "CONDITIONAL": "Check first",
        "INSPIRATION": "Longer journey",
    }
    for card in soup.select(".excursion-card"):
        heading = card.find("h4")
        card_id = slugify(heading.get_text(" ", strip=True))
        card["id"] = f"excursion-{card_id}"
        status = card.get("data-status", "")
        card.attrs.pop("data-excursion-id", None)
        card.attrs.pop("data-status", None)
        identifier = card.select_one(".excursion-id")
        if identifier:
            identifier.decompose()
        pill = card.select_one(".status-pill")
        if pill:
            pill.string = status_copy.get(status, "Plan carefully")
        checked = card.select_one(".checked")
        if checked:
            checked.decompose()
        for term in card.find_all("dt"):
            label = " ".join(term.get_text(" ", strip=True).split()).lower()
            if label == "realistic envelope":
                term.string = "Time to allow"
            elif label == "decisive gate":
                term.string = "Check before leaving"
            elif label == "pairing or fallback":
                term.string = "Simpler alternative"
        source_headings = card.select(".excursion-sources h5")
        if source_headings:
            source_headings[0].string = "Planning links"
        if len(source_headings) > 1:
            source_headings[1].string = "Official information"

    for index, card in enumerate(soup.select(".module-card"), start=1):
        code = card.select_one(".module-code")
        if code:
            code.string = f"{index:02d}"
        input_element = card.find("input", attrs={"type": "checkbox"})
        if input_element:
            input_element["value"] = input_element.get("data-title", f"Day {index}")
    for index, section in enumerate(soup.select(".module-section"), start=1):
        code = section.select_one(".module-head .module-code")
        if code:
            code.string = f"{index:02d}"
    for heading in soup.select(".decision-grid .go h4"):
        heading.string = "Good conditions"
    for heading in soup.select(".decision-grid .caution h4"):
        heading.string = "Check first"
    for heading in soup.select(".decision-grid .no h4"):
        heading.string = "Choose another day"

    hotels = soup.find(id="hotels")
    hotels.select_one(".section-head p").string = "Direct property links, addresses and practical details for choosing a base."
    hotel_callout = hotels.select_one("aside.callout")
    replace_inner(hotel_callout, "<h4>Compare the exact stay</h4><p>Room prices and availability change. Compare the official cancellable rate for the exact dates, and request written confirmation for parking, late arrival, room-level accessibility and mountain transfers when the property page does not answer the question.</p>")
    for node in hotels.find_all(string=re.compile(r"OK:GO record", re.I)):
        node.replace_with(re.sub(r"linked OK:GO record", "linked property information", str(node), flags=re.I))

    safety = soup.find(id="safety")
    fire_heading = next((heading for heading in safety.find_all("h3") if "Fire and official restrictions" in heading.get_text(" ", strip=True)), None)
    if fire_heading:
        paragraph = fire_heading.find_next_sibling("p")
        paragraph.string = "Do not use a stove, smoking source or open fire where a ban applies. Check current cantonal and operator restrictions immediately before setting out; bans can change with heat, wind and drought."

    for element in soup.select("[data-photo-src], [data-photo]"):
        if element.has_attr("data-photo-src"):
            element["data-photo-src"] = PHOTO_SLUGS.get(
                element["data-photo-src"], element["data-photo-src"]
            )
        if element.has_attr("data-photo"):
            old = element["data-photo"]
            slug = PHOTO_SLUGS.get(old, old)
            element["data-photo"] = slug
            caption = photos[slug]["caption"]
            element["aria-label"] = f"Open photograph: {caption}"
    for card in soup.select(".photo-card"):
        card.attrs.pop("data-photo-id", None)
        card.attrs.pop("data-occurrence", None)
        card.attrs.pop("id", None)
        photo_id = card.select_one(".photo-id")
        if photo_id:
            photo_id.decompose()
        size = card.select_one("figcaption small")
        if size:
            size.decompose()
        for meta in card.select(".photo-meta > div"):
            if "Appears in:" in meta.get_text(" ", strip=True):
                meta.decompose()
    lightbox_image = soup.find(id="lightboxImage")
    if lightbox_image:
        lightbox_image["alt"] = "Selected travel photograph"

    photo_section = soup.find(id="photo-atlas")
    photo_section.select_one(".section-head p").string = "Creator, source and licence details for photographs used in the guide."
    photo_callout = photo_section.select_one(".callout")
    if photo_callout:
        replace_inner(photo_callout, "<h4>Photo credits</h4><p>Each photograph is credited to its creator and source. Open the linked source page for the applicable licence details.</p>")
    link_section = soup.find(id="all-links")
    link_section.select_one(".section-head p").string = "Official transport, booking, safety and destination links used throughout the guide."

    footer = soup.select_one(".footer")
    replace_inner(footer, "<p>Operating information can change. Confirm weather, transport, access and reservations directly before departure.</p><p class='fine'>Photographs are credited in the Photo guide.</p>")
    for print_only in soup.select(".print-only"):
        print_only.string = "Lucerne & Central Switzerland Travel Guide"
    print_footer = soup.new_tag("div", attrs={"class": "print-footer", "aria-hidden": "true"})
    replace_inner(print_footer, "<span>Lucerne &amp; Central Switzerland</span><span>Travel guide</span>")
    soup.body.append(print_footer)

    for node in list(soup.find_all(string=True)):
        if not isinstance(node, NavigableString) or node.parent.name in {"script", "style", "noscript", "template"}:
            continue
        updated = clean_text(str(node))
        if updated != str(node):
            node.replace_with(updated)

    scripts = soup.find_all("script")
    scripts[-1].string = TRAVEL_JS
    GUIDE.parent.mkdir(parents=True, exist_ok=True)
    GUIDE.write_text(str(soup), encoding="utf-8")

    archive_soup = BeautifulSoup(str(soup), "html.parser")
    archive_photo_script = next(script for script in archive_soup.find_all("script") if (script.string or "").startswith("window.TRAVEL_PHOTOS="))
    archive_photo_script.string = (archive_photo_script.string or "").replace('"assets/photos/', '"../guide/assets/photos/')
    for link in archive_soup.select("a.pdf-link"):
        link["href"] = "Lucerne_Central_Switzerland_Travel_Guide_2026_v1_2.pdf"
    ARCHIVE.write_text(str(archive_soup), encoding="utf-8")

    print(f"Built {GUIDE}")
    print(f"Built {ARCHIVE}")
    print(f"Exported {len(photos)} photographs in two responsive sizes")


if __name__ == "__main__":
    build()
