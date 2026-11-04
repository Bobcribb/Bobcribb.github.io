#!/usr/bin/env python3
"""Organize the verified Greek inventory without moving or rewriting a manuscript.

Each existing page or book section has one primary thematic home. Editorial
rules use the subject of the title/path, never incidental words in the prose.
Unrecognized future studies remain visible in an explicit sorting queue.
"""
from collections import Counter, defaultdict
from html import escape
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import unicodedata

from bs4 import BeautifulSoup

BASE = '/mythologie-grecque/dossiers/'
FOLDERS = [
    ('cosmogonies', 'Cosmogonies', 'Naissance du monde, générations divines, Hésiode et souveraineté de Zeus.'),
    ('divinites', 'Divinités', 'Olympiens, dieux des Enfers, puissances de la nature et personnifications.'),
    ('heros', 'Héros et héroïnes', 'Héraclès, Thésée, Persée, Chiron, épreuves et métamorphoses.'),
    ('familles', 'Grandes familles mythologiques', 'Lignées attiques, Labdacides, Atrides, filiation et transmission du pouvoir.'),
    ('cycles-epiques', 'Cycles épiques', 'Argonautiques, cycle troyen, Iliade, Odyssée et retours héroïques.'),
    ('cultes-sanctuaires', 'Cultes et sanctuaires', 'Delphes, Délos, Éleusis, fêtes, oracles, mystères et pratiques religieuses.'),
    ('sources-anciennes', 'Sources anciennes', 'Textes, auteurs, documents, atlas, vocabulaire et bibliographies.'),
    ('interpretations-philosophiques', 'Interprétations philosophiques', 'Études des épopées, concepts, historiographie et méthodes de lecture des mythes.'),
]
FOLDER_TITLES = {slug: title for slug, title, _ in FOLDERS}

