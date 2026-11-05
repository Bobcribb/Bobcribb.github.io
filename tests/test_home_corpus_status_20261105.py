"""Le compteur de l'accueil suit le manifeste de la version effectivement publiée."""
import json
from pathlib import Path
import shutil
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class HomeCorpusStatusTests(unittest.TestCase):
    def test_home_retains_a_static_fallback_and_manifest_source(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('id="corpus-status"', html)
        self.assertIn('data-corpus-count=""', html)
        manifest = json.loads((ROOT / "catalog/publication-verification.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(manifest["indexed_documents"], 500)
        self.assertRegex(manifest["source_commit"], r"^[0-9a-f]{40}$")
        self.assertIn("/catalog/publication-verification.json",
                      (ROOT / "assets/mythos-museum.js").read_text(encoding="utf-8"))

    @unittest.skipUnless(shutil.which("node"), "Node.js requis pour tester le script navigateur")
    def test_verified_manifest_and_offline_fallback(self):
        simulation = r"""
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(process.argv[1], 'utf8');
async function run(mode) {
  const label = {
    textContent: 'Nombre initial du HTML', dataset: {},
    setAttribute(key, value) { this[key] = value; }
  };
  let requests = 0;
  const sandbox = {
    document: {querySelector(selector) {
      return selector === '[data-corpus-count]' && mode !== 'other-page' ? label : null;
    }},
    fetch(url, options) {
      requests++;
      if (url !== '/catalog/publication-verification.json' ||
          options.cache !== 'no-store') throw Error('Unexpected manifest endpoint');
      if (mode === 'offline') return Promise.reject(Error('Network unavailable'));
      const value = mode === 'bad-receipt'
        ? {indexed_documents: 900, source_commit: 'unverified'}
        : {indexed_documents: 1518, source_commit: 'a'.repeat(40)};
      return Promise.resolve({ok: true, json: () => Promise.resolve(value)});
    }
  };
  vm.runInNewContext(source, sandbox);
  await new Promise(resolve => setTimeout(resolve, 0));
  return {text: label.textContent, source: label.dataset.corpusCountSource || '',
          live: label['aria-live'] || '', requests};
}
(async () => {
  const good = await run('valid'), bad = await run('bad-receipt');
  const offline = await run('offline'), other = await run('other-page');
  if (!good.text.includes('518') || !good.text.includes('catalogue publié') ||
      good.source !== 'public-verification' || good.live !== 'polite' ||
      good.requests !== 1) throw Error('Valid public count not applied: ' + JSON.stringify(good));
  for (const item of [bad, offline, other])
    if (item.text !== 'Nombre initial du HTML' || item.source !== '')
      throw Error('Static fallback was lost: ' + JSON.stringify(item));
  if (other.requests !== 0) throw Error('Unnecessary request on other pages');
  console.log(JSON.stringify({good, bad, offline, other}));
})().catch(error => {console.error(error); process.exitCode = 1});
"""
        result = subprocess.run(
            ["node", "-e", simulation, str(ROOT / "assets/mythos-museum.js")],
            cwd=ROOT, text=True, capture_output=True, timeout=15, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["good"]["requests"], 1)


if __name__ == "__main__":
    unittest.main()
