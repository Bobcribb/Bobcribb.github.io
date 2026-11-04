"""Rattachement documentaire des dix monographies grecques déjà publiées.

Aucune étude n'est créée ni renumérotée : vérifier les sources intégrales,
leur bibliographie et le classement automatique des lecteurs existants.
"""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_greek_folders import CSS, classify

# (numéro attribué, sujet immuable, famille, sous-dossier documentaire)
CASES = (
    (391, 'aristee-abeilles-oliviers-ceos-olbia-giens-orphee-eurydice',
     'cultes-sanctuaires', 'Aristée — apiculture, techniques agraires et cultes'),
    (392, 'horme-elan-impulsion-action-agora-stoiciens',
     'divinites', 'Hormè — impulsion et personnifications de l’action'),
    (393, 'eukleia-bonne-renommee-artemis-mariage-marathon-aigai-eurydice',
     'cultes-sanctuaires', 'Eukleia — renommée civique et sanctuaires'),
    (394, 'despoina-lykosoura-demeter-poseidon-mysteres-damophon',
     'cultes-sanctuaires', 'Lykosoura — Déméter, Despoina et mystères arcadiens'),
    (395, 'britomartis-dictynna-crete-artemis-filets-minos',
     'cultes-sanctuaires', 'Crète — Britomartis, Dictynna et sanctuaires'),
    (396, 'palaimon-melicertes-ino-leucothea-isthmia-jeux',
     'cultes-sanctuaires', 'Isthmia — Palémon, Mélicerte et jeux funéraires'),
    (397, 'melinoe-hymne-orphique-persephone-apparitions-nocturnes',
     'divinites', 'Mélinoé — hymnes orphiques et puissances nocturnes'),
    (399, 'iynx-torcol-roue-magie-amoureuse-pindare-theocrite',
     'sources-anciennes', 'Pindare et Théocrite — persuasion et magie amoureuse'),
    (400, 'enyo-guerre-destructrice-ares-enyalios-tragedie',
     'divinites', 'Ényô — puissances guerrières et violence destructrice'),
    (423, 'apollon-agyieus-seuil-rue-tegee-argos-ambracie-tragedie',
     'cultes-sanctuaires', 'Apollon Agyieus — voies, piliers et seuils sacrés'),
)


class GreekThematicReconciliationTests(unittest.TestCase):
    def test_ten_scholarly_manuscripts_keep_original_number_bibliography_and_sections(self):
        for number, slug, folder, section in CASES:
            name = f'chapitre-{number}-{slug}'
            source = ROOT / 'chapitres' / 'encyclopedie' / (name + '.md')
            with self.subTest(number=number):
                self.assertTrue(source.is_file(), name)
                text = source.read_text(encoding='utf-8')
                self.assertGreaterEqual(len(text), 6000, name)
                self.assertRegex(text.splitlines()[0], r'\b' + str(number) + r'\b')
                self.assertRegex(text.casefold(), r'bibliograph')
                self.assertGreaterEqual(len(re.findall(r'^## ', text, flags=re.MULTILINE)), 6)
                # Le retour s'insère autour du lecteur HTML, sans modifier ce Markdown.
                url = '/chapitres/encyclopedie/' + name + '/'
                actual = classify(url, 'Zeus et Homère cités au passage',
                                  'Chapitre universitaire')
                self.assertEqual(actual, (folder, section), name)
                self.assertNotEqual(actual[1], 'Nouvelles études à classer', name)

    def test_small_screens_and_native_disclosures_stay_accessible(self):
        self.assertIn('@media(max-width:700px)', CSS)
        self.assertIn('@media(max-width:400px)', CSS)
        self.assertIn('.greek-folder-credit summary{display:list-item;min-height:44px', CSS)
        self.assertIn('.greek-complete-catalogue>summary{display:list-item;min-height:44px', CSS)
        self.assertIn('.greek-folder-links a{display:flex;align-items:center;min-height:44px', CSS)

    def test_unidentified_future_chapter_remains_visible_without_speculative_assignment(self):
        self.assertEqual(
            classify('/chapitres/encyclopedie/chapitre-9999-unknown-rites/',
                     'Mots trompeurs Apollon Artémis Zeus', 'Chapitre universitaire'),
            ('sources-anciennes', 'Nouvelles études à classer'))


if __name__ == '__main__':
    unittest.main()
