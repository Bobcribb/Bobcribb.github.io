# MYTHOS — Galerie photoréaliste : sommaire stable et protection des notices

**Intervention :** 6 novembre 2026, 21 h 21, Europe/Paris. Dépôt : `Bobcribb/Bobcribb.github.io` ; site : `https://bobmythos.fr`.

## Constat issu des exécutions réelles

L'exécution GitHub Actions de publication `42286197509` et les validations `42287670845` et `42287480652` ont échoué dans les tests `test_gallery_toc_anchor_20261106.py` : la galerie contenait **84 sections scientifiques réelles pour 83 entrées au sommaire** dans les commits concernés. Les erreurs `83 != 84` proviennent de l'ajout concurrent de reconstitutions après la création du sommaire, pas de l'absence de ces études dans le HTML.

Lors du contrôle le 6 novembre après 21 h, `main` présente **86 cartes, 86 ancres scientifiques et 86 entrées de sommaire**. Une autre intervention a donc déjà réaligné le HTML source. Ce chantier ne modifie aucune carte existante ; il sécurise le processus pour les ajouts futurs.

La collision de cote historique **MC-109**, vérifiée en parallèle, a également été réconciliée par un autre travail sur `main` : la première soumission `0b2e3ecb-74df-4bc3-9776-202611061953` (*Visages substitués*) conserve le volume CCCXVIII (318). Le manuscrit distinct `a6c192ec-148a-4ba1-a909-202611061954` (*Les ombrelles du sacré*) est préservé dans `editorial/holds.json`, avec son empreinte SHA-256 inchangée. Aucune attribution ni duplication n'est faite ici.

## Correctif de pérennisation

Le nouvel utilitaire `scripts/sync_photoreal_toc.py` reconstruit **uniquement** le bloc de sommaire généré `details.mythos-gallery-toc` depuis chaque section `article.r3d-card` et son `h2[id^="lecture-section-"]` :

- `python scripts/sync_photoreal_toc.py --check` vérifie le nombre, les liens et les labels, sans écrire ;
- `python scripts/sync_photoreal_toc.py --write` corrige seulement ce sommaire si un nouveau dossier a été inséré ;
- refuse les IDs dupliqués, les titres de carte ou les sections manquants et les sommaires ambigus ;
- conserve l'ordre **réel de lecture** de la page, même lorsque les identifiants historiques ont été attribués dans un ordre différent ;
- respecte toutes les images WebP, les notices, les légendes, les dates, les sources archéologiques et les liens de galerie.

`tests/test_sync_photoreal_toc_20261106.py` vérifie l'idempotence, une carte ajoutée dans un jeu d'essai, la réécriture limitée à la navigation, le mode lecture seule et les refus des sections invalides. `AGENTS.md` documente désormais l'étape à suivre **après chaque insertion d'une nouvelle carte**.

## Portée et suivi de publication

Quatre fichiers seulement sont ajoutés ou modifiés par ce travail : un script d'entretien, un test, `AGENTS.md` et ce rapport. Aucune étude du corpus n'est créée, réécrite ou retirée. Aucune cote canonique, aucun reçu, aucun workflow GitHub Actions ni aucune planification automatique n'est changé.

Le site public reste à contrôler indépendamment après déploiement. Les requêtes externes disponibles pendant cette intervention n'ont pas permis de lire de nouveau le manifeste HTTPS ; la présence d'un commit sur `main` ne démontre pas à elle seule sa publication sur le domaine. Vérifier GitHub Actions, les 86 liens de la galerie du rendu et `/catalog/publication-verification.json` avant d'annoncer un résultat public.
