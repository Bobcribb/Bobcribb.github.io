# MYTHOS — Refonte éditoriale du 4 novembre 2026 : huit monographies reclassées

**Périmètre :** dépôt de publication `Bobcribb/Bobcribb.github.io`, branche `main`. Contrôle initial de la branche : `d1277c4c978843f397ceddacd0bfacb512243f8d`. Fichiers `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` lus avant la modification.

## 1. Recherche réelle de contenus intégraux absents

L'inventaire public du dépôt actif contenait **3 149 fichiers suivis** au contrôle, dont les manuscrits `chapitres/encyclopedie/`. La file concurrente contenait **276 demandes JSON** : **271 déjà attribuées**, **5 bloquées et documentées** dans `editorial/holds.json`, **aucune nouvelle soumission non attribuée** au contrôle. Aucun numéro ni registre n'est modifié.

Comparaison ciblée avec l'ancien dépôt public `Bobcribb/Mythos` (205 fichiers, dont 74 chemins de travail sous `corpus/` ou `contenus/` hors README) : les anciennes études et les compilations documentaires existent sous leurs chemins correspondants dans le dépôt actif. Seule une notice JSON d'image de Delphes (`corpus/reconstitutions-3d/delphes-apollon-panorama-notice.json`) manque au contrôle par chemin ; elle n'est **pas** une monographie intégrale et ses données ne justifient ni une étude numérotée ni un doublon.

Les brouillons WordPress issus des sauvegardes Google Drive ne sont **pas des manuscrits approuvés pour publication** et ne sont pas versés dans le dépôt public. Aucune publication de texte inédit non vérifié n'est revendiquée.

**Contenu universitaire intégral nouveau effectivement déposé cette séance : aucun.** Le blocage éditorial est explicite : parmi les sources publiques vérifiées, les manuscrits complets susceptibles d'être utilisés sont déjà attribués et accessibles ; les autres sont des brouillons non approuvés. Il est interdit de remplacer ce manque par un texte reconstruit ou abrégé.

## 2. Huit contenus existants rétablis dans un dossier thématique exact

Le dossier public `/mythologie-grecque/dossiers/sources-anciennes/` comportait **16 études** dans « Nouvelles études à classer » ; les sept monographies suivantes y étaient indûment reléguées, alors qu'elles possèdent déjà cote, texte intégral, sources et bibliographie. La huitième, sur Poséidon, était classée parmi les divinités mais sans sous-dossier spécifique.

| Chapitre canonique | Monographie contrôlée sur `main` | Classement universitaire corrigé |
|---|---|---|
| 401 | Tritopatores, Athènes et Sélinonte | Cultes et sanctuaires / Ancêtres, naissance et rites de purification |
| 402 | Sôsipolis, Élide, Olympie et Magnésie | Cultes et sanctuaires / Olympie, Élide et dieux protecteurs des cités |
| 403 | Ennodia et les sanctuaires thessaliens | Cultes et sanctuaires / Thessalie — déesses des routes et des seuils |
| 405 | Achélôos, dieu-fleuve | Divinités / Dieux-fleuves, paysages et eaux divinisées |
| 406 | Poséidon et les hippocampes | Divinités / Poséidon et le cortège marin |
| 412 | Aristéas de Proconnèse et les Arimaspes | Sources anciennes / Poètes, voyages et traditions fragmentaires |
| 421 | Praxidikai, serments et sanctuaire d'Haliarte | Cultes et sanctuaires / Haliarte — serments, justice et sanction sacrée |
| 422 | Salmakis, Halicarnasse, SEG 48.1330 | Cultes et sanctuaires / Halicarnasse — fontaines, inscriptions et métamorphoses |

Les manuscrits Markdown individuels ont été lus pour vérifier leur sujet, leur étendue (de plus de 9 000 à plus de 45 000 caractères selon l'étude), les sections, la documentation primaire et les bibliographies. Leur **cote canonique est conservée**. Ces huit études n'ont **pas** été recopiées, tronquées ni réécrites.

Le correctif est porté exclusivement dans `scripts/build_greek_folders.py`, par huit règles fondées sur le sujet présent en tête du slug. Une passe de génération reconstruit les rubriques et sommaires, affecte un seul foyer thématique à chaque étude, ajoute le lien inverse vers son sous-dossier précis et maintient les adresses documentaires directes. Les archives et la page source de chaque étude sont conservées. **À distinguer : le classement est corrigé dans le générateur, mais le HTML du domaine public ne l'affiche qu'après génération et déploiement réussis.**

## 3. Graphisme responsive et accessibilité

La présentation muséale approuvée (noir, ivoire et or, bannière grecque avec statue à gauche et temple à droite) est préservée. Les liens des monographies dans les sommaires de dossiers sont rendus plus faciles à toucher sur téléphone (`min-height:44px`), avec meilleure largeur de texte, alignement et indication au survol. La grille passe toujours à une colonne sous 700 pixels, et les états `focus-visible` sont maintenus.

## 4. Commits de la séance

- `5bb6d631eba304b37db0dde61e45b1a36426e6dd` — nouveaux rattachements des huit études.
- `8af3b6e721fce1c2651cd971ab379fe2c57ada90` — correction des bornes d'expressions régulières des huit règles.
- `f973acebc2cb86609cc302168a77448576ca6519` — test régressif vérifiant huit sources intégrales, leur bibliographie, leur rubrique et leur sous-dossier.
- `a5d68617f2f4fba4ef9406c1514941078dd906dc` — adaptation tactile des liens des monographies.
- `99c976c528db7344a49d41a1d34ee92ef5360175` — test du style tactile et responsive.

## 5. Contrôle du site et limites de publication

Au début du contrôle public HTTPS, `https://bobmythos.fr/mythologie-grecque/dossiers/sources-anciennes/` affichait encore « Nouvelles études à classer (16) », comprenant les chapitres 421 et 422 ; `https://bobmythos.fr/mythologie-grecque/dossiers/cultes-sanctuaires/` ne présentait pas encore ces deux derniers textes. C'est la **version antérieure**, pas la version modifiée.

Les workflows de génération et de publication déclenchés par les commits étaient encore en cours ou en attente au dernier contrôle initial : leurs conclusions ne doivent pas être anticipées. La vérification finale devra contrôler `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, le reçu public `/catalog/publication-verification.json`, la disparition des chapitres 421/422 du sous-dossier générique, leur apparition dans la famille cultuelle, leurs liens réciproques et la présence des textes intégraux.

**Garanties :** aucune modification des manuscrits `chapitres/`, des documents de bibliothèque, du registre d'attribution, des demandes `editorial/inbox/`, des cinq blocages `editorial/holds.json`, des archives, des images archéologiques, des reconstitutions ou des autres automatisations MYTHOS ; aucun changement d'horaire.