# Sub-dossiers follow the subject and retain the order of the original books.
BOOK_HOME = {
    'livre-hesiode': ('cosmogonies', 'Lire Hésiode'),
    'livre-dieux': ('dieux', 'Comprendre le polythéisme'),
    'monographies': ('dieux', 'Les Olympiens et les dieux des Enfers'),
    'livre-heracles': ('heracles', 'Les travaux et le parcours d’Héraclès'),
    'livre-thebes': ('thebes', 'Le cycle thébain'),
    'livre-argonautiques': ('argonautes', 'Lire les Argonautiques'),
    'livre-troie': ('troie-iliade', 'Le cycle de Troie'),
    'iliade': ('troie-iliade', 'L’Iliade, chant par chant'),
    'livre-iliade-scenes': ('troie-iliade', 'L’Iliade, scène par scène'),
    'livre-odyssee': ('odyssee', 'L’Odyssée, chant par chant'),
    'odyssee': ('odyssee', 'L’Odyssée, thèmes et analyses'),
    'livre-atrides': ('atrides', 'Le cycle des Atrides'),
    'atlas-mythologique': ('sources', 'Atlas et géographie'),
    'cultes-cites': ('sanctuaires', 'Cultes et cités'),
    'sources-methodes': ('sources', 'Sources et méthodes'),
    'ecole-paris': ('sources', 'Historiographie et école de Paris'),
    'historiographie-v6': ('sources', 'Historiographie et école de Paris'),
    'bibliotheque': ('sources', 'Repères et bibliothèques'),
}
HERO_HOME = {
    'heracles': ('heracles', 'Le héros et son entourage'),
    'thesee': ('athenes-thesee', 'Thésée et ses descendants'),
    'oedipe': ('thebes', 'Œdipe, Antigone et les Labdacides'),
    'antigone': ('thebes', 'Œdipe, Antigone et les Labdacides'),
    'jason': ('argonautes', 'Jason et Médée'),
    'medee': ('argonautes', 'Jason et Médée'),
    'achille': ('troie-iliade', 'Héros et généalogies de Troie'),
    'hector': ('troie-iliade', 'Héros et généalogies de Troie'),
    'helene': ('troie-iliade', 'Héros et généalogies de Troie'),
    'ulysse': ('odyssee', 'Ulysse, Pénélope et Ithaque'),
    'penelope': ('odyssee', 'Ulysse, Pénélope et Ithaque'),
    'oreste': ('atrides', 'Oreste et la justice'),
    'atalante': ('heros', 'Chasse, épreuves et métamorphoses'),
    'persee': ('heros', 'Persée et les autres héros'),
    'orphee': ('heros', 'Orphée et les passages vers l’au-delà'),
}
CHAPTER_RULES = [
    (r'^(nyx|gaia|titanomachie|typhon|gigantomachie)\b', 'cosmogonies', 'Générations divines et conflits de souveraineté'),
    (r'^(promethee|hypnos)\b', 'cosmogonies', 'Condition humaine, mort et destin'),
    (r'^(helios|asteria|pan|satyres)\b', 'dieux', 'Puissances de la nature'),
    (r'^(tyche|hymenaios|ilithyie|aidos|eleos|pheme|hebe)\b', 'dieux', 'Puissances de la vie et de la cité'),
    (r'^(pholos|nessos|atlas|hesperides)\b', 'heracles', 'Le héros et son entourage'),
    (r'^(chiron|ixion|lapithes|cenee)\b', 'heros', 'Chiron, les Lapithes et les Centaures'),
    (r'^(acteon|atalante|orion)\b', 'heros', 'Chasse, épreuves et métamorphoses'),
    (r'^(pelee|achille)\b', 'troie-iliade', 'Héros et généalogies de Troie'),
    (r'^harmonia\b', 'thebes', 'Cadmos et Harmonie'),
    (r'^(asclepios)\b', 'sanctuaires', 'Oracles et guérison'),
    (r'^(triptoleme)\b', 'sanctuaires', 'Éleusis et les mystères'),
    (r'^(navire sacre delos|apollon delien|callimaque delos|hyperboreens)\b', 'sanctuaires', 'Délos, Apollon et Artémis'),
    (r'^(apollon python|pythie|maximes delphiques|omphalos|tresors delphes|aurige delphes|pindare odes)\b', 'sanctuaires', 'Delphes et l’oracle d’Apollon'),
    (r'^daphne\b', 'dieux', 'Apollon, Artémis et leurs récits'),
    (r'^(pandrose|athena polias|erichthonios|boutes|fetes civiques|ares alcippe|athena poseidon)\b', 'athenes-thesee', 'Fêtes, cultes et institutions d’Athènes'),
    (r'^(androgee|thesee ariane|ariane dionysos)\b', 'athenes-thesee', 'La Crète, Ariane et le labyrinthe'),
    (r'^(egee|pallantides|thesee|decheance thesee|descendants thesee|hippolyte|hecale|hippothoon|medee athenes|navire thesee)\b', 'athenes-thesee', 'Thésée et ses descendants'),
    (r'^(pandion|erechthee|orithyie|procris|creuse|cecrops|leos|melanthos|codros|ion xouthos|cecropides|hyacinthides)\b', 'athenes-thesee', 'Rois fondateurs et généalogies attiques'),
]


def normalized(text):
    text = unicodedata.normalize('NFKD', text.lower().replace('œ', 'oe'))
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', text).strip()


