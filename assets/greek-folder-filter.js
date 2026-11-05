/* MYTHOS — consultation locale des dossiers, sans modifier les textes.
   Progressive enhancement: en l'absence de JavaScript, tous les liens restent visibles. */
(() => {
  'use strict';
  const fold = value => String(value || '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLocaleLowerCase('fr').replace(/\s+/g, ' ').trim();

  function init(filter) {
    const input = filter.querySelector('input[type="search"]');
    const status = filter.querySelector('[data-greek-filter-count]');
    const clear = filter.querySelector('[data-greek-filter-clear]');
    const nav = document.querySelector('nav.greek-folder-toc');
    const sections = Array.from(document.querySelectorAll(
      'section.portal-section[id^="theme-"]'
    ));
    if (!input || !status || !clear || !nav || !sections.length) return;

    const groups = sections.map(section => {
      const heading = fold(section.querySelector('h2')?.textContent);
      const entries = Array.from(section.querySelectorAll('ol.greek-folder-links > li'))
        .map(li => ({ li, searchable: fold(heading + ' ' + li.textContent) }));
      const navItem = Array.from(nav.querySelectorAll('a[href]'))
        .find(anchor => anchor.getAttribute('href') === '#' + section.id)?.closest('li');
      return { section, navItem, entries };
    });
    const total = groups.reduce((sum, group) => sum + group.entries.length, 0);
    if (!total) return;
    filter.hidden = false;

    function update() {
      const terms = fold(input.value).split(' ').filter(Boolean);
      let visible = 0;
      groups.forEach(({section, navItem, entries}) => {
        let groupVisible = 0;
        entries.forEach(({li, searchable}) => {
          const matched = terms.every(term => searchable.includes(term));
          li.hidden = !matched;
          if (matched) groupVisible++;
        });
        section.hidden = groupVisible === 0;
        if (navItem) navItem.hidden = groupVisible === 0;
        visible += groupVisible;
      });
      status.textContent = terms.length
        ? visible + ' résultat' + (visible > 1 ? 's' : '') + ' sur ' + total
        : total + ' textes et sections disponibles';
      clear.hidden = !terms.length;
    }
    input.addEventListener('input', update);
    input.addEventListener('keydown', event => {
      if (event.key === 'Escape' && input.value) {
        input.value = '';
        update();
        event.preventDefault();
      }
    });
    clear.addEventListener('click', () => {
      input.value = '';
      update();
      input.focus();
    });
    window.addEventListener('hashchange', () => {
      const target = window.location.hash.slice(1);
      if (target.startsWith('theme-') && document.getElementById(target)?.hidden) {
        input.value = '';
        update();
      }
    });
    update();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      document.querySelectorAll('[data-greek-folder-filter]').forEach(init);
    }, {once: true});
  } else {
    document.querySelectorAll('[data-greek-folder-filter]').forEach(init);
  }
})();
