#!/usr/bin/env node
// MYTHOS: real behaviour of the shared menu script without browser dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const script = fs.readFileSync(
  path.join(__dirname, '..', 'assets', 'mythos-museum.js'), 'utf8'
);

function createScene({hasMenu = true, initialOpen = false} = {}) {
  const docListeners = new Map();
  const menuListeners = new Map();
  const attributes = new Map();
  let focusCount = 0;
  const inside = {};
  const summary = {
    setAttribute: (name, value) => attributes.set(name, value),
    focus: () => { focusCount += 1; }
  };
  const menu = {
    open: initialOpen,
    querySelector: selector => selector === 'summary' ? summary : null,
    addEventListener: (name, listener) => menuListeners.set(name, listener),
    contains: target => target === summary || target === inside
  };
  const document = {
    querySelector: selector => {
      if (selector === '.mythos-menu') return hasMenu ? menu : null;
      if (selector === '[data-corpus-count]') return null;
      return null;
    },
    addEventListener: (name, listener) => docListeners.set(name, listener)
  };
  vm.runInNewContext(script, {document}, {filename: 'mythos-museum.js'});
  return {
    menu, summary, inside,
    label: () => attributes.get('aria-label'),
    focusCount: () => focusCount,
    emitMenu: (name, event) => menuListeners.get(name)?.(event),
    emitDocument: (name, event) => docListeners.get(name)?.(event)
  };
}

{
  const stage = createScene();
  assert.equal(stage.label(), 'Ouvrir le menu');
  stage.menu.open = true;
  stage.emitMenu('toggle', {});
  assert.equal(stage.label(), 'Fermer le menu');

  stage.emitDocument('click', {target: stage.inside});
  assert.equal(stage.menu.open, true, 'An inside click must not close the menu');
  assert.equal(stage.label(), 'Fermer le menu');

  stage.emitDocument('click', {target: {}});
  assert.equal(stage.menu.open, false, 'An outside click must close the menu');
  assert.equal(stage.label(), 'Ouvrir le menu');

  stage.menu.open = true;
  stage.emitMenu('toggle', {});
  let prevented = false;
  stage.emitDocument('keydown', {
    key: 'Escape',
    preventDefault: () => { prevented = true; }
  });
  assert.equal(stage.menu.open, false, 'Escape must close the menu');
  assert.equal(stage.label(), 'Ouvrir le menu');
  assert.equal(stage.focusCount(), 1, 'Focus must return to the summary');
  assert.equal(prevented, true);
}
{
  const opened = createScene({initialOpen: true});
  assert.equal(opened.label(), 'Fermer le menu');
  opened.menu.open = false;
  opened.emitMenu('toggle', {});
  assert.equal(opened.label(), 'Ouvrir le menu');
}
{
  // Pages without a shared menu remain unaffected.
  createScene({hasMenu: false});
}
console.log('OK: MYTHOS menu state, keyboard, pointer and accessible labels');
