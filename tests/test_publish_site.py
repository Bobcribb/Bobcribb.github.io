"""Régressions avec un vrai dépôt distant local et deux éditeurs concurrents."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('publish_site', Path(__file__).resolve().parents[1] / 'scripts/publish_site.py')
publish = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish)

BUILDER = '''from pathlib import Path
import json, shutil
out=Path('_site')
out.mkdir()
chapters=sorted(Path('chapitres').glob('*.md'))
titles=[p.read_text() for p in chapters]
for p in chapters:
    target=out/'chapitres'/p.stem/'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(p.read_text())
(out/'rubriques').mkdir()
(out/'rubriques/index.html').write_text('|'.join(titles))
(out/'search.json').write_text(json.dumps(titles, ensure_ascii=False))
(out/'sitemap.xml').write_text('<urls>'+'|'.join(titles)+'</urls>')
shutil.copy2('index.html',out/'index.html')
shutil.copytree('media',out/'media')
if len(chapters)==1:
    (out/'first-attempt-only.html').write_text('Must not survive a failed push')
'''
VALIDATOR = '''from pathlib import Path
import json
titles=json.loads(Path('_site/search.json').read_text())
assert titles == [p.read_text() for p in sorted(Path('chapitres').glob('*.md'))]
assert not Path('invalid').exists(), 'Latest source fails validation'
'''


class PublicationTests(unittest.TestCase):
    def command(self, cwd, *args):
        return subprocess.check_output(['git', '-C', str(cwd), *args], stderr=subprocess.STDOUT, text=True).strip()

    def write(self, repo, path, content):
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    def commit(self, repo, message):
        self.command(repo, 'add', '-A')
        self.command(repo, 'commit', '-m', message)
        return self.command(repo, 'rev-parse', 'HEAD')

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.remote, self.editor, self.runner = [self.root / name for name in ('remote.git', 'editor', 'runner')]
        self.environment = patch.dict(os.environ, {
            'GIT_AUTHOR_NAME': 'Test', 'GIT_AUTHOR_EMAIL': 'test@example.invalid',
            'GIT_COMMITTER_NAME': 'Test', 'GIT_COMMITTER_EMAIL': 'test@example.invalid',
            'GITHUB_OUTPUT': '',
        })
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.command(self.root, 'init', '--bare', '--initial-branch=main', str(self.remote))
        self.command(self.root, 'clone', str(self.remote), str(self.editor))
        for path, text in {
            '.gitignore': '_site/\n__pycache__/\n',
            'chapitres/a.md': 'Chapitre A intégral',
            'scripts/build_native.py': BUILDER,
            'scripts/validate_publication.py': VALIDATOR,
            'index.html': 'Article historique conservé',
            'media/photo.txt': 'Média original conservé',
            'rubriques/index.html': 'Ancien catalogue',
            'search.json': '[]', 'sitemap.xml': '<urls/>',
        }.items():
            self.write(self.editor, path, text)
        # The numbering worker runs before the builder even in isolated fixtures.
        from test_editorial_queue import initialize
        initialize(self.editor)
        queue_source = Path(__file__).resolve().parents[1] / 'scripts/editorial_queue.py'
        self.write(self.editor, 'scripts/editorial_queue.py', queue_source.read_text())
        history_source = queue_source.with_name('comparative_history.py')
        self.write(self.editor, 'scripts/comparative_history.py', history_source.read_text())
        self.initial = self.commit(self.editor, 'Initial sources')
        self.command(self.editor, 'push', 'origin', 'main')
        self.command(self.root, 'clone', '--depth=1', self.remote.as_uri(), str(self.runner))

    def head(self):
        return self.command(self.remote, 'rev-parse', 'main')

    def race(self, *, invalid=False, always=False):
        # Le hook client publie une édition concurrente juste avant le push
        # du rendu, provoquant un vrai rejet non-fast-forward côté distant.
        hook = self.runner / '.git/hooks/pre-push'
        hook.write_text(f'''#!{sys.executable}
from pathlib import Path
import os, subprocess
editor=Path({str(self.editor)!r})
marker=Path({str(self.root / 'raced')!r})
if marker.exists() and not {always!r}:
    raise SystemExit(0)
local_vars=subprocess.check_output(['git','rev-parse','--local-env-vars'],text=True).splitlines()
env={{key:value for key,value in os.environ.items() if key not in local_vars}}
def git(*args):
    subprocess.run(['git','-C',str(editor),*args],check=True,stdout=subprocess.DEVNULL,env=env)
git('pull','--ff-only','origin','main')
n=int(marker.read_text())+1 if marker.exists() else 1
(editor/'chapitres/b.md').write_text('Chapitre B récent '+str(n))
(editor/'index.html').write_text('Article historique enrichi')
(editor/'media/photo.txt').write_text('Média récent conservé')
for name in ('rubriques/index.html','search.json','sitemap.xml'):
    (editor/name).write_text('Catalogue concurrent '+str(n))
if {invalid!r}:
    (editor/'invalid').write_text('Validation must fail')
git('add','-A')
git('commit','-m','Concurrent editorial update')
git('push','origin','main')
marker.write_text(str(n))
''')
        hook.chmod(0o755)

    def test_concurrent_edit_rebuilt_without_losing_sources_or_stale_files(self):
        self.race()
        published = publish.synchronize(self.runner)
        self.assertEqual(self.head(), published)
        self.assertEqual(self.command(self.remote, 'show', 'main:chapitres/a.md'), 'Chapitre A intégral')
        self.assertEqual(self.command(self.remote, 'show', 'main:chapitres/b.md'), 'Chapitre B récent 1')
        self.assertEqual(self.command(self.remote, 'show', 'main:index.html'), 'Article historique enrichi')
        self.assertEqual(self.command(self.remote, 'show', 'main:media/photo.txt'), 'Média récent conservé')
        for name in ('rubriques/index.html', 'search.json', 'sitemap.xml'):
            remote = self.command(self.remote, 'show', 'main:' + name)
            self.assertIn('Chapitre B récent 1', remote)
            self.assertEqual((self.runner / '_site' / name).read_text().strip(), remote)
        self.assertNotIn('first-attempt-only.html', self.command(self.remote, 'ls-tree', '-r', '--name-only', 'main'))
        self.command(self.remote, 'merge-base', '--is-ancestor', self.command(self.editor, 'rev-parse', 'HEAD'), 'main')
        self.assertEqual(self.command(self.runner, 'rev-parse', 'HEAD'), self.initial)
        self.assertEqual(self.command(self.runner, 'status', '--porcelain'), '')

    def test_no_change_does_not_create_an_extra_commit(self):
        first = publish.synchronize(self.runner)
        second = publish.synchronize(self.runner)
        self.assertEqual(first, second)
        self.assertTrue((self.runner / '_site/search.json').is_file())

    def test_concurrent_update_is_detected_even_when_render_is_unchanged(self):
        publish.synchronize(self.runner)
        original_latest = publish.latest_main
        calls = 0

        def latest(repo):
            nonlocal calls
            calls += 1
            if calls == 2:
                self.command(self.editor, 'pull', '--ff-only', 'origin', 'main')
                self.write(self.editor, 'chapitres/b.md', 'Chapitre ajouté sans push du rendu')
                self.commit(self.editor, 'Update during unchanged render')
                self.command(self.editor, 'push', 'origin', 'main')
            return original_latest(repo)

        with patch.object(publish, 'latest_main', side_effect=latest):
            publish.synchronize(self.runner)
        self.assertIn('Chapitre ajouté sans push du rendu', (self.runner / '_site/search.json').read_text())
        self.assertGreaterEqual(calls, 4)

    def test_latest_sources_are_validated_after_a_rejected_push(self):
        self.race(invalid=True)
        with self.assertRaises(subprocess.CalledProcessError):
            publish.synchronize(self.runner)
        self.assertEqual(self.head(), self.command(self.editor, 'rev-parse', 'HEAD'))
        self.assertFalse((self.runner / '_site').exists())

    def test_repeated_concurrent_writes_exhaust_without_deploying_old_artifact(self):
        self.race(always=True)
        with self.assertRaisesRegex(RuntimeError, 'aucun artefact obsolète'):
            publish.synchronize(self.runner, max_attempts=2)
        self.assertEqual(self.head(), self.command(self.editor, 'rev-parse', 'HEAD'))
        self.assertFalse((self.runner / '_site').exists())

    def test_source_changes_by_builder_are_rejected(self):
        self.write(self.editor, 'scripts/build_native.py', BUILDER + "\n(out/'notes.md').write_text('Unexpected source')\n")
        tip = self.commit(self.editor, 'Broken builder')
        self.command(self.editor, 'push', 'origin', 'main')
        with self.assertRaisesRegex(RuntimeError, 'source ou média modifié'):
            publish.synchronize(self.runner)
        self.assertEqual(self.head(), tip)

    def test_deletions_by_builder_are_rejected(self):
        self.write(self.editor, 'scripts/build_native.py', BUILDER + "\nPath('index.html').unlink()\n(out/'index.html').unlink()\n")
        tip = self.commit(self.editor, 'Broken deletion')
        self.command(self.editor, 'push', 'origin', 'main')
        with self.assertRaisesRegex(RuntimeError, 'suppression'):
            publish.synchronize(self.runner)
        self.assertEqual(self.head(), tip)

    def test_permission_failure_is_not_reported_as_a_concurrent_edit(self):
        hook = self.remote / 'hooks/pre-receive'
        hook.write_text('#!/bin/sh\nexit 1\n')
        hook.chmod(0o755)
        with self.assertRaisesRegex(RuntimeError, 'sans modification de main'):
            publish.synchronize(self.runner)
        self.assertEqual(self.head(), self.initial)
        self.assertFalse((self.runner / '_site').exists())

    def test_dirty_checkout_is_preserved_and_not_published(self):
        self.write(self.runner, 'chapitres/local.md', 'Travail non publié')
        with self.assertRaisesRegex(RuntimeError, 'modifications locales'):
            publish.synchronize(self.runner)
        self.assertEqual((self.runner / 'chapitres/local.md').read_text(), 'Travail non publié')
        self.assertEqual(self.head(), self.initial)


if __name__ == '__main__':
    unittest.main()
