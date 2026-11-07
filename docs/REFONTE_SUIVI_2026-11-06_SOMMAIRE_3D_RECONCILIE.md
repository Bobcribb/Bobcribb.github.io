# MYTHOS — Sommaire 3D auto-réconcilié et navigation profonde

Séance du 6 novembre 2026. Source de vérité inspectée avant écriture : `main` au commit `e87e8f92017a36ebcb7a66a4a68c33d0358aa5d4`. Consignes `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relues.

## 1. Inventaire et intégration des textes

Sur `main`, la galerie photoréaliste contenait **86 sections scientifiques et 86 liens de sommaire sans doublon**. Les archives universitaires examinées sous `corpus/mythologie-grecque/`, les tomes historiques sous `corpus/origines-du-sacre/` et les neuf éditions documentaires de `corpus/theatre-grec/comedies/` étaient déjà en HTML ou reliées à leurs copies Markdown intégrales. Les sources de l'Énéide sont déjà distribuées par `scripts/eneide_source_access.py`.

**Nouveau manuscrit universitaire initialement non publié et approuvé identifié : aucun.** Les brouillons WordPress conservés dans Google Drive portent une interdiction de publication brute dans leur index de sauvegarde. Ne pas contourner cette restriction, dupliquer un volume ni inventer un manuscrit. L'allocation des cinq collections numérotées reste réservée à GitHub Actions et aux reçus de `editorial/numbering.json`.

## 2. Échec technique documenté

Les exécutions de validation du 6 novembre ont échoué lors de tests imposant à la **source HTML** une égalité immédiate entre sections et liens, alors que les nouveaux dossiers 3D sont ajoutés en concurrence : par exemple 83 liens dans le sommaire pour 84 sections déjà présentes. Le moteur `scripts/improve_reading.py` reconstruit pourtant intégralement le sommaire depuis les sections réelles lors du rendu. Conserver l'assertion stricte avant cette passe bloque inutilement la publication, même sans ancre cassée.

## 3. Intervention

- `scripts/improve_reading.py` : contrôler à la fin de la génération que l'ordre de **tous** les liens correspond exactement à toutes les sections H2, que chaque cible existe et que les identifiants sont uniques. Les doublons restent une erreur bloquante. Aucun texte ou média n'est réécrit.
- `tests/test_gallery_toc_anchor_20261106.py` : conserver le contrôle strict des liens déjà présents dans le HTML source, mais laisser un nouveau dossier sans entrée de sommaire **jusqu'à la reconstruction** ; simuler l'ajout d'une 87e notice, vérifier que le moteur produit toutes les entrées, conserve les paragraphes et reste idempotent. Vérifier qu'une collision d'identifiants provoque bien un échec.
- `assets/mythos-discovery.css` : améliorer la lisibilité des titres atteints par lien profond dans la galerie, y compris sur mobile, sans modifier la bannière statue/temple ni le style noir, or et ivoire.

## 4. Vérifications et publication

Les contrôles ciblés doivent être validés par la CI du dépôt, puis par la reconstruction `scripts/build_native.py`, les tests globaux et `scripts/verify_publication.py`. **Aucun déploiement HTTPS n'est revendiqué sans un workflow réussi et un manifeste public concordant** ; le domaine `bobmythos.fr` n'a pas été accessible pour une inspection réseau directe depuis cette séance.

Aucune modification aux manuscrits, aux sources antiques, aux bibliographies, à `chapitres/`, aux demandes `editorial/inbox/`, aux registres, aux workflows et aux planifications des autres automatisations MYTHOS.
