# MYTHOS — Refonte de l'en-tête mobile : cibles tactiles et contrôles réels

**Intervention du 6 novembre 2026, 17 h 55 (Europe/Paris).** Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`, domaine public `https://bobmythos.fr`.

## État réel contrôlé avant modification

- `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relus : les cinq collections restent sous attribution atomique ; aucune planification horaire ne doit changer.
- La publication GitHub Pages `42254292001` a **réussi** le 6 novembre 2026. Son manifeste HTTPS `/catalog/publication-verification.json` indique la source `3b3d181c640f7f097f16c9e112b0076203cfa3fa`, l'exécution `42254292001` et **1 699 documents indexés**.
- L'audit `42254291988` est réussi et les huit dossiers thématiques grecs sont accessibles sur le domaine public. Le commit `main` a ensuite avancé vers `d2b92e486b4bc719100c1daf2d9d8277fc19fa7e` (rendu GitHub généré).
- L'édition scientifique, les 27 archives des Origines du sacré, les médias vérifiés et les photographies archéologiques ne doivent pas être recopiés ou transformés.

## Anomalie UX vérifiée dans la feuille de style

`assets/mythos-museum.css` définissait dans le masthead :

- `.mythos-search-link` : **25 × 25 px**, en dessous d'une cible tactile confortable ;
- `.mythos-menu summary` : **28 × 38 px**, également trop petite pour les usages mobiles.

Le menu natif `<details>` était déjà compatible avec le clavier et les lecteurs d'écran : aucune nouvelle dépendance JavaScript n'est requise.

## Intervention technique

- Agrandir les deux cibles à **44 × 44 px** tout en conservant le pictogramme de recherche de 23 px et les trois traits du menu dans la palette ivoire/or.
- Ajouter des états focus et hover distincts sans modifier la bannière statue grecque/temple ni ses règles de cadrage.
- Sur les téléphones de largeur inférieure ou égale à 420 px, réduire les espacements de l'en-tête et ajuster proportionnellement la taille de la marque pour prévenir son chevauchement avec les contrôles.
- `tests/test_museum_header_touch_targets_20261106.py` : contrôler les tailles CSS, les libellés accessibles et la présence du menu natif dans l'accueil, l'encyclopédie grecque, le théâtre et les Origines.
- `scripts/verify_greek_navigation.cjs` : vérifier par navigateur Playwright les dimensions réellement calculées sur ordinateur, tablette et smartphone ; vérifier l'absence de chevauchement sur un écran compact de 360 px et conserver une capture de contrôle.

## Périmètre strict et conditions de publication

Les changements touchent exclusivement le CSS partagé, les contrôles navigateur et les tests, plus le présent rapport. Ils **ne modifient** aucun manuscrit, registre `editorial/numbering.json`, fichier `editorial/inbox/`, image, reconstitution photoréaliste, texte d'archive ou workflow de planification.

La fusion GitHub n'est pas à elle seule une preuve de déploiement. Contrôler successivement les tests GitHub Actions, l'audit, le workflow de publication Pages, puis la version HTTPS et l'en-tête mobile réel. Le manifeste public doit ensuite annoncer un commit source qui contient cette correction.

## Rectification du contrôle navigateur — incident de séquencement

Le lancement indépendant `42258572814`, déclenché dès la fusion du correctif `91557ffd09227b6c12253cf1a753f0aeec8db226`, a signalé **25 × 25 px** sur `/mythologie-grecque/`. Cette mesure concerne l'ancienne version **encore servie par bobmythos.fr** ; elle ne prouve pas une régression du CSS de la branche fusionnée. Le navigateur était exécuté avant la publication correspondante.

Pour que les contrôles soient techniquement significatifs :

- `verify-greek-navigation.yml` conserve son audit indépendant sur push (navigation, liens, absence de débordement), mais **ne force pas** la condition 44 px avant le déploiement.
- `publish.yml`, sans changement de déclencheurs, de planifications ou de concurrence, transmet `MYTHOS_ENFORCE_TOUCH_TARGETS: '1'` seulement lors de son contrôle navigateur **après** `actions/deploy-pages@v4`.
- `scripts/verify_greek_navigation.cjs` exige alors les surfaces 44 × 44 sur tous les formats et le non-chevauchement à 360 px, et conserve une capture ; le rapport inclut le mode de contrôle.
- Un test de non-régression vérifie la présence de cette condition dans les deux circuits et son ordre après déploiement.

**Statut d'intégration et de publication à distinguer :** même si les fichiers sont fusionnés dans `main`, seul un nouveau workflow Pages réussi, suivi des mesures du site public en mode strict, autorise à conclure que la correction mobile est effectivement visible.
