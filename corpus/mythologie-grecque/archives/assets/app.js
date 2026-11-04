/* MYTHOS — barre de progression des livres archivés.
 * La navigation et la progression de lecture moderne sont gérées séparément.
 * Aucune donnée personnelle n'est enregistrée. */
(() => {
  "use strict";
  const bar = document.querySelector(".progress");
  if (!bar) return;
  Object.assign(bar.style, {
    position: "fixed", top: "0", left: "0", width: "0", height: "3px",
    backgroundColor: "#c6a16b", zIndex: "1100", pointerEvents: "none"
  });
  bar.setAttribute("aria-hidden", "true");
  let pending = false;
  const update = () => {
    pending = false;
    const total = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    const percent = total ? Math.min(100, Math.max(0, window.scrollY / total * 100)) : 100;
    bar.style.width = percent.toFixed(2) + "%";
  };
  const schedule = () => {
    if (pending) return;
    pending = true;
    requestAnimationFrame(update);
  };
  window.addEventListener("scroll", schedule, {passive: true});
  window.addEventListener("resize", schedule);
  schedule();
})();
