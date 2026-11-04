# Illustrations éditoriales — correction du 4 novembre 2026

## Règle de publication

Les deux distributeurs automatiques de `build_native.py` et de
`build_navigation.py` sont remplacés par `scripts/editorial_illustrations.py`.
Toutes les collections partagent la même règle : seul un sujet explicite du
titre du chapitre ou de son propre slug permet de choisir un média. Les noms
des collections, les menus, les paragraphes comparatifs et les anciennes
galeries ne servent pas de critères. Il n'y a plus de rotation par chemin ni
de collection grecque par défaut.

`scripts/editorial_media.json` référence 90 médias locaux et les notices
documentées déjà présentes dans les articles du dépôt. Chaque entrée conserve
son texte alternatif, sa légende, ses crédits, les liens de provenance et de
droits, et la page d'où la notice a été reprise. Le commit d'origine est
enregistré dans le catalogue. La sélection conserve les réserves des notices
(réception moderne, identification discutée, photographie de vestiges, etc.).

Une notice ne s'applique pas à toute une civilisation. Ainsi, le papyrus de
Derveni est sélectionnable pour Derveni, le relief de Behistun pour Behistun,
et l'hydrie de Médée pour Médée. Le Mithras romain n'est pas automatiquement
assimilé au Mithra iranien. Une image manquante est omise sans remplacement.

## Cas signalés et conservation

- **471 — Inde, yuga et calendriers** : aucune galerie automatique ; aucun
  document directement adapté n'est présent dans la sélection locale.
- **462 — Égypte, sistre et Hathor** : même traitement ; le papyrus d'Ani et
  la chambre d'Ounas ne sont pas des illustrations du sistre.
- Les anciennes galeries générées sont retirées du rendu, y compris celles
  recopiées dans les HTML historiques. Les figures, notes et études rédigées
  à l'intérieur des articles restent intactes.
- Au maximum quatre documents sont ajoutés, sans répéter une image déjà dans
  l'article (y compris ses variantes avec paramètres ou adresses historiques).
- Les vignettes génériques des 27 tomes ont été retirées du portail des
  Origines du sacré. Une céramique grecque ne doit pas illustrer Hohle Fels,
  ni Mycènes la préhistoire du sacré. Les 27 titres et liens sont conservés.

## Vérifications

```sh
python -m unittest discover -s scripts -p 'test_editorial_illustrations.py' -v
python scripts/build_native.py
python scripts/validate_publication.py
python scripts/audit_integrity.py
```

Seize tests couvrent les deux signalements, les autres collections, les
titres Unicode, les limites de mots, la distinction Mithra/Mithras, les
médias absents, les doublons, les anciens HTML, l'idempotence et la
conservation des notes ainsi que du menu. Le nouveau graphisme conserve ses
couvertures décoratives uniquement pour une liste de portails nommés : une
carte de chapitre ne reçoit jamais leur image par héritage de collection ni
le cratère de Derveni par défaut.

Sur la reconstruction comparée du commit `871b5333c2faadcba16b97b1a3b6694482052449`,
1 062 corps d'articles restent identiques après sérialisation HTML. Seuls le
portail des Origines (vignettes retirées) et le catalogue théâtral généré
(contenu textuel inchangé) diffèrent. L'audit de cette reconstruction
vérifie 110 médias et 1 078 entrées, sans erreur ni avertissement.
Les chapitres 471, 462 et le volume CL sur Médée ont été contrôlés visuellement
dans le navigateur, avec chargement effectif de l'hydrie et affichage des crédits.

Les modifications du workflow portent sur les fichiers déclencheurs et les
tests de régression ; aucune planification horaire n'est modifiée.

## Ajouter une illustration

1. Vérifier le rapport précis entre le sujet et l'objet représenté.
2. Utiliser un fichier local et une notice de provenance vérifiable.
3. Ajouter une entrée au catalogue avec des sujets précis, sans catégorie
   générique telle que « sacré », « Égypte », « philosophie » ou « théâtre ».
4. Indiquer la page de provenance, la licence, l'auteur du cliché et les
   limites de l'identification ; ne pas transformer une hypothèse en fait.
5. Exécuter les tests et reconstruire. Ne pas imposer d'image à un chapitre
   pour atteindre un quota.


Les réconciliations de numérotation et la file éditoriale ajoutées en parallèle
sont conservées. Cette correction ne change aucun manuscrit ni aucun registre
de numérotation.


## Enrichissement des articles — 4 novembre 2026

À la demande de Boris, le catalogue passe de 56 à 90 documents : 34 notices
provenant des articles existants, avec leurs crédits et leurs liens de licence.
Les ajouts concernent notamment Apollon, Arès, Héphaïstos, Héra, Hadès,
Perséphone, Orphée, Hermès, Asclépios, Médée, Achille, l’Iliade et l’Odyssée,
les sanctuaires grecs, Persépolis, les cultes domestiques romains et Śiva.
Aucune illustration générique n’est imposée aux autres sujets.

La sélection ajoute jusqu’à quatre images distinctes par page. L’hydrie
07.128.1 du Met et le plan de Délos disposent aussi de correspondances avec
leurs autres noms locaux pour éviter les répétitions du même document.
Les galeries affichent deux grandes images par ligne sur ordinateur et une
sur petit écran ; les images ne sont pas recadrées et ouvrent leur fichier
original au clic. Le chargement différé est conservé.

Comparaison sur le commit source `8eb71e88276de0275d236a69d3ead16b12b1f6a3` :
90 pages d’articles reçoivent 140 images supplémentaires. Ce sont des
occurrences supplémentaires dans les articles, pas 140 œuvres nouvelles.
Les 110 fichiers du fonds documentaire original restent inchangés.

Validation locale : 105 tests du dépôt et 16 tests iconographiques réussis.
Les manuscrits, leur numérotation et les planifications restent inchangés.


## Conservation lors des publications rapides

Le constructeur d’instantané des reconstitutions applique désormais le même
catalogue aux copies HTML des articles. Il ne modifie aucun fichier source.
Les titres déplacés dans la bannière muséale sont reconnus, ainsi que le titre
d’œuvre sous une bannière limitée au numéro (y compris les numéros romains
suivis de leur équivalent décimal). Une simple sous-section comparative ne
sert toujours pas de critère.

Validation sur main après enrichissement : 113 tests généraux, 18 tests
iconographiques ; instantané complet de 1 202 pages, six PDF et 28 WebP.
Les 140 ajouts des 90 articles sont présents, et aucune image des anciennes
galeries documentaires des chapitres n’est perdue. La publication rapide
actualise 212 galeries, sans réécrire les manuscrits ni leur numérotation.
