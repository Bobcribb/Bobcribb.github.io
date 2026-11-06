# MYTHOS — refonte du portail « Mythologies du monde » — 6 novembre 2026

## Source de vérité et garde éditoriale
Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main` contrôlée avant dérivation.
Les règles `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md` et
`docs/PROTOCOLE_DRIVE_VERS_GITHUB.md` ont été relues.
Aucune demande `editorial/inbox/`, aucun registre, numéro de chapitre,
workflow, publication scientifique ou planification horaire n'est modifié.

## Corpus universitaires vérifiés — statut exact
Quatre volumes historiques intégralement conservés sur `main`, avec texte
long et mentions de sources/bibliographie :
- Volume X, *Kalevala*, `bibliotheque-mythologies-du-monde/mythos-volume-10-finno-carelien-kalevala/index.html`, 64 856 caractères HTML.
- Volume XII, *Royaume de Koush et Méroé*, `bibliotheque-mythologies-du-monde/mythos-volume-12-koush-meroe-apedemak/index.html`, 66 918 caractères HTML.
- Volume XIII, *Arménie, Vahagn et David de Sassoun*, `bibliotheque-mythologies-du-monde/mythos-volume-13-armenie-vahagn-david-sassoun/index.html`, 65 942 caractères HTML.
- Volume XIX, *La Galigo*, `bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/index.html`, 52 355 caractères HTML.

Ils figuraient **déjà** sur le portail et ne sont donc **pas** comptés
comme des premières publications. Aucun de ces textes n'est réécrit ni déplacé.
Les quinze sauvegardes privées WordPress sur Drive sont des brouillons de travail,
signalés explicitement comme non destinés à la publication brute.
La présence et l'intégralité de ces brouillons ne suffisent pas à les déclarer
validés scientifiquement pour diffusion publique. Aucun nouveau manuscrit
universitaire intégral absent du site et approuvé n'a été identifié de façon
certaine dans les sources examinées : **premières intégrations : zéro**.

## Changement de navigation et présentation
- Le constructeur `scripts/build_navigation.py` génère un sommaire ancré
  à trois rubriques, avec contrôle d'unicité des trois intitulés.
- Le document `mythologies/index.html` porte les mêmes ancres :
  `#mythologies-figures`, `#mythologies-traditions`,
  `#mythologies-methodes`.
- La charte `assets/mythos-museum.css` donne au sommaire un cadre anthracite,
  des liens ivoire/or, une grille à trois colonnes sur écran large,
  une colonne sur smartphone, des cibles tactiles de 48 px, le focus clavier,
  et un masquage à l'impression. La bannière commune statue grecque et temple
  demeure inchangée.
- Les cartes des volumes XII (Naqa, vestiges photographiés par LassiHU en 2005)
  et XIII (statue moderne de David de Sassoun photographiée par Marcin Konsek
  en 2014) reçoivent dans la page HTML les images et les textes alternatifs
  déjà définis dans le générateur, avec leurs crédits explicites.
  Les photographies restent distinctes de toute reconstitution 2,5D.
- `tests/test_world_mythologies_toc_20261106.py` contrôle les ancres,
  le lien unique vers chaque volume historique, la présence du texte long
  et de ses mentions documentaires, les deux images/crédits et le CSS responsive.

## Ce qui reste à vérifier après fusion
Exécuter la suite `python -m unittest discover -s tests -v`,
le générateur et les contrôles du manifeste de publication.
Une PR et même sa fusion ne démontrent pas la mise en ligne.
Vérifier `/mythologies/` sur `https://bobmythos.fr`, les deux médias distants
et `/catalog/publication-verification.json` après le déploiement Pages.
