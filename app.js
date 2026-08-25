(() => {
  const DAYS = [
    {
      kicker: "L1 · Lake base",
      title: "Lucerne city and lake",
      body: "Chapel Bridge, the Reuss, Musegg Wall and the shoreline — the orientation day that makes every mountain loop readable.",
      stay: "Base · Hotel Schweizerhof or Des Balances",
      img: "assets/images/module-city.jpg",
      alt: "Lucerne old town and lake setting",
    },
    {
      kicker: "L2 · Classic round trip",
      title: "Rigi classic round trip",
      body: "Boat, cogwheel and ridge air — the Queen of the Mountains loop, date-bound for the complete circuit through mid-October.",
      stay: "Gate · 11 May–18 Oct for the full loop",
      img: "assets/images/module-rigi.jpg",
      alt: "Rigi summit panorama above the lake",
    },
    {
      kicker: "L3 · Golden Round Trip",
      title: "Pilatus Golden Round Trip",
      body: "Boat, the world’s steepest cogwheel, and the aerial descent — only when every component operates and seats are secured.",
      stay: "Gate · autumn Kriens aerial closure windows",
      img: "assets/images/module-pilatus.jpg",
      alt: "Pilatus summit above Central Switzerland",
    },
    {
      kicker: "L4 · High alpine",
      title: "Engelberg and Titlis",
      body: "A glacier day with hard 2026 construction truth: rail replacement and Rotair limits change capacity, access and what counts as GO.",
      stay: "Gate · 2026 rail and Rotair constraints",
      img: "assets/images/module-titlis.jpg",
      alt: "Mount Titlis alpine panorama",
    },
    {
      kicker: "L5 · Ridge walk",
      title: "Stoos and the Fronalpstock ridge",
      body: "The steep funicular, then the Klingenstock–Fronalpstock ridge — weather and ticket windows decide whether it stays elegant.",
      stay: "Gate · Peak Experience ticket validity",
      img: "assets/images/module-stoos.jpg",
      alt: "Stoos ridge and alpine pasture terrain",
    },
    {
      kicker: "L6 · Open-top ascent",
      title: "Stanserhorn and Stans",
      body: "CabriO open-top cableway and a composed Stans return — seasonal, reservation-aware, and deliberately calmer than Titlis.",
      stay: "Season · 11 Apr–22 Nov 2026",
      img: "assets/images/module-stanserhorn.jpg",
      alt: "Stanserhorn summit and lake views",
    },
    {
      kicker: "L7 · Cliff elevator",
      title: "Bürgenstock and Hammetschwand",
      body: "Lake terrace, cliff path and Europe’s highest outdoor elevator — a polished half-to-full day above the water.",
      stay: "Mood · lake elegance after harder summits",
      img: "assets/images/module-burgenstock.jpg",
      alt: "Bürgenstock above Lake Lucerne",
    },
  ];

  const MODULES = {
    city: {
      tag: "Lake Lucerne · Orientation",
      title: "Lucerne city and lake",
      body: "The waterfront and old town as a full day — bridges, walls, and lake light — or as the calm bookend around harder mountain circuits.",
      facts: [
        "Chapel Bridge and Water Tower",
        "Musegg Wall and Lion Monument",
        "GO / caution / NO-GO gate included",
      ],
      img: "assets/images/module-city.jpg",
    },
    rigi: {
      tag: "Queen of the Mountains · Classic loop",
      title: "Rigi classic round trip",
      body: "A composed boat-and-cogwheel circuit with ridge air at Kulm — elegant when the full loop is in season and connections hold.",
      facts: [
        "Complete loop window: 11 May–18 Oct 2026",
        "Cogwheel continues later without full boat loop",
        "SGV boat + Rigi day logistics",
      ],
      img: "assets/images/module-rigi.jpg",
    },
    pilatus: {
      tag: "Golden Round Trip · Steepest cogwheel",
      title: "Pilatus Golden Round Trip",
      body: "Three transport moods in one day — only after seat reservation, component status and autumn aerial closures are checked.",
      facts: [
        "World’s steepest cogwheel segment",
        "Kriens aerial maintenance windows in autumn 2026",
        "Reserve before you commit the day",
      ],
      img: "assets/images/module-pilatus.jpg",
    },
    titlis: {
      tag: "Engelberg · Construction-aware glacier day",
      title: "Engelberg and Titlis",
      body: "High alpine spectacle with explicit 2026 mobility gates — rail replacement and Rotair limits are part of the plan, not footnotes.",
      facts: [
        "Rail replacement 7 Sep–1 Nov 2026",
        "Rotair closed 17 Aug–11 Dec 2026",
        "Hard Trübsee limits for some travellers",
      ],
      img: "assets/images/module-titlis.jpg",
    },
    stoos: {
      tag: "Fronalpstock · Ridge day",
      title: "Stoos and the Fronalpstock ridge",
      body: "Steepest funicular, then a ridge that rewards clear weather — ticket windows and wind decide the day.",
      facts: [
        "Stoos funicular ascent",
        "Klingenstock–Fronalpstock ridge hike",
        "Peak Experience ticket validity window",
      ],
      img: "assets/images/module-stoos.jpg",
    },
    stanserhorn: {
      tag: "CabriO · Open-air ascent",
      title: "Stanserhorn and Stans",
      body: "An open-top cableway day with village calm at the end — lighter than Titlis, still seasonal and reservation-aware.",
      facts: [
        "Regular season 11 Apr–22 Nov 2026",
        "CabriO open-top segment",
        "Stans village return",
      ],
      img: "assets/images/module-stanserhorn.jpg",
    },
    burgenstock: {
      tag: "Hammetschwand · Lake terrace",
      title: "Bürgenstock and Hammetschwand",
      body: "Cliff path, outdoor elevator and lake polish — the day that restores elegance after harder summits.",
      facts: [
        "Bürgenstock above the lake",
        "Hammetschwand Lift",
        "Half-day or composed full day",
      ],
      img: "assets/images/module-burgenstock.jpg",
    },
  };

  const nav = document.querySelector("[data-nav]");
  const menuToggle = document.querySelector("[data-menu-toggle]");
  const drawer = document.querySelector("[data-drawer]");
  const toast = document.querySelector("[data-toast]");
  const parallax = document.querySelector("[data-parallax]");
  const mobileBar = document.querySelector("[data-mobile-bar]");

  const onScroll = () => {
    if (!nav) return;
    const y = window.scrollY;
    nav.classList.toggle("is-solid", y > 24);
    if (mobileBar) {
      const heroH = Math.max(320, window.innerHeight * 0.72);
      mobileBar.classList.toggle("is-visible", y > heroH);
    }
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  if (menuToggle && drawer) {
    menuToggle.addEventListener("click", () => {
      const open = !nav.classList.contains("is-open");
      nav.classList.toggle("is-open", open);
      menuToggle.setAttribute("aria-expanded", String(open));
      drawer.hidden = !open;
    });
    drawer.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => {
        nav.classList.remove("is-open");
        menuToggle.setAttribute("aria-expanded", "false");
        drawer.hidden = true;
      });
    });
  }

  if (parallax && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    window.addEventListener(
      "scroll",
      () => {
        const y = Math.min(window.scrollY, 600);
        parallax.style.transform = `scale(1.06) translate3d(0, ${y * 0.18}px, 0)`;
      },
      { passive: true }
    );
  }

  const dayButtons = [...document.querySelectorAll("[data-day]")];
  const dayImg = document.querySelector("[data-day-img]");
  const dayKicker = document.querySelector("[data-day-kicker]");
  const dayTitle = document.querySelector("[data-day-title]");
  const dayBody = document.querySelector("[data-day-body]");
  const dayStay = document.querySelector("[data-day-stay]");

  const setDay = (index) => {
    const day = DAYS[index];
    if (!day) return;
    dayButtons.forEach((btn, i) => {
      const on = i === index;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-selected", String(on));
    });
    dayKicker.textContent = day.kicker;
    dayTitle.textContent = day.title;
    dayBody.textContent = day.body;
    dayStay.textContent = day.stay;
    if (dayImg) {
      dayImg.classList.add("is-swap");
      window.setTimeout(() => {
        dayImg.src = day.img;
        dayImg.alt = day.alt;
        dayImg.classList.remove("is-swap");
      }, 180);
    }
  };

  dayButtons.forEach((btn) => {
    btn.addEventListener("click", () => setDay(Number(btn.dataset.day)));
  });

  const modButtons = [...document.querySelectorAll("[data-mod]")];
  const modImg = document.querySelector("[data-mod-img]");
  const modTag = document.querySelector("[data-mod-tag]");
  const modTitle = document.querySelector("[data-mod-title]");
  const modBody = document.querySelector("[data-mod-body]");
  const modFacts = document.querySelector("[data-mod-facts]");

  const setMod = (key) => {
    const mod = MODULES[key];
    if (!mod) return;
    modButtons.forEach((btn) => {
      const on = btn.dataset.mod === key;
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-selected", String(on));
    });
    modTag.textContent = mod.tag;
    modTitle.textContent = mod.title;
    modBody.textContent = mod.body;
    modFacts.innerHTML = mod.facts.map((f) => `<li>${f}</li>`).join("");
    if (modImg) {
      modImg.classList.add("is-swap");
      window.setTimeout(() => {
        modImg.src = mod.img;
        modImg.classList.remove("is-swap");
      }, 180);
    }
  };

  modButtons.forEach((btn) => {
    btn.addEventListener("click", () => setMod(btn.dataset.mod));
  });

  const counters = [...document.querySelectorAll("[data-count]")];
  const animateCount = (el) => {
    const target = Number(el.dataset.count);
    const duration = 1100;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      el.textContent = String(Math.round(target * eased));
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          animateCount(entry.target);
          obs.unobserve(entry.target);
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((el) => io.observe(el));
  } else {
    counters.forEach(animateCount);
  }

  document
    .querySelectorAll(".section__head, .timeline, .module-board, .stats, .checks, .hashes, .dl-grid, .caution__inner")
    .forEach((el) => el.classList.add("reveal"));

  if ("IntersectionObserver" in window) {
    const revealIo = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("is-in");
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -8% 0px" }
    );
    document.querySelectorAll(".reveal").forEach((el) => revealIo.observe(el));
  } else {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("is-in"));
  }

  let toastTimer;
  const showToast = (msg) => {
    if (!toast) return;
    toast.textContent = msg;
    toast.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.hidden = true;
    }, 1600);
  };

  document.querySelectorAll("[data-hash-row]").forEach((row) => {
    const btn = row.querySelector("[data-copy]");
    const value = row.querySelector(".hash__value");
    if (!btn || !value) return;
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(value.textContent.trim());
        btn.textContent = "Copied";
        btn.classList.add("is-done");
        showToast("Hash copied");
        setTimeout(() => {
          btn.textContent = "Copy";
          btn.classList.remove("is-done");
        }, 1400);
      } catch {
        showToast("Copy failed");
      }
    });
  });

  const track = document.querySelector("[data-timeline]");
  if (track) {
    track.addEventListener("keydown", (e) => {
      const active = dayButtons.findIndex((b) => b.classList.contains("is-active"));
      if (e.key === "ArrowRight") {
        e.preventDefault();
        const next = Math.min(DAYS.length - 1, active + 1);
        setDay(next);
        dayButtons[next]?.focus();
      }
      if (e.key === "ArrowLeft") {
        e.preventDefault();
        const prev = Math.max(0, active - 1);
        setDay(prev);
        dayButtons[prev]?.focus();
      }
    });
  }
})();
