(() => {
  "use strict";
  const doc = document.documentElement;
  doc.classList.add("js");
  const WA = "https://wa.me/27833036393";

  // hero entrance once the hero image is ready
  const hero = document.querySelector(".hero");
  if (hero) {
    const img = hero.querySelector(".hero__img");
    const go = () => requestAnimationFrame(() => hero.classList.add("is-ready"));
    if (!img || img.complete) go();
    else { img.addEventListener("load", go, { once: true }); img.addEventListener("error", go, { once: true }); setTimeout(go, 1800); }
  }

  // solid nav and floating WhatsApp button after the hero
  const nav = document.querySelector("[data-nav]");
  const float = document.querySelector("[data-float]");
  if (hero && "IntersectionObserver" in window) {
    const sentinel = document.createElement("div");
    sentinel.style.cssText = "position:absolute;top:0;left:0;height:120px;width:1px;pointer-events:none";
    hero.appendChild(sentinel);
    new IntersectionObserver(([en]) => nav && nav.classList.toggle("is-solid", !en.isIntersecting)).observe(sentinel);
    new IntersectionObserver(([en]) => float && float.classList.toggle("is-in", !en.isIntersecting), { threshold: 0.15 }).observe(hero);
  } else if (nav) {
    nav.classList.add("is-solid");
  }
  const book = document.getElementById("book");
  if (book && float && "IntersectionObserver" in window) {
    new IntersectionObserver(([en]) => { if (en.isIntersecting) float.classList.remove("is-in"); }, { threshold: 0.2 }).observe(book);
  }

  // mobile menu
  const menuBtn = document.querySelector("[data-menu]");
  const sheet = document.querySelector("[data-sheet]");
  const setMenu = (open) => {
    if (!menuBtn || !sheet) return;
    menuBtn.setAttribute("aria-expanded", String(open));
    sheet.hidden = !open;
    nav.toggleAttribute("data-open", open);
    document.body.style.overflow = open ? "hidden" : "";
  };
  if (menuBtn) {
    menuBtn.addEventListener("click", () => setMenu(menuBtn.getAttribute("aria-expanded") !== "true"));
    sheet.addEventListener("click", (ev) => { if (ev.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") setMenu(false); });
    matchMedia("(min-width: 961px)").addEventListener("change", (m) => { if (m.matches) setMenu(false); });
  }

  // reveal on scroll
  const reveal = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveal.forEach((el) => io.observe(el));
  } else {
    reveal.forEach((el) => el.classList.add("is-in"));
  }

  // before and after
  document.querySelectorAll("[data-compare]").forEach((box) => {
    const range = box.querySelector("input");
    const set = (v) => box.style.setProperty("--pos", v + "%");
    range.addEventListener("input", () => set(range.value));
    set(range.value);
  });

  // Black Friday pricing, 20 to 30 November 2026 (South African time)
  const now = new Date();
  const start = new Date("2026-11-20T00:00:00+02:00");
  const end = new Date("2026-12-01T00:00:00+02:00");
  if (now >= start && now < end) {
    document.querySelectorAll(".price[data-bf]").forEach((p) => {
      const cur = p.querySelector(".price__now");
      const was = document.createElement("s");
      was.className = "price__was";
      was.textContent = cur.textContent;
      cur.textContent = p.dataset.bf;
      p.prepend(was);
      p.classList.add("is-bf");
    });
    document.querySelectorAll("[data-bf-note]").forEach((n) => { n.hidden = false; });
  }

  // booking form opens WhatsApp with the message ready
  const form = document.querySelector("[data-form]");
  if (form) {
    const date = form.querySelector("#f-date");
    if (date) {
      const t = new Date();
      date.min = new Date(t.getTime() - t.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
    }
    const check = (el) => {
      const ok = el.value.trim() !== "";
      const err = document.getElementById(el.id + "-err");
      el.setAttribute("aria-invalid", String(!ok));
      if (err) { err.hidden = ok; ok ? el.removeAttribute("aria-describedby") : el.setAttribute("aria-describedby", err.id); }
      return ok;
    };
    const required = [...form.querySelectorAll("[required]")];
    required.forEach((el) => el.addEventListener("change", () => check(el)));
    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const bad = required.filter((el) => !check(el));
      if (bad.length) { bad[0].focus(); return; }
      const f = new FormData(form);
      let when = "";
      if (f.get("date")) {
        const d = new Date(f.get("date") + "T12:00:00");
        when = d.toLocaleDateString("en-ZA", { weekday: "long", day: "numeric", month: "long" });
      }
      const lines = [
        "Hi Beauty Edition, I would like to book an appointment.",
        "",
        "Name: " + f.get("name").trim(),
        "Treatment: " + f.get("service"),
      ];
      if (when) lines.push("Preferred date: " + when);
      if (f.get("time")) lines.push("Time of day: " + f.get("time"));
      if (f.get("notes").trim()) lines.push("Notes: " + f.get("notes").trim());
      window.open(WA + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
    });
  }
})();
