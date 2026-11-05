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
import json
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
    # Études intégrales déjà déposées dans editorial/inbox : aucun numéro
    # anticipé. Dès l’attribution par Actions, rattacher les pages au
    # sanctuaire local correspondant, sans déplacer leur manuscrit.
    (r'^apollon ptoios\\b', 'sanctuaires',
     'Béotie — Apollon Ptoios, oracle, kouroi et héros Ptoios'),
    (r'^hera lakinia\\b', 'sanctuaires',
     'Grande-Grèce — Héra Lakinia, Crotone et Capo Colonna'),
    # 426 : le manuscrit intégral et son reçu sont déjà publiés. L'épiclèse
    # Amarysia renvoie au sanctuaire d'Amarynthos, pas à une déesse autonome.
    (r'^artemis amarysia\b', 'sanctuaires',
     'Amarynthos et Érétrie — Artémis Amarysia, fêtes et inscriptions'),
    # Étude intégrale 425 (Pausanias I, 15, 3 et I, 32, 5) : héros
    # attique de Marathon, non divinité et non source antique autonome.
    (r'^echetlos\b', 'heros', 'Marathon — Échétlos, araire et mémoire civique'),
    # Étude intégrale antérieure 326 : Hécalé accueille Thésée à Marathon.
    # Conservation de sa cote historique et de ses références à Callimaque.
    (r'^hecale\b', 'heros', 'Hécalé — Thésée, hospitalité et mémoire attique'),
    # Études déjà publiées 398 et 424 : le sujet est le sanctuaire local,
    # non l'appartenance générale d'Artémis/Dionysos au panthéon olympien.
    # Liens de retour et sommaires régénérés sans réécrire les manuscrits.
    (r'^artemis soteira\b', 'sanctuaires', 'Mégare, Trézène et Pellène — Artémis Sôteira et salut civique'),
    (r'^dionysos aisymnetes\b', 'sanctuaires', 'Patras — Dionysos Aisymnètès, Artémis Triklaria et Eurypyle'),
    # Réconciliation de 10 études intégrales déjà publiées (391–400, 423).
    # Affectation par le sujet effectif et les témoignages primaires contrôlés :
    # seules les rubriques/sous-dossiers sont générés ; ni cote ni texte modifiés.
    (r'^aristee\b', 'sanctuaires', 'Aristée — apiculture, techniques agraires et cultes'),
    (r'^horme\b', 'dieux', 'Hormè — impulsion et personnifications de l’action'),
    (r'^eukleia\b', 'sanctuaires', 'Eukleia — renommée civique et sanctuaires'),
    (r'^despoina\b', 'sanctuaires', 'Lykosoura — Déméter, Despoina et mystères arcadiens'),
    (r'^britomartis\b', 'sanctuaires', 'Crète — Britomartis, Dictynna et sanctuaires'),
    (r'^palaimon\b', 'sanctuaires', 'Isthmia — Palémon, Mélicerte et jeux funéraires'),
    (r'^melinoe\b', 'dieux', 'Mélinoé — hymnes orphiques et puissances nocturnes'),
    (r'^iynx\b', 'sources', 'Pindare et Théocrite — persuasion et magie amoureuse'),
    (r'^enyo\b', 'dieux', 'Ényô — puissances guerrières et violence destructrice'),
    (r'^apollon agyieus\b', 'sanctuaires', 'Apollon Agyieus — voies, piliers et seuils sacrés'),
    # Études 401–403, 405–406, 412 et 421–422 : ces manuscrits intégraux
    # étaient accessibles, mais plusieurs étaient relégués dans la file
    # « Nouvelles études à classer ». Rattachement par sujet épigraphique
    # ou cultuel attesté, et non par des noms mentionnés au passage.
    (r'^tritopatores\b', 'sanctuaires', 'Ancêtres, naissance et rites de purification'),
    (r'^sosipolis\b', 'sanctuaires', 'Olympie, Élide et dieux protecteurs des cités'),
    (r'^ennodia\b', 'sanctuaires', 'Thessalie — déesses des routes et des seuils'),
    (r'^acheloos\b', 'dieux', 'Dieux-fleuves, paysages et eaux divinisées'),
    (r'^poseidon hippocampes\b', 'dieux', 'Poséidon et le cortège marin'),
    (r'^aristeas\b', 'sources', 'Poètes, voyages et traditions fragmentaires'),
    (r'^praxidikai\b', 'sanctuaires', 'Haliarte — serments, justice et sanction sacrée'),
    (r'^salmakis\b', 'sanctuaires', 'Halicarnasse — fontaines, inscriptions et métamorphoses'),
    # Sujets vérifiés dans les chapitres 407 et 410–420 : éviter que les
    # études récentes, pourtant déjà publiées, restent dans le dossier
    # générique « Nouvelles études à classer ». Une seule famille primaire
    # est choisie par titre ; les renvois associés sont générés plus bas.
    (r'^makaria\b', 'familles', 'Héraclides — asile, sacrifice et cité'),
    (r'^alastor\b', 'familles', 'Atrides — vengeance, mémoire et souillure'),
    (r'^agdistis\b', 'dieux', 'Puissances phrygiennes et traditions anatoliennes'),
    (r'^pothos\b', 'dieux', 'Puissances du désir et personnifications'),
    (r'^asopos\b', 'dieux', 'Divinités fluviales et généalogies'),
    (r'^telesphoros\b', 'sanctuaires', 'Asclépios, santé et cultes de guérison'),
    (r'^agathos daimon\b', 'sanctuaires', 'Cultes domestiques et prospérité'),
    (r'^eunostos\b', 'sanctuaires', 'Héros locaux et interdits sacrés'),
    (r'^epimenide\b', 'sanctuaires', 'Purification des cités et médiation rituelle'),
    (r'^eiresione\b', 'sanctuaires', 'Apollon — processions et offrandes'),
    (r'^bendis\b', 'sanctuaires', 'Cultes thraces et célébrations en Attique'),
    (r'^(kouretes|couretes)\b', 'cosmogonies', 'Enfance de Zeus et traditions crétoises'),
    (r'^cnossos\b', 'sources', 'Archéologie égéenne : lieux et récits'),
    (r'^zeus meilichios\b', 'sanctuaires', 'Épithètes cultuelles et rites de purification'),
    (r'^(nyx|gaia|titanomachie|typhon|gigantomachie)\b', 'cosmogonies', 'Générations divines et conflits de souveraineté'),
    (r'^(promethee|hypnos)\b', 'cosmogonies', 'Condition humaine, mort et destin'),
    (r'^(helios|asteria|pan|satyres)\b', 'dieux', 'Puissances de la nature'),
    (r'^(tyche|hymenaios|ilithyie|aidos|eleos|pheme|hebe|kairos)\b', 'dieux', 'Puissances de la vie et de la cité'),
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
    # Mémoire de philosophie antique complet et déjà publié (PHY-SOC-2026-01).
    # Le mot « Delphes » ne doit pas le classer comme un compte rendu de culte.
    if slug == 'chapitres/philosophie/socrate-oracle-delphes-paradoxe-sagesse':
        return 'interpretations-philosophiques', 'Socrate — oracle, enquête et sagesse'
    # Étude complète déjà publique dans les civilisations : renvoi sans copie.
    if slug == 'bibliotheque-mythologies-du-monde/civilisations-chypre-paphos-aphrodite':
        return 'cultes-sanctuaires', 'Palaepaphos — Aphrodite et histoire du sanctuaire'
    # Publications intégrales de Civilisations : adresses et cotes conservées.
    history_homes = {
        'bibliotheque-mythologies-du-monde/civilisations-histoire-egee-bronze':
            ('sources-anciennes', 'Égée du Bronze — archéologie, linéaire A et B'),
        'bibliotheque-mythologies-du-monde/civilisations-histoire-grece-antique':
            ('sources-anciennes', 'Histoire des cités grecques — institutions et témoignages'),
        'bibliotheque-mythologies-du-monde/civilisations-pergame-attalides-autel-zeus':
            ('cultes-sanctuaires', 'Pergame — Grand Autel, Gigantomachie et royauté'),
        'bibliotheque-mythologies-du-monde/civilisations-lycie-xanthos-letoon':
            ('cultes-sanctuaires', 'Lycie — Létoon, Léto, Artémis et Apollon'),
        'bibliotheque-mythologies-du-monde/civilisations-commagene-antiochos-nemrut':
            ('cultes-sanctuaires', 'Commagène — Nemrut Dağ, dieux et souveraineté'),
        'bibliotheque-mythologies-du-monde/civilisations-royaumes-greco-bactriens-indo-grecs':
            ('sources-anciennes', 'Royaumes gréco-bactriens — inscriptions, monnaies et échanges'),
        'bibliotheque-mythologies-du-monde/civilisations-lydie-sardes-cresus':
            ('sources-anciennes', 'Lydie — Hérodote, Crésus et monnaies archaïques'),
        'bibliotheque-mythologies-du-monde/civilisations-phrygie-midas-gordion':
            ('cultes-sanctuaires', 'Phrygie — Gordion, Matar et traditions de Midas'),
        'bibliotheque-mythologies-du-monde/civilisations-thraces-odryses-kazanlak':
            ('cultes-sanctuaires', 'Thrace — Kazanlak, royaume odryse et rites funéraires'),
        'bibliotheque-mythologies-du-monde/civilisations-empire-seleucide-antiochos':
            ('sources-anciennes', 'Empire séleucide — cités, inscriptions et chroniques'),
        'bibliotheque-mythologies-du-monde/civilisations-egypte-ptolemaique-alexandrie':
            ('cultes-sanctuaires', 'Alexandrie — Sérapis, Isis et institutions lagides'),
        'bibliotheque-mythologies-du-monde/civilisations-histoire-etrusques':
            ('sources-anciennes', 'Étrurie — images grecques, divination et épigraphie'),
        'bibliotheque-mythologies-du-monde/civilisations-histoire-iran-perse':
            ('sources-anciennes', 'Iran achéménide — inscriptions royales et sources grecques'),
        'bibliotheque-mythologies-du-monde/civilisations-histoire-hittites-anatolie':
            ('sources-anciennes', 'Hattousa — archives, Kumarbi et traditions de succession'),
    }
    # Sources déjà publiées : seulement un rattachement thématique grec.
    history_homes.update({
        'bibliotheque-mythologies-du-monde/civilisations-hourrites-mittani-kumarbi':
            ('sources-anciennes', 'Hourrites — tablettes de Kumarbi et archives du Mittani'),
        'bibliotheque-mythologies-du-monde/mythos-comparatif-souverainete-cosmique-kumarbi-hesiode-pergame':
            ('interpretations-philosophiques', 'Kumarbi et Hésiode — souveraineté cosmique en comparaison'),
    })
    if slug in history_homes:
        return history_homes[slug]
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
    mapping = {'cosmogonies': 'cosmogonies', 'familles': 'familles', 'dieux': 'divinites',
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


# Lectures croisées entre quatre études intégrales, déjà attribuées dans
# le registre canonique. Elles restent dans leurs familles primaires ; ces
# liens sont des renvois complémentaires, jamais de nouvelles attributions.
# Ne pas y substituer des résumés ou modifier le contenu scientifique.
MARATHON_STUDIES = (
    ('/chapitres/encyclopedie/chapitre-425-echetlos-echetlaios-heros-araire-marathon-memoire-stoa-poikile/',
     'Chapitre 425 — Échétlos et Échétlaios',
     'Apparition héroïque, Stoa Poikilè et mémoire de la bataille.'),
    ('/chapitres/encyclopedie/chapitre-326-hecale-taureau-marathon/',
     'Chapitre 326 — Hécalé et le taureau de Marathon',
     'Thésée, hospitalité et mémoire cultuelle attique : autre tradition.'),
    ('/chapitres/encyclopedie/chapitre-371-pan-nouvelle-etude/',
     'Chapitre 371 — Pan',
     'Le dieu Pan et le coureur athénien : un témoignage distinct.'),
    ('/chapitres/encyclopedie/chapitre-393-eukleia-bonne-renommee-artemis-mariage-marathon-aigai-eurydice/',
     'Chapitre 393 — Eukleia',
     'Renommée publique et mémoire religieuse de Marathon.'),
)

# Parcours documentaire de quatre études intégrales déjà publiées. Les
# épiclèses d'Artémis et les pratiques rituelles sont LOCALES : ce parcours
# compare les témoignages sans prétendre à un rite panhellénique unique.
ARTEMIS_STUDIES = (
    ('/chapitres/encyclopedie/chapitre-426-artemis-amarysia-amarynthos-eretrie-sanctuaire-procession-epigraphie/',
     'Chapitre 426 — Artémis Amarysia',
     'Amarynthos et Érétrie : processions, droit civique, épigraphie.'),
    ('/chapitres/encyclopedie/chapitre-398-artemis-soteira-megare-trezene-pellene-salut-cites/',
     'Chapitre 398 — Artémis Sôteira',
     'Mégare, Trézène et Pellène : protection, serments et mémoires locales.'),
    ('/chapitres/encyclopedie/chapitre-395-britomartis-dictynna-crete-artemis-filets-minos/',
     'Chapitre 395 — Britomartis et Dictynna',
     'Crète : témoignages de Callimaque, Strabon et Pausanias.'),
    ('/chapitres/encyclopedie/chapitre-424-dionysos-aisymnetes-patras-eurypyle-triklaria-fete-rites/',
     'Chapitre 424 — Artémis Triklaria et Dionysos Aisymnètès',
     'Patras : récit rituel et transformations de la mémoire sacrificielle.'),
)

# Trois textes intégraux déjà publics. Distinguer l'institution de la Pythie,
# les maximes delphiques et l'usage philosophique du récit chez Platon.
# La cote PHY-SOC-2026-01 n'est pas un chapitre numéroté de l'encyclopédie.
DELPHES_STUDIES = (
    ('/chapitres/philosophie/socrate-oracle-delphes-paradoxe-sagesse/',
     'PHY-SOC-2026-01 — Socrate, l’oracle et la sagesse',
     'Mémoire de philosophie antique : Platon, Xénophon, examen de soi et annexes.'),
    ('/chapitres/encyclopedie/chapitre-348-pythie-delphes-parole-inspiree/',
     'Chapitre 348 — La Pythie de Delphes',
     'Consultation, rituels et autorité de la prêtresse : enquête historique.'),
    ('/chapitres/encyclopedie/chapitre-349-maximes-delphiques-connais-toi-toi-meme/',
     'Chapitre 349 — Les maximes delphiques',
     'Connais-toi toi-même : traditions textuelles et histoire des interprétations.'),
)


# Trois études intégrales déjà publiques, trois corpus documentaires distincts.
# La rubrique Civilisations et le texte original de Palaepaphos sont préservés.
APHRODITE_STUDIES = (
    ('/corpus/mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html',
     'MG · 02 — Aphrodite : monographie universitaire',
     'Généalogies, cultes, variantes et interprétations philosophiques.'),
    ('/sappho-aphrodite-poesie-lyrique-fragments-papyrus/',
     'Sappho — Aphrodite, fragments et papyrus',
     'Prière, poésie archaïque et transmission matérielle des textes.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-chypre-paphos-aphrodite/',
     'Chypre antique — Palaepaphos et Aphrodite',
     'Archéologie du sanctuaire, royautés chypriotes et traditions littéraires.'),
)

# Trois documents historiques intégralement publiés dans Civilisations.
# Bronze mycénien, Grèce des cités et Pergame sont des époques distinctes.
HISTORY_STUDIES = (
    ('/bibliotheque-mythologies-du-monde/civilisations-histoire-egee-bronze/',
     'Égée du Bronze — Minoens et Mycéniens',
     'Archives de Pylos, linéaires A et B, limites des parallèles homériques.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-histoire-grece-antique/',
     'Grèce antique — institutions, démocratie et tragédie',
     'Sources sur la cité, ses pratiques politiques et les festivals de théâtre.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-pergame-attalides-autel-zeus/',
     'Pergame — Attalides, Grand Autel et Gigantomachie',
     'Iconographie monumentale, légitimation dynastique et histoire des cultes.'),
)

# Études intégrales déjà publiques dans Civilisations, reliées sans copie.
# Les cultes lyciens, la royauté de Commagène, l'iconographie attalide et
# les monnaies de Bactriane ne sont pas assimilés à une tradition uniforme.
HELLENISTIC_CONTACT_STUDIES = (
    ('/bibliotheque-mythologies-du-monde/civilisations-lycie-xanthos-letoon/',
     'Lycie — Létoon, Léto, Artémis et Apollon',
     'Sanctuaire, inscriptions trilingues et institutions locales lyciennes.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-commagene-antiochos-nemrut/',
     'Commagène — Antiochos Ier et Nemrut Dağ',
     'Royauté gréco-perse, statues et théonymes composés.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-pergame-attalides-autel-zeus/',
     'Pergame — Autel des Attalides et Gigantomachie',
     'Monument hellénistique, image du pouvoir et interprétation cultuelle.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-royaumes-greco-bactriens-indo-grecs/',
     'Bactriane et royaumes indo-grecs',
     'Numismatique, échanges, ruptures et pluralité de traditions religieuses.'),
)


# Quatre études civiles intégrales déjà publiées et vérifiées : accès croisé
# aux contacts culturels sans les assimiler à une religion « grecque » unique.
# Leurs URL et leurs textes restent dans la rubrique Civilisations.
ANATOLIA_THRACE_STUDIES = (
    ('/bibliotheque-mythologies-du-monde/civilisations-lydie-sardes-cresus/',
     'Lydie — Sardes et Crésus',
     'Hérodote, monnaies et représentations grecques du pouvoir lydien.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-phrygie-midas-gordion/',
     'Phrygie — Midas et Gordion',
     'Matar-Cybèle, archéologie du tumulus MM et récits tardifs.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-thraces-odryses-kazanlak/',
     'Thraces — Odryses et Kazanlak',
     'Sépultures, banquet funéraire et témoignages grecs sur les cultes.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-empire-seleucide-antiochos/',
     'Empire séleucide — de Séleucos aux Antiochos',
     'Cités hellénistiques, traditions mésopotamiennes et rois grecs.'),
)


# Quatre études publiques intégrales, chacune à son adresse patrimoniale.
# La comparaison porte sur la réception et les sources, et n'affirme
# ni filiation religieuse automatique ni équivalence des panthéons.
TRANSMISSION_STUDIES = (
    ('/bibliotheque-mythologies-du-monde/civilisations-egypte-ptolemaique-alexandrie/',
     'Égypte ptolémaïque — Alexandrie et Sérapis',
     'Dynastie lagide, pratiques religieuses égyptiennes et royauté hellénistique.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-histoire-etrusques/',
     'Étrusques — cités, iconographie et divination',
     'Écriture, représentations de mythes grecs et traditions rituelles locales.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-histoire-iran-perse/',
     'Iran ancien — Achéménides et sources grecques',
     'Archives impériales, Persépolis et regards d’Hérodote sur l’empire perse.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-histoire-hittites-anatolie/',
     'Hittites — Hattousa, Kumarbi et traditions anatoliennes',
     'Textes de succession divine, archives hittites et comparaison avec Hésiode.'),
)


# Les textes restent aux URL d'origine : une source grecque, deux études
# comparatives déjà publiées. Les liens réciproques ne sont pas des doublons.
COSMIC_STUDIES = (
    ('/livre-hesiode/',
     'Hésiode — Théogonie et condition humaine',
     'Le récit grec de succession d’Ouranos, Cronos et Zeus.'),
    ('/bibliotheque-mythologies-du-monde/civilisations-hourrites-mittani-kumarbi/',
     'Hourrites et Mittani — le cycle de Kumarbi',
     'Archives de Syrie et d’Anatolie et sources de l’âge du Bronze.'),
    ('/bibliotheque-mythologies-du-monde/mythos-comparatif-souverainete-cosmique-kumarbi-hesiode-pergame/',
     'Kumarbi, Hésiode et Pergame — lecture comparée',
     'Comparaison des récits, des images et des lectures philosophiques.'),
)


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

# One archival object per editorial theme, deliberately curated (not a
# civilization-wide image fallback). Objects and captions are read at build time
# from the provenance register; no historical image or text is rewritten.
# Derveni transmits an ancient commentary on an Orphic theogony, relevant to
# cosmogonies as a textual witness (NOT an illustration of creation scenes).
# P.Oxy. 20 illustrates manuscript transmission for the sources family.
FOLDER_ARTWORK = {
    "cosmogonies": ("mythos-derveni-papyrus-fragments-thessalonique-gts-tg", "Derveni"),
    "divinites": ("mythos-bronze-artemision-zeus-ou-poseidon", "Zeus"),
    "heros": ("mythos-thesee-minotaure-amphore-taleides-met-47-11-5", "Thésée"),
    "familles": ("mythos-mycene-porte-lionnes-zde-2020", "Mycènes"),
    "cycles-epiques": ("mythos-hector-priam-rancon-briseis-peintre-british-museum-e75", "Iliade"),
    "cultes-sanctuaires": ("delphes-temple-apollon-bernard-gagnon", "Delphes"),
    "sources-anciennes": ("mythos-papyrus-oxyrhynchus-20-iliade-ii", "Iliade"),
    "interpretations-philosophiques": ("jacques-louis-david-mort-de-socrate-1787", "Socrate"),
}


def folder_artworks(root, out, families):
    """Return only verified, on-disk photographs with documented attribution.

    A missing artwork raises before deployment; editorial absence is preferable
    to substituting an unrelated photograph or an old 2.5D reconstruction.
    """
    if root is None:
        return {}
    root, out = Path(root), Path(out)
    manifest = root / "scripts/editorial_media.json"
    if not manifest.is_file():
        raise RuntimeError("MYTHOS : registre de provenance iconographique absent")
    records = json.loads(manifest.read_text(encoding="utf-8"))["media"]
    by_id = {item["id"]: item for item in records}
    if len(by_id) != len(records):
        raise RuntimeError("MYTHOS : identifiants d'illustrations dupliqués")
    images = {}
    for slug, (art_id, subject) in FOLDER_ARTWORK.items():
        if slug not in families:
            continue
        item = by_id.get(art_id)
        if not item or subject not in item.get("subjects", []):
            raise RuntimeError("Dossier grec : provenance non vérifiée : " + slug)
        path = item.get("path", "")
        caption = item.get("caption_html", "")
        if (not path.startswith("media/2026/10/")
                or ".." in Path(path).parts
                or not path.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
                or not item.get("alt") or not caption or "href=" not in caption
                or not (out / path).is_file()):
            raise RuntimeError("Dossier grec : image/source absente : " + slug)
        images[slug] = item
    return images


def cards_html(rows, artworks=None):
    artwork = artworks or {}
    cards = []
    for slug, title, description in FOLDERS:
        members = [r for r in rows if r['folder'] == slug]
        if not members:
            continue
        record = artwork.get(slug)
        image = ('<img class="greek-folder-illustration" src="/' +
                 escape(record["path"], quote=True) + '" alt="' +
                 escape(record["alt"], quote=True) +
                 '" loading="lazy" decoding="async">' if record else '')
        credit = ('<details class="greek-folder-credit"><summary>'
                  'Document représentatif : source et licence</summary>'
                  '<p>Repère iconographique de ce thème, et non preuve '
                  'historique de tous ses récits.</p><div>' +
                  record["caption_html"] + '</div></details>' if record else '')
        cards.append(
            '<div class="greek-folder-entry"><a class="greek-folder-link" href="' +
            BASE + slug + '/">' + image +
            '<span class="greek-folder-kicker">DOSSIER THÉMATIQUE</span>' +
            '<strong>' + escape(title) + '</strong><span class="greek-folder-description">' +
            escape(description) + '</span><small>' +
            escape(counts(members, compact=True)) +
            '</small><span class="greek-folder-arrow" aria-hidden="true">→</span></a>' +
            credit + '</div>')
    return '<div class="portal-grid greek-folder-grid">' + ''.join(cards) + '</div>'


def overview(rows, artworks=None):
    return ('<section id="dossiers-thematiques" class="portal-section"><h2>Choisir un dossier thématique</h2>'
            '<p class="portal-lead">Entrez par un personnage, un cycle ou un thème, puis ouvrez les chapitres qui s’y rapportent.</p>'
            '<p>' + escape(counts(rows)) + '. Les sections sont des passages des livres, accessibles directement à leur titre.</p>'
            + cards_html(rows, artworks) + '</section>')


def build(out, groups, sections, books, root=None):
    from build_navigation import shell
    out = Path(out)
    rows = inventory(groups, sections, books)
    artworks = folder_artworks(root, out, {r["folder"] for r in rows})
    # A single ordered source of truth for the headings, jump anchors and
    # reciprocal links: a reader returns to its exact thematic subsection,
    # not just to the top of a potentially very long family catalogue.
    subsets_by_folder = {slug: defaultdict(list) for slug, _, _ in FOLDERS}
    for row in rows:
        subsets_by_folder[row['folder']][row['section']].append(row)
    subsection_urls = {
        (folder, section): BASE + folder + '/#theme-' + str(index)
        for folder, subsets in subsets_by_folder.items()
        for index, section in enumerate(subsets, 1)
    }
    def render(title, body, description=''):
        return shell(title, body, description).replace('</head>', '<style id="greek-folder-style">'+CSS+'</style></head>')
    (out / BASE.strip('/')).mkdir(parents=True, exist_ok=True)
    index = '<h1>Les dossiers de l’encyclopédie grecque</h1><p><a href="/mythologie-grecque/">Encyclopédie grecque</a></p>' + overview(rows, artworks)
    (out / BASE.strip('/') / 'index.html').write_text(render('Dossiers thématiques de l’encyclopédie grecque', index), encoding='utf-8')
    # Le circuit Marathon est ajouté autour des études *existantes*.
    # La présence dans l'inventaire, et non une hypothèse tirée du slug,
    # détermine si un lien réciproque peut être affiché.
    marathon_urls = {url for url, _, _ in MARATHON_STUDIES
                     if any(row['url'] == url for row in rows)}
    artemis_urls = {url for url, _, _ in ARTEMIS_STUDIES
                    if any(row['url'] == url for row in rows)}
    delphes_urls = {url for url, _, _ in DELPHES_STUDIES
                    if any(row['url'] == url for row in rows)}
    aphrodite_urls = {url for url, _, _ in APHRODITE_STUDIES
                      if any(row['url'] == url for row in rows)}
    history_urls = {url for url, _, _ in HISTORY_STUDIES
                    if any(row['url'] == url for row in rows)}
    contact_urls = {url for url, _, _ in HELLENISTIC_CONTACT_STUDIES
                    if any(row['url'] == url for row in rows)}
    border_urls = {url for url, _, _ in ANATOLIA_THRACE_STUDIES
                   if any(row['url'] == url for row in rows)}
    transmission_urls = {url for url, _, _ in TRANSMISSION_STUDIES
                         if any(row['url'] == url for row in rows)}
    cosmic_urls = {url for url, _, _ in COSMIC_STUDIES
                   if any(row['url'] == url for row in rows)}
    # Return links stay outside the article, leaving its scholarly text untouched.
    for row in rows:
        if (row['kind'] not in ('Chapitre universitaire', 'Livre', 'Notice', 'Étude')
                and row['url'] not in ({DELPHES_STUDIES[0][0],
                                       APHRODITE_STUDIES[1][0],
                                       APHRODITE_STUDIES[2][0]} | history_urls | contact_urls | border_urls | transmission_urls | cosmic_urls)):
            continue
        page = out / row['url'].lstrip('/')
        if row['url'].endswith('/'):
            page /= 'index.html'
        doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        main = doc.main
        if main is None:
            continue  # Minimal test fixtures may only contain a heading.
        for old in doc.select('[data-greek-folder-nav], [data-greek-cross-readings]'):
            old.decompose()
        folder = row['folder']
        subsection_url = subsection_urls[(folder, row['section'])]
        nav = BeautifulSoup('<nav class="greek-folder-breadcrumb" data-greek-folder-nav="true" aria-label="Dossier de cette étude">'
                            '<a href="/mythologie-grecque/">Encyclopédie grecque</a> · <a href="'+BASE+folder+'/">'
                            +escape(FOLDER_TITLES[folder])+'</a> · <a class="greek-folder-return-topic" href="'
                            +escape(subsection_url, quote=True)+'">Sous-dossier : '
                            +escape(row['section'])+'</a></nav>', 'html.parser').nav
        main.insert(0, nav)
        if row['url'] in marathon_urls:
            companions = [(url, title, context)
                          for url, title, context in MARATHON_STUDIES
                          if url in marathon_urls and url != row['url']]
            if companions:
                # Hors de l'article : le manuscrit, ses citations et ses
                # bibliographies demeurent strictement intacts.
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="marathon" '
                    'aria-label="Études croisées sur Marathon">'
                    '<h2>Marathon : lectures croisées</h2>'
                    '<p>Quatre enquêtes distinctes : apparition héroïque, '
                    'récit de Thésée, intervention de Pan et mémoire civique. '
                    'Chaque lien donne accès à une étude complète avec ses '
                    'sources, et non à un résumé de remplacement.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in artemis_urls:
            companions = [(url, title, context)
                          for url, title, context in ARTEMIS_STUDIES
                          if url in artemis_urls and url != row['url']]
            if companions:
                # Ces lectures sont accolées à la page, hors du manuscrit.
                # Les sources, la bibliographie et la cote ne changent pas.
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="artemis" '
                    'aria-label="Cultes locaux d’Artémis : lectures croisées">'
                    '<h2>Artémis et les cultes locaux : lectures croisées</h2>'
                    '<p>Ces quatre études intégrales distinguent les lieux, '
                    'les épiclèses et les sources antiques. Elles ne supposent '
                    'ni rites identiques ni continuité historique universelle.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in delphes_urls:
            companions = [(url, title, context)
                          for url, title, context in DELPHES_STUDIES
                          if url in delphes_urls and url != row['url']]
            if companions:
                # En dehors de l'article, sans toucher aux sources ni annexes.
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="delphes" '
                    'aria-label="Delphes : textes et interprétations">'
                    '<h2>Delphes : textes, oracle et connaissance de soi</h2>'
                    '<p>Trois lectures intégrales complémentaires. '
                    'La pratique religieuse delphique et la réélaboration '
                    'philosophique de Socrate ne se confondent pas.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in aphrodite_urls:
            companions = [(url, title, context)
                          for url, title, context in APHRODITE_STUDIES
                          if url in aphrodite_urls and url != row['url']]
            if companions:
                # Panneau hors de l'article, sans changer les bibliographies,
                # cotes historiques ou textes des trois lectures.
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="aphrodite" '
                    'aria-label="Aphrodite : mythe, poésie et sanctuaire">'
                    '<h2>Aphrodite : du poème au sanctuaire</h2>'
                    '<p>Trois enquêtes intégrales : traditions divines, fragments '
                    'de Sappho et histoire de Palaepaphos. Le témoignage '
                    'littéraire n’établit pas à lui seul les pratiques '
                    'archéologiques du sanctuaire chypriote.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in history_urls:
            companions = [(url, title, context)
                          for url, title, context in HISTORY_STUDIES
                          if url in history_urls and url != row['url']]
            if companions:
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="chronologie" '
                    'aria-label="Égée et Grèce : histoire et sources">'
                    '<h2>Égée et Grèce : trois dossiers historiques</h2>'
                    '<p>Les archives mycéniennes, les institutions des cités et '
                    'le programme monumental des Attalides relèvent de sources '
                    'et d’époques distinctes. La transmission des récits '
                    'ne démontre pas une continuité politique ou cultuelle.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in contact_urls:
            companions = [(url, title, context)
                          for url, title, context in HELLENISTIC_CONTACT_STUDIES
                          if url in contact_urls and url != row['url']]
            if companions:
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="contacts" '
                    'aria-label="Mondes grecs et traditions locales">'
                    '<h2>Sanctuaires et royautés : contacts culturels</h2>'
                    '<p>Quatre monographies intégrales, des cités de Lycie aux '
                    'royaumes de Bactriane. Les sources, époques et pratiques '
                    'diffèrent : une analogie iconographique ou linguistique '
                    'n’est pas la preuve d’un culte identique.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in border_urls:
            companions = [(url, title, context)
                          for url, title, context in ANATOLIA_THRACE_STUDIES
                          if url in border_urls and url != row['url']]
            if companions:
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="frontieres" '
                    'aria-label="Anatolie et Thrace : sources et contacts grecs">'
                    '<h2>Aux frontières des mondes grecs : lectures croisées</h2>'
                    '<p>Quatre études intégrales de périodes distinctes. Les '
                    'témoignages grecs sur les Lydiens, Phrygiens et Thraces '
                    'ne se confondent pas avec leurs propres pratiques ; '
                    'les Séleucides appartiennent à une époque plus tardive. '
                    'Aucune continuité cultuelle n’est présumée.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in transmission_urls:
            companions = [(url, title, context) for url, title, context
                          in TRANSMISSION_STUDIES
                          if url in transmission_urls and url != row['url']]
            if companions:
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="transmissions" '
                    'aria-label="Transmissions et regards entre cultures antiques">'
                    '<h2>Mondes grecs : transferts, lectures et sources</h2>'
                    '<p>Quatre études universitaires intégrales : les Lagides '
                    'd’Égypte, les Étrusques, l’empire perse et l’Anatolie '
                    'hittite. Les rapprochements sont documentaires ; ils '
                    'n’impliquent ni identité des cultes ni transmission '
                    'directe de chaque récit.</p><ul>' + links +
                    '</ul></aside>', 'html.parser').aside
                main.append(box)
        if row['url'] in cosmic_urls:
            companions = [(url, title, context) for url, title, context
                          in COSMIC_STUDIES if url in cosmic_urls and url != row['url']]
            if companions:
                links = ''.join(
                    '<li><a href="' + escape(url, quote=True) + '">' +
                    escape(title) + '</a><small>' + escape(context) +
                    '</small></li>' for url, title, context in companions)
                box = BeautifulSoup(
                    '<aside class="greek-cross-readings" '
                    'data-greek-cross-readings="souverainete-cosmique" '
                    'aria-label="Hésiode et Kumarbi : sources et lectures comparées">'
                    '<h2>Généalogies divines : Hésiode et Kumarbi</h2>'
                    '<p>Trois lectures complètes : poème grec, archives '
                    'hourrites et étude comparée. Une ressemblance ne prouve '
                    'pas à elle seule une transmission directe ; sources et '
                    'chronologies doivent être distinguées.</p>'
                    '<ul>' + links + '</ul></aside>', 'html.parser').aside
                main.append(box)
        page.write_text(str(doc), encoding='utf-8')
    for slug, title, description in FOLDERS:
        members = [r for r in rows if r['folder'] == slug]
        if not members:
            continue
        subsets = subsets_by_folder[slug]
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
    # Les liens transversaux sont contrôlés séparément : ils ne comptent
    # jamais comme de secondes affectations éditoriales.
    marathon_urls = {url for url, _, _ in MARATHON_STUDIES if url in expected_urls}
    if len(marathon_urls) > 1:
        for url in marathon_urls:
            path = out / url.lstrip('/') / 'index.html'
            doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="marathon"]')
            assert len(panels) == 1, 'Parcours Marathon manquant ou dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == marathon_urls - {url}, 'Lectures croisées incomplètes : ' + url
            assert len(actual) == len(set(actual)), 'Lien Marathon répété : ' + url
    artemis_urls = {url for url, _, _ in ARTEMIS_STUDIES if url in expected_urls}
    if len(artemis_urls) > 1:
        for url in artemis_urls:
            path = out / url.lstrip('/') / 'index.html'
            doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="artemis"]')
            assert len(panels) == 1, 'Parcours Artémis manquant ou dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == artemis_urls - {url}, 'Lectures Artémis incomplètes : ' + url
            assert len(actual) == len(set(actual)), 'Lien Artémis répété : ' + url
    delphes_urls = {url for url, _, _ in DELPHES_STUDIES if url in expected_urls}
    if len(delphes_urls) > 1:
        for url in delphes_urls:
            path = out / url.lstrip('/') / 'index.html'
            doc = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="delphes"]')
            assert len(panels) == 1, 'Parcours Delphes manquant ou dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == delphes_urls - {url}, 'Lectures Delphes incomplètes : ' + url
            assert len(actual) == len(set(actual)), 'Lien Delphes répété : ' + url
    aphrodite_urls = {url for url, _, _ in APHRODITE_STUDIES
                      if url in expected_urls}
    if len(aphrodite_urls) > 1:
        for url in aphrodite_urls:
            page = out / url.lstrip('/')
            if url.endswith('/'):
                page /= 'index.html'
            assert page.is_file(), 'Étude Aphrodite introuvable : ' + url
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="aphrodite"]')
            assert len(panels) == 1, 'Parcours Aphrodite manquant ou dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == aphrodite_urls - {url}, 'Lectures Aphrodite incomplètes : ' + url
            assert len(actual) == len(set(actual)), 'Lien Aphrodite répété : ' + url
    history_urls = {url for url, _, _ in HISTORY_STUDIES if url in expected_urls}
    if len(history_urls) > 1:
        for url in history_urls:
            page = out / url.lstrip('/') / 'index.html'
            assert page.is_file(), 'Étude historique introuvable : ' + url
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="chronologie"]')
            assert len(panels) == 1, 'Parcours historique absent ou dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == history_urls - {url}, 'Parcours historique incomplet : ' + url
            assert len(actual) == len(set(actual)), 'Lien historique répété : ' + url
    contact_urls = {url for url, _, _ in HELLENISTIC_CONTACT_STUDIES
                    if url in expected_urls}
    if len(contact_urls) > 1:
        for url in contact_urls:
            page = out / url.lstrip('/') / 'index.html'
            assert page.is_file(), 'Étude des contacts grecs introuvable : ' + url
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="contacts"]')
            assert len(panels) == 1, 'Parcours des contacts manquant ou dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == contact_urls - {url}, 'Lectures croisées incomplètes : ' + url
            assert len(actual) == len(set(actual)), 'Lien vers les contacts répété : ' + url
    border_urls = {url for url, _, _ in ANATOLIA_THRACE_STUDIES
                   if url in expected_urls}
    if len(border_urls) > 1:
        for url in border_urls:
            page = out / url.lstrip('/') / 'index.html'
            assert page.is_file(), 'Étude Anatolie/Thrace introuvable : ' + url
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="frontieres"]')
            assert len(panels) == 1, 'Parcours frontières manquant ou dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == border_urls - {url}, 'Lectures frontières incomplètes : ' + url
            assert len(actual) == len(set(actual)), 'Lien frontières répété : ' + url
    transmission_urls = {url for url, _, _ in TRANSMISSION_STUDIES
                         if url in expected_urls}
    if len(transmission_urls) > 1:
        for url in transmission_urls:
            page = out / url.lstrip('/') / 'index.html'
            assert page.is_file(), 'Étude de transmission introuvable : ' + url
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="transmissions"]')
            assert len(panels) == 1, 'Parcours de transmission manquant/dupliqué : ' + url
            actual = [a['href'] for a in panels[0].select('a[href]')]
            assert set(actual) == transmission_urls - {url}, 'Parcours de transmission incomplet : ' + url
            assert len(actual) == len(set(actual)), 'Lien de transmission répété : ' + url
    cosmic_urls = {url for url, _, _ in COSMIC_STUDIES if url in expected_urls}
    if len(cosmic_urls) > 1:
        for url in cosmic_urls:
            page = out / url.lstrip('/') / 'index.html'
            assert page.is_file(), 'Étude Hésiode/Kumarbi absente : ' + url
            doc = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
            panels = doc.select('aside[data-greek-cross-readings="souverainete-cosmique"]')
            assert len(panels) == 1, 'Parcours Hésiode/Kumarbi manquant ou dupliqué : ' + url
            links = [a['href'] for a in panels[0].select('a[href]')]
            assert set(links) == cosmic_urls - {url}, 'Renvois Hésiode/Kumarbi incomplets : ' + url
            assert len(links) == len(set(links)), 'Renvoi Hésiode/Kumarbi dupliqué : ' + url
    assert set(assignments) == set(expected_urls), 'Classement incomplet ou inattendu : '+str(set(assignments) ^ set(expected_urls))
    assert all(n == 1 for n in assignments.values()), 'Texte classé plusieurs fois dans les dossiers'
    print('Dossiers grecs vérifiés :', len(assignments), 'destinations uniques, tous les textes et toutes les sections accessibles')