def _classify_subject(url, title, kind):
    """Give one primary home; unsupported future topics remain visible."""
    path = urlsplit(url).path
    slug = path.strip('/').removesuffix('.html')
    if kind == 'Archive':
        book = Path(path).stem
        return BOOK_HOME.get(book, ('sources', 'Repères et bibliothèques'))[0], 'Archives historiques'
    if path.startswith('/chapitres/encyclopedie/'):
        subject = normalized(re.sub(r'^chapitre-\d+-', '', path.strip('/').split('/')[-1]))
        for pattern, folder, section in CHAPTER_RULES:
            if re.search(pattern, subject):
                return folder, section
        for hero, home in HERO_HOME.items():
            if subject == hero or subject.startswith(hero+' '):
                return home
        if re.match(r'^(zeus|hera|poseidon|demeter|athena|apollon|artemis|ares|aphrodite|hephaistos|hermes|dionysos|hestia|hades|persephone|hebe)\b', subject):
            return 'dieux', 'Les Olympiens et les dieux des Enfers'
        return 'sources', 'Nouvelles études à classer'
    if kind == 'Section de livre' and slug == 'monographies':
        return HERO_HOME.get(normalized(title), BOOK_HOME['monographies'])
    if slug in BOOK_HOME:
        return BOOK_HOME[slug]
    if slug.startswith('dieu-') or 'aphrodite-etude-integrale' in slug:
        return 'dieux', 'Les Olympiens et les dieux des Enfers'
    if slug.startswith('heros-'):
        return HERO_HOME.get(slug[6:], ('heros', 'Persée et les autres héros'))
    if slug in ('philosophie-iliade', 'philosophie-odyssee', 'philosophie-theogonie'):
        return {'philosophie-iliade': 'troie-iliade', 'philosophie-odyssee': 'odyssee', 'philosophie-theogonie': 'cosmogonies'}[slug], 'Analyses philosophiques'
    if any(x in slug for x in ('delphes', 'pythie')):
        return 'sanctuaires', 'Delphes et l’oracle d’Apollon'
    if 'delos' in slug:
        return 'sanctuaires', 'Délos, Apollon et Artémis'
    if any(x in slug for x in ('eleusis', 'samothrace')):
        return 'sanctuaires', 'Éleusis et les mystères'
    if any(x in slug for x in ('epidaure', 'amphiaraion', 'dodone')):
        return 'sanctuaires', 'Oracles et guérison'
    if any(x in slug for x in ('olympie', 'nemee', 'isthmia', 'brauron', 'artemis-ephese')):
        return 'sanctuaires', 'Sanctuaires, fêtes et concours'
    if any(x in slug for x in ('orphee', 'derveni')):
        return 'heros', 'Orphée et les passages vers l’au-delà'
    if 'bacchantes' in slug:
        return 'thebes', 'Dionysos et les Bacchantes'
    if 'demodocos' in slug:
        return 'odyssee', 'L’Odyssée, thèmes et analyses'
    if 'hecate' in slug:
        return 'dieux', 'Puissances de la nature'
    if 'sappho' in slug or slug in ('textes', 'bibliographie', 'glossaire'):
        return 'sources', 'Textes, vocabulaire et bibliographies'
    if slug in ('grece', 'chronologie'):
        return 'sources', 'Atlas et géographie'
    if slug == 'religion':
        return 'sanctuaires', 'Cultes et cités'
    if slug in ('bestiaire', 'recits'):
        return 'heros', 'Persée et les autres héros'
    return 'sources', 'Repères et bibliothèques'



def classify(url, title, kind):
    """Eight thematic families, with explicit subject subfolders underneath."""
    old, section = _classify_subject(url, title, kind)
    slug = urlsplit(url).path.strip('/').removesuffix('.html')
    subject = normalized(re.sub(r'^chapitre-\d+-', '', slug.split('/')[-1]))
    if slug.startswith('philosophie-'):
        return 'interpretations-philosophiques', 'Analyses philosophiques des épopées'
    if slug in ('ecole-paris', 'historiographie-v6', 'sources-methodes'):
        return 'interpretations-philosophiques', 'Historiographie et méthodes d’interprétation'
    if slug.startswith('chapitres/encyclopedie/') and re.match(r'^(tyche|aidos|eleos|maximes delphiques)\b', subject):
        return 'interpretations-philosophiques', 'Destin, connaissance de soi et valeurs morales'
    if slug.startswith('chapitres/encyclopedie/') and re.match(r'^(callimaque|pindare|pheme)\b', subject):
        return 'sources-anciennes', 'Poésie, rhétorique et parole publique'
    if old == 'athenes-thesee':
        if section.startswith('Fêtes'):
            return 'cultes-sanctuaires', section
        if section.startswith('Rois'):
            return 'familles', section
        return 'heros', section
    mapping = {'cosmogonies': 'cosmogonies', 'dieux': 'divinites',
               'heracles': 'heros', 'heros': 'heros', 'thebes': 'familles',
               'atrides': 'familles', 'argonautes': 'cycles-epiques',
               'troie-iliade': 'cycles-epiques', 'odyssee': 'cycles-epiques',
               'sanctuaires': 'cultes-sanctuaires', 'sources': 'sources-anciennes'}
    if old == 'heracles':
        section = 'Héraclès — ' + section
    elif old in ('argonautes', 'troie-iliade', 'odyssee', 'atrides', 'thebes'):
        section = {'argonautes': 'Argonautiques', 'troie-iliade': 'Troie et Iliade',
                   'odyssee': 'Odyssée', 'atrides': 'Atrides', 'thebes': 'Thèbes'}[old] + ' — ' + section
    return mapping[old], section


