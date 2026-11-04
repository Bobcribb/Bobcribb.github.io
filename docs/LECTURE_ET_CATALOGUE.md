# Catalogue et lecture — 4 novembre 2026

Le générateur conserve le corpus et ajoute une couche de navigation reproductible.

- `/catalogue-integral/` : toutes les entrées avec identifiant stable dérivé de l’adresse, collection, sujets et filtres.
- `/etat-du-corpus/` : comptes par collection, distinction entre pages construites, vérification HTTP et relecture scientifique.
- `/parcours/` : trois itinéraires : mythes grecs, tragédie grecque, récits de création.
- `/methode-editoriale/` : témoignages, hypothèses, interprétations, images et signalement d’erreurs.
- Les longues études reçoivent un sommaire à ancres stables, des commandes de taille, une lecture épurée, l’impression et une reprise locale.
- Les trois études philosophiques sont reliées aux récits, aux éditions de référence et aux six PDF A4 de l’édition du 4 novembre 2026. Leurs empreintes SHA-256, leur format A4 et leur pagination sont vérifiés avec pypdf à chaque construction. Le seuil de 100 pages est contrôlé sur les fichiers d’analyse seule (107, 101 et 103 pages), hors illustrations et bibliographies. Les éditions illustrées comptent 122, 116 et 117 pages.

Les catégories de recherche sont des aides de découverte tirées des titres et des chemins. Elles ne constituent ni une attribution scientifique nouvelle ni une validation du contenu. `scholarly_review` reste `not_certified`.

`catalog/entries.json` expose les adresses, les empreintes et les métadonnées. `catalog/reading-audit.json` bloque les erreurs des nouveaux parcours et signale séparément les liens historiques non résolus. Le workflow compare le catalogue public au catalogue construit, puis contrôle chaque adresse après déploiement. Son rapport HTTP est conservé dans l’artefact `mythos-live-verification`.

La sélection des illustrations continue d’utiliser `editorial_illustrations.py` et son catalogue de notices par sujet. Aucun numéro éditorial, manuscrit ou calendrier horaire n’est modifié par cette couche.

Vérification : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/validate_publication.py`, `python scripts/verify_museum_design.py` ; après déploiement, `python scripts/verify_live_site.py`.