CSS = '''
.greek-folder-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}
.greek-folder-entry{min-width:0;display:flex;flex-direction:column;border:1px solid #785f3f;border-radius:5px;overflow:hidden;background:#101718}
.greek-folder-link{min-width:0;display:flex;flex:1;flex-direction:column;padding:0 1.1rem 1rem;color:#f0e5d2!important;text-decoration:none}
.mythos-design .greek-folder-link>.greek-folder-illustration{width:calc(100% + 2.2rem)!important;max-width:none!important;height:160px!important;object-fit:cover;display:block;margin:0 -1.1rem .8rem!important;border-bottom:1px solid #785f3f}
.greek-folder-kicker{color:#d8bd89;font:600 .68rem/1.6 system-ui;letter-spacing:.11em;margin-top:.85rem}
.greek-folder-link strong{font:1.3rem/1.3 Georgia,serif;color:#efd7a6;margin:.45rem 0 .6rem}
.greek-folder-description{color:#e2d5bc;font:1rem/1.6 Georgia,serif}
.greek-folder-link small{color:#c8b995;font:.78rem/1.5 system-ui;margin-top:.65rem}
.greek-folder-arrow{color:#e3be7d;margin-top:.4rem;align-self:flex-end}
.greek-folder-link:hover,.greek-folder-link:focus-visible{background:#182125;outline:2px solid #e5c38d;outline-offset:-2px}
.greek-folder-credit{border-top:1px solid #5d4e3a;padding:.45rem 1rem .75rem;color:#d7cab2;font:13px/1.5 Georgia,serif;overflow-wrap:anywhere}
.greek-folder-credit summary{display:list-item;min-height:44px;box-sizing:border-box;padding:.65rem .2rem;color:#ead0a4;cursor:pointer;overflow-wrap:anywhere}
.greek-folder-credit p{font-size:.8rem;margin:.55rem 0}
.greek-folder-credit a{color:#f7dda7;text-decoration:underline}
@media(max-width:700px){.mythos-design .greek-folder-link>.greek-folder-illustration{height:125px!important}}
.greek-folder-toc ul{display:flex;flex-wrap:wrap;justify-content:center;gap:.7rem;list-style:none;padding:0}
.greek-folder-toc a{display:flex;align-items:center;min-height:44px;box-sizing:border-box;padding:.7rem 1rem;border:1px solid #8b724d;border-radius:5px;color:#ead3a9;text-decoration:none;line-height:1.45;overflow-wrap:anywhere}
.greek-folder-links{list-style:none;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem 1.6rem}
.greek-folder-links li{padding:.65rem 0;border-bottom:1px solid #57472f;min-width:0}
.greek-folder-links a{display:flex;align-items:center;min-height:44px;padding:.35rem 0;color:#f0dfc0;overflow-wrap:anywhere;line-height:1.5;text-underline-offset:.2em}
.greek-folder-links a:hover{color:#ffe4b1;text-decoration-thickness:2px}
.greek-folder-links small{display:block;color:#bfb39a;font:.78rem/1.5 system-ui;margin-top:.3rem}
.greek-folder-breadcrumb{margin:0 0 1.4rem;padding:.8rem 0;color:#dec18d;font-size:.9rem;line-height:1.7;overflow-wrap:anywhere}
.greek-folder-breadcrumb .greek-folder-return-topic{color:#f0d29a;text-decoration:underline;text-underline-offset:3px}
.greek-folder-breadcrumb a:focus-visible{outline:3px solid #f8dc9c;outline-offset:3px}
.greek-folder-toc~.portal-section[id^="theme-"]{scroll-margin-top:115px}
.greek-folder-toc~.portal-section[id^="theme-"]:target{outline:2px solid #dab981;outline-offset:4px}
.greek-complete-catalogue{margin:2.5rem 0;border-top:1px solid #8b724d;padding-top:1.2rem}
.greek-complete-catalogue>summary{display:list-item;min-height:44px;box-sizing:border-box;font:1.35rem Georgia,serif;color:#e9cd9a;cursor:pointer;padding:.8rem}
.greek-folder-toc a:focus-visible,.greek-folder-links a:focus-visible,.greek-complete-catalogue>summary:focus-visible{outline:3px solid #f8dc9c;outline-offset:4px}
@media(max-width:1050px){.greek-folder-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:700px){.greek-folder-grid,.greek-folder-links{grid-template-columns:1fr}.greek-folder-toc ul{display:block}.greek-folder-toc li{margin-bottom:.5rem}.greek-folder-toc a{width:100%}}
@media(max-width:400px){.greek-folder-link{padding:0 .85rem .9rem}.mythos-design .greek-folder-link>.greek-folder-illustration{width:calc(100% + 1.7rem)!important;margin:0 -.85rem .75rem!important;height:110px!important}.greek-folder-link strong{font-size:1.16rem}.greek-folder-credit{padding:.6rem .85rem}}
/* Mobile : titres de sous-dossiers longs, dont les épiclèses cultuelles. */
@media(max-width:480px){
  .greek-folder-toc a,.greek-folder-links a{
    font-size:clamp(.94rem,3.6vw,1.03rem);
    line-height:1.6;
    overflow-wrap:anywhere;
    hyphens:auto;
  }
}

'''