RELATED_FOLDERS = {
    'cosmogonies': ['divinites', 'sources-anciennes', 'interpretations-philosophiques'],
    'divinites': ['cosmogonies', 'cultes-sanctuaires', 'heros'],
    'heros': ['familles', 'cycles-epiques', 'cultes-sanctuaires'],
    'familles': ['heros', 'cycles-epiques', 'interpretations-philosophiques'],
    'cycles-epiques': ['heros', 'familles', 'interpretations-philosophiques'],
    'cultes-sanctuaires': ['divinites', 'sources-anciennes', 'cosmogonies'],
    'sources-anciennes': ['cycles-epiques', 'cosmogonies', 'interpretations-philosophiques'],
    'interpretations-philosophiques': ['sources-anciennes', 'cycles-epiques', 'cosmogonies'],
}


# Preserve previously published dossier addresses when consolidating the
# navigation into eight thematic families. No manuscript is redirected here.
LEGACY_FOLDERS = {
    'dieux': 'divinites', 'heracles': 'heros', 'athenes-thesee': 'heros',
    'thebes': 'familles', 'atrides': 'familles', 'argonautes': 'cycles-epiques',
    'troie-iliade': 'cycles-epiques', 'odyssee': 'cycles-epiques',
    'sanctuaires': 'cultes-sanctuaires', 'sources': 'sources-anciennes',
}


def inventory(groups, sections, books):
    """Deduplicate exact destinations, distinguishing pages from deep sections."""
    kinds = {'grec-livres': 'Livre', 'grec-archives': 'Archive',
             'grec-universitaire': 'Chapitre universitaire', 'grec-monographies': 'Étude',
             'grec-dieux': 'Notice', 'grec-heros': 'Notice',
             'grec-dossiers': 'Dossier documentaire', 'grec-liens': 'Lecture associée'}
    rows, seen = [], set()

    def add(url, title, kind, book=None):
        if url in seen:
            return
        seen.add(url)
        folder, section = classify(url, title, kind)
        rows.append(dict(url=url, title=title, kind=kind, folder=folder, section=section, book=book))

    for _, key, items in groups:
        for url, title in items:
            add(url, title, kinds[key])
    for (book_title, entries), (_, slug) in zip(sections, books):
        for url, title in entries:
            add(url, title, 'Section de livre', book_title)
    return rows


def counts(rows, compact=False):
    tally = Counter(r['kind'] for r in rows)
    labels = [('Chapitre universitaire', 'étude numérotée', 'études numérotées'),
              ('Section de livre', 'section de livre', 'sections de livres')]
    if compact:
        tally['Documents'] = len(rows)-tally['Chapitre universitaire']-tally['Section de livre']
        labels.append(('Documents', 'document associé', 'documents associés'))
    else:
        labels += [('Livre', 'livre', 'livres'), ('Notice', 'notice', 'notices'),
                   ('Étude', 'étude', 'études'), ('Dossier documentaire', 'dossier documentaire', 'dossiers documentaires'),
                   ('Lecture associée', 'lecture associée', 'lectures associées'), ('Archive', 'archive', 'archives')]
    return ' · '.join(str(tally[k])+' '+(singular if tally[k] == 1 else plural)
                      for k, singular, plural in labels if tally[k])


def cards_html(rows):
    return '<div class="portal-grid greek-folder-grid">' + ''.join(
        '<a class="portal-card" href="'+BASE+slug+'/"><span class="portal-card-kicker">DOSSIER THÉMATIQUE</span>'
        '<strong>'+escape(title)+'</strong><span>'+escape(description)+'</span><small>'
        +escape(counts([r for r in rows if r['folder'] == slug], compact=True))+'</small>'
        '<span class="card-indicator" aria-hidden="true">↗</span></a>'
        for slug, title, description in FOLDERS if any(r['folder'] == slug for r in rows)) + '</div>'


def overview(rows):
    return ('<section id="dossiers-thematiques" class="portal-section"><h2>Choisir un dossier thématique</h2>'
            '<p class="portal-lead">Entrez par un personnage, un cycle ou un thème, puis ouvrez les chapitres qui s’y rapportent.</p>'
            '<p>' + escape(counts(rows)) + '. Les sections sont des passages des livres, accessibles directement à leur titre.</p>'
            + cards_html(rows) + '</section>')


