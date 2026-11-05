/* Contrôle navigateur simulé, sans dépendance externe ni source modifiée. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const script = fs.readFileSync(path.join(__dirname, '..', 'assets', 'greek-folder-filter.js'), 'utf8');

function fixture(href) {
  let current = new URL(href);
  const events = {};
  const inputEvents = {};
  const clearEvents = {};
  const sectionA = {id: 'theme-1', hidden: false, title: 'Delphes et l’oracle',
    entries: [{textContent: 'Pythie de Delphes · étude intégrale', hidden: false}]};
  const sectionB = {id: 'theme-2', hidden: false, title: 'Divinités',
    entries: [{textContent: 'Zeus et Héra · étude intégrale', hidden: false}]};
  const sections = [sectionA, sectionB];
  const navItems = sections.map(() => ({hidden: false}));
  for (const section of sections) {
    section.querySelector = selector => selector === 'h2' ? {textContent: section.title} : null;
    section.querySelectorAll = selector =>
      selector === 'ol.greek-folder-links > li' ? section.entries : [];
  }
  const anchors = sections.map((section, i) => ({
    getAttribute: () => '#' + section.id,
    closest: () => navItems[i],
  }));
  const filter = {
    hidden: true,
    querySelector(selector) {
      if (selector === 'input[type="search"]') return input;
      if (selector === '[data-greek-filter-count]') return status;
      if (selector === '[data-greek-filter-clear]') return clear;
      return null;
    },
  };
  const input = {
    value: '',
    focused: false,
    addEventListener: (event, fn) => {inputEvents[event] = fn;},
    focus() {this.focused = true;},
  };
  const status = {textContent: ''};
  const clear = {hidden: true, addEventListener: (event, fn) => {clearEvents[event] = fn;}};
  const nav = {querySelectorAll: selector => selector === 'a[href]' ? anchors : []};
  const document = {
    readyState: 'complete',
    querySelector: selector => selector === 'nav.greek-folder-toc' ? nav : null,
    querySelectorAll(selector) {
      if (selector === '[data-greek-folder-filter]') return [filter];
      if (selector === 'section.portal-section[id^="theme-"]') return sections;
      return [];
    },
    getElementById: id => sections.find(section => section.id === id) || null,
  };
  const location = {
    get href() {return current.href;},
    get pathname() {return current.pathname;},
    get search() {return current.search;},
    get hash() {return current.hash;},
  };
  const history = {
    state: {fixture: true},
    replaceState(state, unused, relative) {
      assert.deepEqual(state, this.state);
      current = new URL(relative, current);
    },
  };
  const window = {
    location, history,
    addEventListener: (event, fn) => {events[event] = fn;},
  };
  vm.runInNewContext(script, {window, document, URL, URLSearchParams});
  return {
    input, status, clear, filter, sections, navItems, inputEvents, clearEvents, events,
    get url() {return current;},
    setURL(url) {current = new URL(url);},
  };
}

{
  const app = fixture('https://bobmythos.fr/mythologie-grecque/dossiers/sources-anciennes/?mode=lecture&filtre=d%C3%A9lphes#theme-1');
  assert.equal(app.filter.hidden, false);
  assert.equal(app.input.value, 'délphes');
  assert.equal(app.sections[0].hidden, false);
  assert.equal(app.sections[1].hidden, true);
  assert.equal(app.status.textContent, '1 résultat sur 2');

  app.input.value = 'Zeus';
  app.inputEvents.input();
  assert.equal(app.sections[0].hidden, true);
  assert.equal(app.sections[1].hidden, false);
  assert.equal(app.url.searchParams.get('mode'), 'lecture');
  assert.equal(app.url.searchParams.get('filtre'), 'Zeus');
  assert.equal(app.url.hash, '#theme-1');

  app.events.hashchange();
  assert.equal(app.input.value, '');
  assert.equal(app.url.searchParams.has('filtre'), false);
  assert.equal(app.sections[0].hidden, false);
  assert.equal(app.navItems[0].hidden, false);

  app.input.value = 'Zeus';
  app.inputEvents.input();
  app.clearEvents.click();
  assert.equal(app.input.value, '');
  assert.equal(app.input.focused, true);
  assert.equal(app.url.searchParams.get('mode'), 'lecture');
  assert.equal(app.url.searchParams.has('filtre'), false);
  assert.equal(app.status.textContent, '2 textes et sections disponibles');

  app.setURL('https://bobmythos.fr/mythologie-grecque/dossiers/sources-anciennes/?filtre=zeus');
  app.events.popstate();
  assert.equal(app.input.value, 'zeus');
  assert.equal(app.sections[1].hidden, false);
  assert.equal(app.sections[0].hidden, true);
}
console.log('Filtre grec : URL partageable, ancres, retour historique et texte inchangé — OK');
