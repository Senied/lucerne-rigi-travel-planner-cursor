(() => {
  "use strict";

  document.title = "Lucerne & Central Switzerland Travel Guide";
  const description = document.querySelector('meta[name="description"]');
  if (description) {
    description.content = "A complete travel guide to Lucerne, Lake Lucerne, Rigi, Pilatus, Titlis, Stoos, Stanserhorn and Bürgenstock.";
  }

  const replacements = [
    [/Audited modular travel manual\s*·\s*v1\.0\s*-\s*24 August 2026/gi, "Independent travel guide · Central Switzerland"],
    [/Modular planner\s*·\s*v1\.0/gi, "Central Switzerland · day planner"],
    [/Lucerne, Rigi and Central Switzerland Modular Travel Planner 2026\s*·\s*v1\.0/gi, "Lucerne, Rigi and Central Switzerland Travel Planner"],
    [/Research cutoff 2026-08-24\. Operational information remains subject to live confirmation\./gi, "Operating information can change. Confirm the exact route and conditions before departure."],
    [/Complete visible link directory/gi, "Travel links"],
    [/101 unique external targets; the directory is the exact set used elsewhere in the guide\./gi, "Official transport, booking, safety and destination links used throughout the guide."],
    [/Photo provenance atlas/gi, "Photo guide"],
    [/Photo atlas/gi, "Photo guide"],
    [/Standalone verdict/gi, "At a glance"],
    [/GO\s*\/\s*caution\s*\/\s*NO-GO gate/gi, "Conditions to check"],
    [/GO\s*\/\s*CAUTION\s*\/\s*NO-GO gates/gi, "conditions to check"],
    [/gates pass/gi, "conditions are suitable"],
    [/gate included/gi, "planning conditions included"],
    [/weather gate/gi, "weather check"],
    [/day-before gate/gi, "day-before check"],
    [/one hard gate/gi, "one deciding check"],
    [/hard gate/gi, "deciding condition"],
    [/advance gate/gi, "book or check ahead"],
    [/decision gates/gi, "decision checks"],
    [/timetable gates/gi, "timetable checks"],
    [/live gate/gi, "live check"],
    [/what counts as GO/gi, "what is practical"],
    [/only a GO after/gi, "suitable only after"],
    [/no-go in closure/gi, "skip when closed"],
    [/\bgates\b/gi, "conditions"],
    [/\bgate\b/gi, "condition"],
    [/\bverified\b/gi, "confirmed"],
    [/\bverification\b/gi, "confirmation"],
    [/\baudited\b/gi, "checked"],
    [/\baudit\b/gi, "check"],
    [/\bprovenance\b/gi, "credits"],
    [/\bdossiers\b/gi, "guides"],
    [/\bdossier\b/gi, "guide"],
    [/\bModular\b/g, "Flexible"],
    [/\bmodular\b/g, "flexible"],
    [/\bModules\b/g, "Day plans"],
    [/\bmodules\b/g, "day plans"],
    [/\bModule\b/g, "Day plan"],
    [/\bmodule\b/g, "day plan"],
    [/^L[1-7]\s+(?=(?:City|Rigi|Pilatus|Engelberg|Stoos|Stanserhorn|Bürgenstock))/g, ""],
    [/^L\d{3}\s*·\s*/g, ""],
    [/\bL1-L7\b/g, "all seven day plans"],
    [/\bL2-L7\b/g, "the six mountain days"],
    [/\bL1\b/g, "City"],
    [/\bL2\b/g, "Rigi"],
    [/\bL3\b/g, "Pilatus"],
    [/\bL4\b/g, "Titlis"],
    [/\bL5\b/g, "Stoos"],
    [/\bL6\b/g, "Stanserhorn"],
    [/\bL7\b/g, "Bürgenstock"],
  ];

  const cleanText = (value) => {
    const trimmed = value.trim();
    const dayCode = trimmed.match(/^L([1-7])$/);
    if (dayCode) return value.replace(trimmed, dayCode[1].padStart(2, "0"));
    if (trimmed === "GO") return value.replace("GO", "Good conditions");
    if (trimmed === "CAUTION") return value.replace("CAUTION", "Check first");
    if (trimmed === "NO-GO") return value.replace("NO-GO", "Choose another day");
    return replacements.reduce((text, [pattern, replacement]) => text.replace(pattern, replacement), value);
  };

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const parent = node.parentElement;
      if (!parent || parent.closest("script, style")) return NodeFilter.FILTER_REJECT;
      return node.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
    },
  });
  const textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);
  textNodes.forEach((node) => {
    node.nodeValue = cleanText(node.nodeValue);
  });

  document.querySelectorAll(".photo-id, .photo-card figcaption small").forEach((element) => {
    element.setAttribute("aria-hidden", "true");
  });
  document.querySelectorAll(".photo-open").forEach((button) => {
    const label = button.getAttribute("aria-label") || "Open photo";
    button.setAttribute("aria-label", label.replace(/^Open P\d{3}:\s*/i, "Open photo: "));
  });

  const pdfLink = document.querySelector(".pdf-link");
  if (pdfLink) {
    pdfLink.href = "Lucerne_Central_Switzerland_Travel_Guide_2026.pdf";
    pdfLink.textContent = "Open printable guide";
  }

  const sidebar = document.querySelector(".sidebar");
  const sidebarNav = sidebar?.querySelector("nav");
  const brand = sidebar?.querySelector(".brand");
  if (sidebar && sidebarNav && brand) {
    sidebarNav.id = "guide-navigation";
    const toggle = document.createElement("button");
    toggle.className = "guide-menu-toggle";
    toggle.type = "button";
    toggle.textContent = "Menu";
    toggle.setAttribute("aria-controls", sidebarNav.id);
    toggle.setAttribute("aria-expanded", "false");
    brand.after(toggle);

    const setOpen = (open, restoreFocus = false) => {
      sidebar.classList.toggle("menu-open", open);
      toggle.setAttribute("aria-expanded", String(open));
      toggle.textContent = open ? "Close" : "Menu";
      if (open) requestAnimationFrame(() => sidebarNav.querySelector("a")?.focus());
      if (!open && restoreFocus) toggle.focus();
    };

    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true", true));
    sidebarNav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => setOpen(false)));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setOpen(false, true);
    });
    document.addEventListener("pointerdown", (event) => {
      if (toggle.getAttribute("aria-expanded") !== "true") return;
      if (!sidebar.contains(event.target)) setOpen(false);
    });
    matchMedia("(min-width: 1101px)").addEventListener("change", (event) => {
      if (event.matches) setOpen(false);
    });
  }

  const footer = document.querySelector(".footer");
  if (footer) {
    const links = document.createElement("div");
    links.className = "guide-footer-links";
    links.innerHTML = '<a href="../index.html">Planner overview</a><a href="../releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_0.html">Earlier edition</a>';
    footer.append(links);
  }
})();