def build(out, groups, sections, books):
    from build_navigation import shell
    out = Path(out)
    rows = inventory(groups, sections, books)
    def render(title, body, description=''):
        return shell(title, body, description).replace('</head>', '<style id="greek-folder-style">'+CSS+'</style></head>')
    (out / BASE.strip('/')).mkdir(parents=True, exist_ok=True)
    index = '<h1>Les dossiers de l’encyclopédie grecque</h1><p><a href="/mythologie-grecque/">Encyclopédie grecque</a></p>' + overview(rows)
    (out / BASE.strip('/') / 'index.html').write_text(render('Dossiers thématiques de l’encyclopédie grecque', index), encoding='utf-8')
    # Return links stay outside the article, leaving its scholarly text untouched.
    for row in rows:
        if row['kind'] not in ('Chapitre universitaire', 'Livre', 'Notice', 'Étude'):
            continue
        page = out / row['url'].lstrip('/')
        if row['url'].endswith('/'):
            page /= 'index.html'
        doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        main = doc.main
        if main is None:
            continue  # Minimal test fixtures may only contain a heading.
        for old in doc.select('[data-greek-folder-nav]'):
            old.decompose()
        folder = row['folder']
        nav = BeautifulSoup('<nav class="greek-folder-breadcrumb" data-greek-folder-nav="true" aria-label="Dossier de cette étude">'
                            '<a href="/mythologie-grecque/">Encyclopédie grecque</a> · <a href="'+BASE+folder+'/">'
                            +escape(FOLDER_TITLES[folder])+'</a></nav>', 'html.parser').nav
        main.insert(0, nav)
        page.write_text(str(doc), encoding='utf-8')
    for slug, title, description in FOLDERS:
        members = [r for r in rows if r['folder'] == slug]
        if not members:
            continue
        subsets = defaultdict(list)
        for row in members:
            subsets[row['section']].append(row)
        body = '<nav aria-label="Fil d’Ariane"><a href="/mythologie-grecque/">Encyclopédie grecque</a> · <a href="'+BASE+'">Tous les dossiers</a></nav>'
        body += '<h1>'+escape(title)+'</h1><p class="portal-lead">'+escape(description)+'</p><p>'+escape(counts(members))+'.</p>'
        body += '<p>Choisissez un sous-dossier. Les liens ouvrent les textes complets ou la section exacte du livre indiqué.</p>'
        body += '<nav class="greek-folder-toc" aria-label="Sous-dossiers"><ul>'+''.join(
            '<li><a href="#theme-'+str(i)+'">'+escape(name)+' ('+str(len(items))+')</a></li>'
            for i, (name, items) in enumerate(subsets.items(), 1))+'</ul></nav>'
        for i, (name, items) in enumerate(subsets.items(), 1):
            body += '<section class="portal-section" id="theme-'+str(i)+'"><h2>'+escape(name)+'</h2>'
            if name == 'Nouvelles études à classer':
                body += '<p>Ces études récentes restent consultables ici en attendant leur rattachement à un sujet précis.</p>'
            body += '<ol class="greek-folder-links">'
            for row in items:
                context = row['kind'] + (' · '+row['book'] if row['book'] else '')
                body += '<li><a data-greek-entry="'+escape(row['kind'], quote=True)+'" href="'+escape(row['url'], quote=True)+'">'+escape(row['title'])+'</a><small>'+escape(context)+'</small></li>'
            body += '</ol></section>'
        body += '<aside class="greek-related"><h2>Renvois vers les thèmes associés</h2><ul>' + ''.join(
            '<li><a href="'+BASE+related+'/">'+escape(FOLDER_TITLES[related])+'</a></li>'
            for related in RELATED_FOLDERS[slug]
            if any(r['folder'] == related for r in rows)) + '</ul></aside>'
        body += '<p><a href="'+BASE+'">Revenir aux dossiers thématiques</a> · <a href="/mythologie-grecque/#catalogue-complet">Catalogue intégral</a></p>'
        target = out / BASE.strip('/') / slug / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(title+' — dossier mythologique', body, description), encoding='utf-8')
    for legacy, current in LEGACY_FOLDERS.items():
        if not any(r['folder'] == current for r in rows):
            continue
        destination = BASE + current + '/'
        alias = out / BASE.strip('/') / legacy / 'index.html'
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8">'
                         '<meta name="viewport" content="width=device-width, initial-scale=1">'
                         '<meta http-equiv="refresh" content="0;url='+destination+'">'
                         '<link rel="canonical" href="https://bobmythos.fr'+destination+'">'
                         '<title>Dossier thématique — MYTHOS</title></head><body>'
                         '<p><a href="'+destination+'">'+escape(FOLDER_TITLES[current])+'</a></p>'
                         '</body></html>', encoding='utf-8')
    return rows


