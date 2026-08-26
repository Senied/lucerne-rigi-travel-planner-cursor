(() => {
  "use strict";

  const imageSources = (name, originalWidth) => {
    const responsive = `assets/images/responsive/${name}-640.webp 640w, assets/images/responsive/${name}-1280.webp 1280w`;
    return originalWidth > 1280 ? `${responsive}, assets/images/${name}.jpg ${originalWidth}w` : responsive;
  };

  const DAYS = [
    {
      kicker: "Day 1 · Lake base",
      title: "Lucerne city and lake",
      body: "Chapel Bridge, the Reuss, Musegg Wall and the shoreline — the orientation day that makes every mountain route easier to read.",
      stay: "Best for · Arrival day or uncertain weather",
      img: "assets/images/responsive/module-city-1280.webp",
      srcset: imageSources("module-city", 1280),
      alt: "Lucerne Old Town on the Reuss",
      width: 1280,
      height: 851,
      photoId: "P002",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P002-O03",
    },
    {
      kicker: "Day 2 · Classic round trip",
      title: "Rigi classic round trip",
      body: "Boat, cogwheel and ridge air — the Queen of the Mountains loop, with the complete circuit available through mid-October.",
      stay: "Best window · 11 May–18 October for the full loop",
      img: "assets/images/responsive/module-rigi-1280.webp",
      srcset: imageSources("module-rigi", 1280),
      alt: "Rigi Kulm panorama",
      width: 1280,
      height: 952,
      photoId: "P006",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P006-O02",
    },
    {
      kicker: "Day 3 · Golden Round Trip",
      title: "Pilatus Golden Round Trip",
      body: "Boat, the world’s steepest cogwheel railway and the aerial descent — when every segment operates and seats are secured.",
      stay: "Check first · All segments and autumn aerial closures",
      img: "assets/images/responsive/module-pilatus-1280.webp",
      srcset: imageSources("module-pilatus", 1280),
      alt: "Pilatus summit",
      width: 1280,
      height: 744,
      photoId: "P010",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P010-O02",
    },
    {
      kicker: "Day 4 · High alpine",
      title: "Engelberg and Titlis",
      body: "A glacier day with important 2026 operating changes: rail replacement and Rotair limits affect capacity, access and timing.",
      stay: "Check first · Dated rail and Rotair changes",
      img: "assets/images/responsive/module-titlis-1280.webp",
      srcset: imageSources("module-titlis", 1280),
      alt: "Mount Titlis seen from Gross Spannort",
      width: 1280,
      height: 961,
      photoId: "P013",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P013-O02",
    },
    {
      kicker: "Day 5 · Ridge walk",
      title: "Stoos and the Fronalpstock ridge",
      body: "The steep funicular, then the Klingenstock–Fronalpstock ridge — a rewarding choice for dry, stable weather.",
      stay: "Best for · Hikers on a clear, calm day",
      img: "assets/images/responsive/module-stoos-1280.webp",
      srcset: imageSources("module-stoos", 1280),
      alt: "Klingenstock-Fronalpstock ridge hike",
      width: 1280,
      height: 854,
      photoId: "P017",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P017-O02",
    },
    {
      kicker: "Day 6 · Open-top ascent",
      title: "Stanserhorn and Stans",
      body: "CabriO open-top cableway and a composed Stans return — seasonal, reservation-aware and calmer than Titlis.",
      stay: "Regular season · 11 April–22 November 2026",
      img: "assets/images/responsive/module-stanserhorn-1280.webp",
      srcset: imageSources("module-stanserhorn", 1280),
      alt: "Stanserhorn CabriO",
      width: 1280,
      height: 853,
      photoId: "P020",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P020-O02",
    },
    {
      kicker: "Day 7 · Cliff path and lift",
      title: "Bürgenstock and Hammetschwand",
      body: "Lake terrace, cliff path and Europe’s highest outdoor elevator — a polished half-to-full day above the water.",
      stay: "Check first · Cliff path and lift operation",
      img: "assets/images/responsive/module-burgenstock-1280.webp",
      srcset: imageSources("module-burgenstock", 1280),
      alt: "Bürgenstock above the lake",
      width: 1280,
      height: 957,
      photoId: "P018",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P018-O02",
    },
  ];

  const MODULES = {
    city: {
      tag: "Lake Lucerne · Easy first day",
      title: "Lucerne city and lake",
      body: "The waterfront and old town as a full day — bridges, walls and lake light — or as a calm bookend around harder mountain routes.",
      facts: ["Chapel Bridge and Water Tower", "Musegg Wall and Lion Monument", "Works in almost any weather"],
      img: "assets/images/responsive/module-city-1280.webp",
      srcset: imageSources("module-city", 1280),
      alt: "Lucerne Old Town on the Reuss",
      width: 1280,
      height: 851,
      photoId: "P002",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P002-O03",
      link: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#module-l1",
    },
    rigi: {
      tag: "Queen of the Mountains · Classic loop",
      title: "Rigi classic round trip",
      body: "A composed boat-and-cogwheel circuit with ridge air at Kulm — elegant when the full loop is in season and connections hold.",
      facts: ["Complete loop: 11 May–18 October 2026", "Cogwheel services continue beyond the boat-loop season", "Allow extra time for the Weggis transfer"],
      img: "assets/images/responsive/module-rigi-1280.webp",
      srcset: imageSources("module-rigi", 1280),
      alt: "Rigi Kulm panorama",
      width: 1280,
      height: 952,
      photoId: "P006",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P006-O02",
      link: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#module-l2",
    },
    pilatus: {
      tag: "Golden Round Trip · Steepest cogwheel",
      title: "Pilatus Golden Round Trip",
      body: "Three transport moods in one day — after seat reservations, operating status and autumn aerial closures are checked.",
      facts: ["Boat, cogwheel railway and aerial cableway", "Autumn maintenance changes some routes", "Reserve the cogwheel segment before committing the day"],
      img: "assets/images/responsive/module-pilatus-1280.webp",
      srcset: imageSources("module-pilatus", 1280),
      alt: "Pilatus summit",
      width: 1280,
      height: 744,
      photoId: "P010",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P010-O02",
      link: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#module-l3",
    },
    titlis: {
      tag: "Engelberg · Construction-aware glacier day",
      title: "Engelberg and Titlis",
      body: "High-alpine spectacle with explicit 2026 mobility conditions — rail replacement and Rotair limits belong in the plan.",
      facts: ["Rail replacement: 7 September–1 November 2026", "Rotair changes: 17 August–11 December 2026", "Accessibility above Trübsee is date-dependent"],
      img: "assets/images/responsive/module-titlis-1280.webp",
      srcset: imageSources("module-titlis", 1280),
      alt: "Mount Titlis seen from Gross Spannort",
      width: 1280,
      height: 961,
      photoId: "P013",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P013-O02",
      link: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#module-l4",
    },
    stoos: {
      tag: "Fronalpstock · Ridge day",
      title: "Stoos and the Fronalpstock ridge",
      body: "The steep funicular followed by a ridge that rewards clear weather — wind, trail condition and ticket validity decide the day.",
      facts: ["Stoos funicular ascent", "Klingenstock–Fronalpstock ridge hike", "Dry footing and stable visibility are essential"],
      img: "assets/images/responsive/module-stoos-1280.webp",
      srcset: imageSources("module-stoos", 1280),
      alt: "Klingenstock-Fronalpstock ridge hike",
      width: 1280,
      height: 854,
      photoId: "P017",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P017-O02",
      link: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#module-l5",
    },
    stanserhorn: {
      tag: "CabriO · Open-air ascent",
      title: "Stanserhorn and Stans",
      body: "An open-top cableway day with village calm at the end — lighter than Titlis, still seasonal and reservation-aware.",
      facts: ["Regular season: 11 April–22 November 2026", "CabriO open-top cableway", "Stans village return"],
      img: "assets/images/responsive/module-stanserhorn-1280.webp",
      srcset: imageSources("module-stanserhorn", 1280),
      alt: "Stanserhorn CabriO",
      width: 1280,
      height: 853,
      photoId: "P020",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P020-O02",
      link: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#module-l6",
    },
    burgenstock: {
      tag: "Hammetschwand · Lake terrace",
      title: "Bürgenstock and Hammetschwand",
      body: "Cliff path, outdoor elevator and lake polish — an elegant choice after harder summits, when the route is officially open.",
      facts: ["Catamaran and funicular approach", "Cliff Walk and Hammetschwand Lift", "Half-day or composed full day"],
      img: "assets/images/responsive/module-burgenstock-1280.webp",
      srcset: imageSources("module-burgenstock", 1280),
      alt: "Bürgenstock above the lake",
      width: 1280,
      height: 957,
      photoId: "P018",
      photoHref: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#photo-P018-O02",
      link: "releases/Lucerne_Rigi_Modular_Travel_Planner_2026_v1_3.html#module-l7",
    },
  };

  const nav = document.querySelector("[data-nav]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const drawer = document.querySelector("[data-drawer]");
  const parallax = document.querySelector("[data-parallax]");
  const mobileBar = document.querySelector("[data-mobile-bar]");

  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!nav || !menuToggle || !drawer) return;
    nav.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.setAttribute("aria-label", "Open menu");
    drawer.hidden = true;
    if (restoreFocus) menuToggle.focus();
  };

  const openMenu = () => {
    if (!nav || !menuToggle || !drawer) return;
    nav.classList.add("is-open");
    menuToggle.setAttribute("aria-expanded", "true");
    menuToggle.setAttribute("aria-label", "Close menu");
    drawer.hidden = false;
    requestAnimationFrame(() => drawer.querySelector("a")?.focus());
  };

  if (menuToggle && drawer) {
    menuToggle.addEventListener("click", () => {
      const open = menuToggle.getAttribute("aria-expanded") === "true";
      if (open) closeMenu({ restoreFocus: true });
      else openMenu();
    });
    drawer.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => closeMenu()));
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && menuToggle.getAttribute("aria-expanded") === "true") {
        closeMenu({ restoreFocus: true });
      }
    });
    document.addEventListener("pointerdown", (event) => {
      if (menuToggle.getAttribute("aria-expanded") !== "true") return;
      if (!nav.contains(event.target) && !drawer.contains(event.target)) closeMenu();
    });
    window.addEventListener("resize", () => {
      if (window.innerWidth >= 900) closeMenu();
    });
  }

  const onScroll = () => {
    if (!nav) return;
    const y = window.scrollY;
    nav.classList.toggle("is-solid", y > 24);
    if (mobileBar) {
      const heroHeight = Math.max(320, window.innerHeight * 0.72);
      mobileBar.classList.toggle("is-visible", y > heroHeight);
    }
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (parallax && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    window.addEventListener("scroll", () => {
      const y = Math.min(window.scrollY, 600);
      parallax.style.transform = `scale(1.06) translate3d(0, ${y * 0.18}px, 0)`;
    }, { passive: true });
  }

  const wireTablist = (buttons, activate) => {
    buttons.forEach((button, index) => {
      button.addEventListener("click", () => activate(index));
      button.addEventListener("keydown", (event) => {
        let nextIndex = null;
        if (event.key === "ArrowRight") nextIndex = (index + 1) % buttons.length;
        if (event.key === "ArrowLeft") nextIndex = (index - 1 + buttons.length) % buttons.length;
        if (event.key === "Home") nextIndex = 0;
        if (event.key === "End") nextIndex = buttons.length - 1;
        if (nextIndex === null) return;
        event.preventDefault();
        activate(nextIndex);
        buttons[nextIndex].focus();
      });
    });
  };

  const swapImage = (image, item, photoRef) => {
    if (!image) return;
    image.classList.add("is-swap");
    window.setTimeout(() => {
      image.src = item.img;
      image.srcset = item.srcset;
      image.alt = item.alt;
      image.width = item.width;
      image.height = item.height;
      if (photoRef) {
        photoRef.href = item.photoHref;
        photoRef.textContent = `${item.photoId} · Photo atlas`;
        photoRef.setAttribute("aria-label", `Open ${item.photoId} details in the photo atlas`);
      }
      image.classList.remove("is-swap");
    }, 180);
  };

  const dayButtons = [...document.querySelectorAll("[data-day]")];
  const dayPanel = document.querySelector("[data-day-panel]");
  const dayImg = document.querySelector("[data-day-img]");
  const dayKicker = document.querySelector("[data-day-kicker]");
  const dayTitle = document.querySelector("[data-day-title]");
  const dayBody = document.querySelector("[data-day-body]");
  const dayStay = document.querySelector("[data-day-stay]");
  const dayPhoto = document.querySelector("[data-day-photo]");

  const setDay = (index) => {
    const day = DAYS[index];
    if (!day) return;
    dayButtons.forEach((button, buttonIndex) => {
      const selected = buttonIndex === index;
      button.classList.toggle("is-active", selected);
      button.setAttribute("aria-selected", String(selected));
      button.tabIndex = selected ? 0 : -1;
    });
    dayPanel?.setAttribute("aria-labelledby", dayButtons[index].id);
    if (dayKicker) dayKicker.textContent = day.kicker;
    if (dayTitle) dayTitle.textContent = day.title;
    if (dayBody) dayBody.textContent = day.body;
    if (dayStay) dayStay.textContent = day.stay;
    swapImage(dayImg, day, dayPhoto);
  };
  wireTablist(dayButtons, setDay);

  const modButtons = [...document.querySelectorAll("[data-mod]")];
  const modPanel = document.querySelector("[data-mod-panel]");
  const modImg = document.querySelector("[data-mod-img]");
  const modTag = document.querySelector("[data-mod-tag]");
  const modTitle = document.querySelector("[data-mod-title]");
  const modBody = document.querySelector("[data-mod-body]");
  const modFacts = document.querySelector("[data-mod-facts]");
  const modLink = document.querySelector("[data-mod-link]");
  const modPhoto = document.querySelector("[data-mod-photo]");

  const setMod = (index) => {
    const button = modButtons[index];
    const mod = MODULES[button?.dataset.mod];
    if (!button || !mod) return;
    modButtons.forEach((item, buttonIndex) => {
      const selected = buttonIndex === index;
      item.classList.toggle("is-active", selected);
      item.setAttribute("aria-selected", String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    modPanel?.setAttribute("aria-labelledby", button.id);
    if (modTag) modTag.textContent = mod.tag;
    if (modTitle) modTitle.textContent = mod.title;
    if (modBody) modBody.textContent = mod.body;
    if (modFacts) modFacts.innerHTML = mod.facts.map((fact) => `<li>${fact}</li>`).join("");
    if (modLink) modLink.href = mod.link;
    swapImage(modImg, mod, modPhoto);
  };
  wireTablist(modButtons, setMod);

  document.querySelectorAll(".section__head, .timeline, .module-board, .practical-grid, .dl-grid, .earlier-edition, .caution__inner").forEach((element) => element.classList.add("reveal"));

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add("is-in");
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));
  } else {
    document.querySelectorAll(".reveal").forEach((element) => element.classList.add("is-in"));
  }
})();
