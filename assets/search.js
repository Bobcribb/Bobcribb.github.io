document.addEventListener('DOMContentLoaded', () => {
  const input = document.querySelector('[data-search]');
  const results = document.querySelector('[data-results]');
  if (!input || !results) return;
  let documents = [];
  const norm = s => (s || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const draw = () => {
    const query = norm(input.value.trim());
    const found = query
      ? documents.filter(x => norm(x.title + ' ' + x.excerpt).includes(query))
      : documents.slice(0, 30);
    results.textContent = '';
    const count = document.createElement('p');
    count.textContent = query
      ? found.length + ' dossier(s) trouvé(s)'
      : documents.length + ' dossiers dans la bibliothèque';
    results.appendChild(count);
    for (const doc of found.slice(0, 100)) {
      const a = document.createElement('a');
      a.href = doc.url;
      a.textContent = doc.title;
      results.appendChild(a);
    }
  };
  input.addEventListener('input', draw);
  fetch('/search.json')
    .then(r => { if (!r.ok) throw new Error('Index indisponible'); return r.json(); })
    .then(data => { documents = data; draw(); })
    .catch(() => { results.textContent = 'Index de recherche temporairement indisponible.'; });
});