def verify(out, expected_urls):
    """Reject missing/duplicate assignments, broken anchors or orphan folders."""
    out = Path(out)
    root = out / BASE.strip('/')
    assignments, cache = Counter(), {}
    index = BeautifulSoup((root / 'index.html').read_text(encoding='utf-8'), 'html.parser')
    for page in root.glob('*/index.html'):
        if page.parent.name in LEGACY_FOLDERS:
            current = LEGACY_FOLDERS[page.parent.name]
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            assert doc.select_one('meta[http-equiv="refresh"]'), 'Alias historique non reconstruit'
            assert doc.find('a', href=BASE+current+'/'), 'Renvoi historique absent'
            assert (root/current/'index.html').is_file(), 'Cible historique absente'
            continue
        assert index.select_one('a[href="'+BASE+page.parent.name+'/"]'), 'Dossier orphelin : '+str(page)
        doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        for link in doc.select('a[data-greek-entry]'):
            url = link['href']
            assignments[url] += 1
            parsed = urlsplit(url)
            target = out / unquote(parsed.path).lstrip('/')
            if parsed.path.endswith('/'):
                target /= 'index.html'
            assert target.is_file(), 'Texte absent du dossier : '+url
            if parsed.fragment:
                if target not in cache:
                    cache[target] = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
                assert cache[target].find(id=unquote(parsed.fragment)), 'Section introuvable : '+url
    assert set(assignments) == set(expected_urls), 'Classement incomplet ou inattendu : '+str(set(assignments) ^ set(expected_urls))
    assert all(n == 1 for n in assignments.values()), 'Texte classé plusieurs fois dans les dossiers'
    print('Dossiers grecs vérifiés :', len(assignments), 'destinations uniques, tous les textes et toutes les sections accessibles')


CSS = '''
.greek-folder-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
.greek-folder-grid .portal-card strong{font:1.3rem/1.3 Georgia,serif;color:#efd7a6}
.greek-folder-grid .portal-card small{color:#c8b995;font:.78rem/1.5 system-ui}
.greek-folder-toc ul{display:flex;flex-wrap:wrap;justify-content:center;gap:.7rem;list-style:none;padding:0}
.greek-folder-toc a{display:block;padding:.7rem 1rem;border:1px solid #8b724d;border-radius:5px;color:#ead3a9;text-decoration:none}
.greek-folder-links{list-style:none;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem 1.6rem}
.greek-folder-links li{padding:.65rem 0;border-bottom:1px solid #57472f;min-width:0}
.greek-folder-links a{display:block;color:#f0dfc0;overflow-wrap:anywhere;line-height:1.5}
.greek-folder-links small{display:block;color:#bfb39a;font:.78rem/1.5 system-ui;margin-top:.3rem}
.greek-folder-breadcrumb{margin:0 0 1.4rem;padding:.8rem 0;color:#dec18d;font-size:.9rem}
.greek-complete-catalogue{margin:2.5rem 0;border-top:1px solid #8b724d;padding-top:1.2rem}
.greek-complete-catalogue>summary{font:1.35rem Georgia,serif;color:#e9cd9a;cursor:pointer;padding:.8rem}
.greek-folder-toc a:focus-visible,.greek-folder-links a:focus-visible,.greek-complete-catalogue>summary:focus-visible{outline:3px solid #f8dc9c;outline-offset:4px}
@media(max-width:1050px){.greek-folder-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.greek-folder-grid,.greek-folder-links{grid-template-columns:1fr}.greek-folder-toc ul{display:block}.greek-folder-toc li{margin-bottom:.5rem}}
'''
