# MYTHOS — Refonte : quatre études de transmission et de réception

**Contrôle : 5 novembre 2026, 08 h 00 UTC (09 h 00 à Paris, environ).**  
**Dépôt :** `Bobcribb/Bobcribb.github.io`, branche `main`.

## 1. Garde éditoriale et état des demandes

`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus avant toute écriture. Le `main` initial contrôlé était `e56015fa796362e2266bfc8dde42538bbb628393`. Le circuit concurrent sous `editorial/inbox/<uuid>.json` avec placeholders `{{numero}}` et `{{volume}}` reste inchangé.

La lecture des données de `main` du 5 novembre indique **336 objets JSON dans `editorial/inbox/`**, **331 attributions dans `editorial/numbering.json`** (72 Origines, 75 Encyclopédie, 48 Comédies, 48 Tragédies, 88 Comparatif) et **5 demandes en retenue dans `editorial/holds.json`**. Pas de nouvelle demande valide connue hors de ces deux états. Les cinq retenues doivent rester intactes jusqu'à rapprochement des collisions ; ne pas créer d'UUID de substitution.

Les quatre sources historiques examinées sont **déjà publiées** sous `/bibliotheque-mythologies-du-monde/`. Elles étaient absentes des liens `RELATED` du portail grec ; leur intégration dans le sommaire grec ne constitue **pas** une première publication. Aucune autre source universitaire **intégrale, nouvelle, publiable et vérifiée comme inédite**, n'a pu être établie à partir des sources examinées. Les sauvegardes privées WordPress précédemment inventoriées ne sont pas une autorisation de les publier ; aucun de ces brouillons n'a été exposé.

## 2. Quatre textes préexistants, préservés intégralement

| Étude complète | Volume HTML | SHA Git de la source au contrôle | Rubrique grecque |
| --- | ---: | --- | --- |
| Égypte ptolémaïque : Alexandrie, Sérapis, Lagides et Cléopâtre | 12 719 caractères | `0f21deac1b6d86bf196a401a39371c88c354bf76` | Cultes et sanctuaires → Alexandrie |
| Étrusques : cités, religion, iconographie et divination | 24 899 caractères | `a637187545291210b488f602e296079cac8c18e6` | Sources anciennes → Étrurie |
| Iran ancien : Achéménides, inscriptions, Persépolis et sources grecques | 25 588 caractères | `d5639b0d6c573ade1ab7021edbbdf57d4e633e47` | Sources anciennes → Iran achéménide |
| Anatolie hittite : Hattousa, Kumarbi et successions divines | 29 125 caractères | `69a7bcde37c3d619cfae4137832a194571914c75` | Sources anciennes → Hattousa |

Chaque fichier présente des sections développées et des références/bibliographies ; certains signalent explicitement que la consolidation critique continue. Le classement repose sur le **sujet principal**, non sur la mention incidente d'un dieu ou d'une cité. Ces études ne sont **ni copiées ni déplacées ni résumées**. Le corpus de référence, les sources originales, URLs, manuscrits numérotés, cotes et registres ne sont pas modifiés.

## 3. Intégration et ergonomie

- `scripts/build_greek_corpus.py` : quatre références supplémentaires dans l'entrée unifiée `/mythologie-grecque/`. Une seule entrée de navigation grecque reste autorisée.
- `scripts/build_greek_folders.py` : rattachement à des sous-dossiers précis, liens de retour et panneau **« Mondes grecs : transferts, lectures et sources »**. Sur chacune des quatre pages, trois liens vers les autres textes, soit **douze liens dirigés**. Le panneau est inséré **hors de l'article** ; son recalcul est idempotent, sans second exemplaire après reconstruction.
- `assets/mythos-museum.css` : encadrement doré, fond noir/anthracite, typographie adaptée, rupture mobile sous 480 px. La grille partagée des lectures croisées est à une seule colonne sous 700 px et les liens ont une cible tactile d'au moins 44 px.
- Aucune ancienne illustration 2,5D n'est réintroduite ; la bannière statue grecque/temple et les images archéologiques sourcées sont conservées.

Le rapprochement est explicitement **critique et historiographique** : Alexandrie lagide, Étrurie, empire perse et monde hittite ne représentent ni une culture homogène ni une transmission automatique de toutes les traditions.

## 4. Tests, transactions et déploiement

Les validations ajoutées dans `tests/test_greek_folders.py` vérifient les sources intégrales présentes, les rubriques, les destinations `RELATED`, les liens réciproques, le respect des articles et deux reconstructions identiques. Les contrôles de `verify()` refusent les panneaux absents, dupliqués ou comportant un renvoi manquant.

Commits fonctionnels :
- `d3c193718a9443eb07a92cf048bacb08029f5e1a` : catalogue grec.
- `26b9eeb6bdb7dc3f8ca97aa174728f7ecc100c24` : classement, navigation et vérification.
- `ed70b5696abd73f673148d72413f14ee1f0863df` : adaptation noire et dorée.
- `20bc97382f79e9149450a4f76e8b5f1f92c49992` : tests d'intégrité.

Au contrôle du 5 novembre, l'exécution GitHub Actions de validation `41991649310` était `in_progress` et l'exécution de publication `41991649539` était `pending` pour le commit `20bc97382f79e9149450a4f76e8b5f1f92c49992`. Les exécutions antérieures de publication ont été annulées lorsque de nouveaux commits sont arrivés. Le reçu du dépôt `catalog/publication-verification.json` indiquait encore la source `7da6b10c5a90fb0b8ec9b4c814383251e2423917`, **1 455 documents, 27 archives et 110 médias**, donc une version précédente. Les deux URLs HTTPS de `bobmythos.fr` interrogées directement n'ont pas répondu via l'outil de vérification. **Aucune réussite de déploiement public n'est donc revendiquée.**

**Limite de validation :** avant de déclarer la mise en ligne, obtenir une exécution de publication réussie et un reçu public `/catalog/publication-verification.json` faisant référence à un commit englobant les changements, puis contrôler les quatre pages HTML servies.

Aucune automatisation, fréquence, allocation canonique ou archive n'a été modifiée par cette intervention.
