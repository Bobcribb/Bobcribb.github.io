# MYTHOS — Refonte de la bibliothèque de l’Énéide : dix-huit sources intégrales et parcours croisés

**Contrôle du 6 novembre 2026, séance de reprise de la refonte.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`. Site cible : `https://bobmythos.fr`. État initial relu : `e5e8ea209b17587b5bbd8ab02608198f905cf846`.

## 1. Contrôle documentaire et garde éditoriale

Avant toute modification, lecture de `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, `EDITORIAL_CONTINUITY.md` et `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md`, inspection de l'arbre GitHub (5 508 entrées à la photographie initiale), du générateur `scripts/build_native.py`, des portails et des dossiers d'archives déjà rattachés. L'étude philosophique de l'Énéide et le récit historique d'Énée ont été relus à leurs URL GitHub, avec contrôle des dix-huit sources de `corpus/philosophie/eneide/` et des dix-huit ancres de l'édition HTML.

Les neuf dossiers des comédies perdues et neuf tomes historiques des *Origines du sacré* avaient déjà été conservés dans GitHub, avec leurs études, sources et lecteurs. Les resoumettre comme études nouvelles constituerait une duplication. Le document Google Drive `MYTHOS — LIRE EN PREMIER — index et contrôle des 135 brouillons` précise expressément **« Ne pas publier ces documents sur GitHub »** ; les 134 pages et l'article WordPress sont des archives privées, non autorisées pour import automatique. Les sujets en file `editorial/inbox/` ou en retenue `editorial/holds.json` ne sont pas réattribués.

**Premières publications d'études universitaires inédites : 0.** Aucun nouveau manuscrit complet, distinct, encore inédit et explicitement approuvé à la publication n'a été établi parmi les sources consultées. Aucune nouvelle demande d'attribution n'est déposée : ni `editorial/inbox/`, ni `editorial/numbering.json`, ni les cinq collections numérotées ne sont modifiés.

## 2. Lacune d'accessibilité repérée et correction

Les **dix-huit manuscrits originaux Markdown de l'étude universitaire existante de l'Énéide** sont conservés dans `corpus/philosophie/eneide/` et leur texte est déjà intégré à la page `/philosophie-eneide.html`. Ce lecteur est une **première livraison de 76 pages A4 d'analyse** (84 pages PDF), et non l'étude finale de 300 pages demandée. La bibliothèque narrative conserve aussi une page spécifique au cycle d'Énée et Didon à `/bibliotheque-mythologies-du-monde/heros-mythologies-monde-cycles-epiques/cycle-enee-didon-eneide-romaine/`.

**Lacune vérifiée en HTTPS avant déploiement :** `https://bobmythos.fr/corpus/philosophie/eneide/00-introduction.md` renvoyait **404**, alors que son texte figure intégralement dans le dépôt et dans le lecteur HTML. Le générateur initial n'exportait les sources `.md` de `corpus/` que lorsqu'elles figuraient déjà en liens dans les HTML préexistants, condition non satisfaite pour l'Énéide.

La correction `scripts/eneide_source_access.py` :
- valide **chacun des dix-huit** fichiers de source (fichiers explicites, longueur minimale, titre Markdown et identité du titre `h2` dans le lecteur `/philosophie-eneide.html`) et la présence du dossier bibliographique final ;
- refuse une source manquante ou divergente, puis copie les **dix-huit fichiers byte-for-byte** dans `_site/corpus/philosophie/eneide/` : aucun texte n'est résumé, paraphrasé, numéroté ou modifié ;
- crée un sommaire indépendant de dix-huit liens directs vers les sources Markdown ; maintient inchangés les dix-huit chapitres déjà rendus en HTML, leurs références, leur lecteur et leur PDF ;
- crée un lien réciproque entre la lecture narrative d'Énée et Didon et l'étude universitaire distincte, pour éviter toute confusion entre récit et analyse critique ;
- n'intervient que sur le **rendu** du site, sans réécrire les fichiers sources HTML ou Markdown du dépôt, les archives ni les cotes.

`scripts/build_native.py` appelle ce module après les transformations générales, avant la compilation des PDF et le contrôle de publication. Cette intervention concerne un corpus **hors des cinq collections numérotées** : elle n'attribue aucun numéro.

**Statut éditorial exact :** ces dix-huit textes sont **déjà publiés** sous forme d'étude HTML universitaire. Ce qui est nouveau est leur **diffusion séparée, sans troncature, en fichiers sources Markdown directement accessibles sur le site** après déploiement, et les liens entre les deux parcours. Ne pas présenter cette amélioration comme la création d'un nouveau livre inédit.

## 3. Design, lisibilité et navigation

`assets/mythos-eneide-sources.css` introduit un panneau documentaire anthracite, ivoire et or compatible avec la charte muséale existante, un sommaire à deux colonnes passant à une colonne sous 680 px, des liens tactiles de 44 px, un focus clavier explicite et des styles d'impression. La bannière de référence (statue grecque à gauche, temple à droite) et les autres portails restent inchangés. Aucun schéma 2,5D ni menu incrusté à des images n'est réintroduit.

Le nouveau module rend ses panneaux de manière idempotente grâce à `data-mythos-eneide-sources` pour éviter les doublons au second rendu. Le test `tests/test_eneide_source_access_20261106.py` vérifie les dix-huit copies exactes, les liens réciproques, l'idempotence, l'arrêt si une source manque et le refus d'un titre HTML divergent.

## 4. Commits créés sur `main`

- `ea7e39d019e060918acbbf1ba66a8e03ae40c4a8` — module de contrôle et d'accès aux sources complètes ;
- `56c103f936e99306a263355295a65accf6761d17` — feuille CSS responsive noir et or ;
- `1f2844c1ba912e3ab9dba61199cb649daeb65c34` — correction des expressions régulières ;
- `a9ca2c2ae39fdd0632f9879c14d459a5461ca73c` — raccordement du module au générateur public ;
- `afb3c6b46d0b6cf5103324fb71fb72ea600f094e` — tests d'intégralité et d'idempotence ;
- `eb6f5de78c6d08e6a7b0e7172e91c4dfbb5cb001` — correction du contrôle des premières lignes Markdown.

## 5. GitHub Actions et preuve publique

Le contrôle du manifeste public `https://bobmythos.fr/catalog/publication-verification.json` donnait encore `source_commit=00c888fd4b1f2d9a83beb82c40012f2eceb562a4`, `github_run_id=42163598977`, 1 594 dossiers indexés, 27 archives et 110 médias. Il est antérieur aux présentes modifications. Les URL HTML de l'Énéide existent et son sommaire de dix-huit sections est public ; **les dix-huit fichiers sources nouveaux ne sont pas encore confirmés en HTTPS**.

Une première CI `42166150544` sur `afb3c6b` a échoué sur les quatre tests nouvellement introduits en raison d'une expression régulière trop restrictive, corrigée ensuite dans `eb6f5de`. Cette première CI n'est **pas** une validation finale. Vérifier le nouveau workflow, puis le manifeste public et, au minimum, `/corpus/philosophie/eneide/00-introduction.md` et `/corpus/philosophie/eneide/17-reperes-et-sources.md` avant d'annoncer la diffusion effective.

**Préservation :** aucun numéro canonique, registre, reçu, texte universitaire historique, brouillon Drive, archive, domaine, workflow ou planification horaire MYTHOS n'est modifié par cette séance.
