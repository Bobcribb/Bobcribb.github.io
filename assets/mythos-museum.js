/* Native <details> remains usable without JavaScript. Keep its label
   synchronized with the actual disclosure state for assistive technology. */
(() => {
  const menu = document.querySelector('.mythos-menu');
  const summary = menu?.querySelector('summary');
  if (!menu || !summary) return;
  const syncLabel = () => summary.setAttribute(
    'aria-label', menu.open ? 'Fermer le menu' : 'Ouvrir le menu'
  );
  syncLabel();
  menu.addEventListener('toggle', syncLabel);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.open) {
      menu.open = false;
      syncLabel();
      summary.focus();
      event.preventDefault();
    }
  });
  document.addEventListener('click', event => {
    if (menu.open && !menu.contains(event.target)) {
      menu.open = false;
      syncLabel();
    }
  });
})();

/* The home-page figure must describe the DEPLOYED catalogue, not the rapidly
   changing branch main. A small public verification manifest is authoritative;
   the static HTML figure remains visible if JavaScript or fetch fails. */
(() => {
  const label = document.querySelector('[data-corpus-count]');
  if (!label || typeof fetch !== 'function') return;
  fetch('/catalog/publication-verification.json', {cache: 'no-store'})
    .then(response => {
      if (!response.ok) throw new Error('Manifest not available');
      return response.json();
    })
    .then(manifest => {
      const count = manifest && manifest.indexed_documents;
      const commit = manifest && manifest.source_commit;
      if (!Number.isSafeInteger(count) || count < 500 ||
          typeof commit !== 'string' || !/^[0-9a-f]{40}$/i.test(commit)) return;
      label.textContent = `${count.toLocaleString('fr-FR')} entrées disponibles dans le catalogue publié · textes et archives conservés.`;
      label.dataset.corpusCountSource = 'public-verification';
      label.setAttribute('aria-live', 'polite');
    })
    .catch(() => { /* Preserve the server-rendered figure, including offline. */ });
})();
