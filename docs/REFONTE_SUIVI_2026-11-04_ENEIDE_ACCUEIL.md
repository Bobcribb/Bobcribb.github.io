# MYTHOS — Refonte : quatre œuvres d'étude et accès à l’Énéide

**Date de contrôle : 4 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`.

## 1. Garde éditoriale et inventaire

À l'ouverture de cette séance, `main` pointait sur `e8c5ec3e1aa06f6a7d53ff5bf18d405532425eba`. Les instructions `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relues sur `main` **avant toute intervention**, en particulier l'obligation d'utiliser `editorial/inbox/<uuid>.json` et les reçus GitHub Actions pour les cinq collections numérotées.

L'inventaire à cette photographie a trouvé **241 demandes** dans `editorial/inbox/`, **234 allocations** enregistrées dans `editorial/numbering.json`, **5 mises en attente explicites** dans `editorial/holds.json` et **2 demandes déjà soumises, sans reçu** :

- `7cd8d3a2-44ff-4d66-8bc3-7ab2d2858e90` : **Bendis**, étude grecque intégrale de **56 154 caractères Markdown**, `encyclopedie`, `{{numero}}` encore provisoire.
- `519d3d78-86ef-4f76-a502-25e48c9a0054` : **MC-054 — Quand les dieux rient**, étude comparative de **115 436 caractères Markdown**, `comparatif`, `{{volume}}` et `{{numero}}` provisoires.

Les deux manuscrits sont déjà dans la file officielle. Les publier en double ou fixer leur numéro hors de GitHub Actions violerait la garde ; aucune soumission nouvelle n'a été créée. Les 135 brouillons WordPress sauvegardés dans Google Drive sont des archives privées, exclues de la publication. Les études intégrales candidates déjà présentes ont été vérifiées contre leurs lecteurs et leurs circuits de publication.

**Nouveau texte universitaire inédit ajouté lors de cette exécution : aucun.** Aucun autre manuscrit intégral nouveau, disponible, non publié et approuvé n'a été identifié dans les sources inspectées. L'absence de nouvelle étude n'autorise ni récit fictif, ni résumé de remplacement, ni réédition du même texte.

## 2. Contenu universitaire existant désormais mieux accessible

Le fichier `assets/philosophie/eneide-pagination.json` confirme une **première livraison de l’Énéide** présentant **76 pages A4 d'analyse**, **84 pages PDF au total**, **30 402 mots** et **18 fichiers sources Markdown**, pour un objectif éditorial **inachevé** de 300 pages. La page de lecture intégrale de cette première livraison était déjà disponible : `/philosophie-eneide.html`. Aucune analyse n'a été abrégée ni dupliquée dans l'accueil.

L'accueil `index.html` possède maintenant **quatre cartes illustrées** au lieu de trois : `/philosophie-iliade.html`, `/philosophie-odyssee.html`, `/philosophie-theogonie.html` et `/philosophie-eneide.html`. La carte de Virgile indique honnêtement son état partiel, sans prétendre avoir atteint les 300 pages.

L'illustration de l’Énéide utilise le média local archivé `media/2026/10/mythos-troie-vi-porte-est-hisarlik-cherryx-2012.jpg`, présent dans `media/manifest.json` avec empreinte SHA-256 `a7f4f2f46523a6da9cfe6a1bc89b2f63dbb2c7f789fdd97c111a631736e83304`. L'attribut `alt` décrit explicitement **les vestiges archéologiques de Troie VI**, non une scène certaine du poème de Virgile.

## 3. Graphisme, navigation et conservation

- `index.html` : passage cohérent de « Trois œuvres à approfondir » à **« Quatre œuvres à approfondir »**, ajout de la carte et d'un avertissement sur le chantier incomplet de l’Énéide. Le sommaire conserve `#home-oeuvres`.
- `scripts/apply_museum_design.py` : mapping de la photographie locale, sommaire mis à jour et conservation de son texte alternatif après des passes muséales répétées. Si l'image référencée disparaît, la génération doit échouer, non la remplacer silencieusement.
- `assets/mythos-museum.css` : grille quatre colonnes sur grands écrans, deux sur tablette, une sur téléphone ; cartes noires, accents ivoire et or, images bien cadrées. L’identité statue grecque/temple reste inchangée, aucun SVG 2,5D n'est réintroduit.
- `tests/test_home_eneide_cards.py` : trois tests de lecteurs existants, pagination, absence de doublons, stabilité des images et sommaires lors de deux reconstructions, signalement d'un média absent.
- `tests/test_museum_home_toc.py` : adaptation du cas de contrôle à quatre œuvres après constat qu'une validation précédente échouait sur l'ancien intitulé « Trois œuvres ».

## 4. Commits

1. `856dfd4b64da33594e527748433e03e1ba8733e1` — nouvelle carte Énéide dans l'accueil.
2. `eff63dc8b787df410038513faedc8611ec886226` — couverture et sommaire muséal.
3. `3a0cae4089032b06ce19e9c9df95ae579129ab20` — styles noirs et or adaptatifs.
4. `e72aaf9aa397acf0751cfcb72d77536b3dbf84b6` — conservation du texte alternatif et refus d'une image manquante.
5. `e4519da23887ace051942339716a216df3fca168` — tests des quatre cartes.
6. `24642ca7b1529d7fdb43f59dff17e7b0de9bab38` — alignement du test de sommaire.

## 5. Déploiement et vérifications

La dernière consultation indépendante de `https://bobmythos.fr/catalog/publication-verification.json` confirme la version publique **antérieure** `source_commit=4b4cc6c3874398cd6c8b7e638e493cc8707381fb`, avec **1 358 documents indexés**, **27 archives** et **110 médias** vérifiés. Le sommaire des neuf études critiques d'Aristophane, réalisé dans une intervention précédente, est effectivement visible sur `https://bobmythos.fr/theatre/` : cette publication est confirmée.

**La nouvelle carte de l’Énéide n'était pas encore confirmée sur le domaine** au dernier contrôle. GitHub Actions réalise encore les validations des nouveaux commits. Ne pas confondre inscription des fichiers sur `main` et déploiement réussi.

Les vérifications restant nécessaires pour le nouveau changement sont : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, la conclusion réussie du workflow Pages, l'absence de doublons dans `#home-oeuvres`, le maintien de l'ALT des vestiges de Troie et l'évolution du reçu public.

**Aucune intervention** sur les cinq registres d'attribution, les manuscrits universitaires, les archives, les workflows GitHub, les autres automatisations MYTHOS ou leurs planifications horaires.
