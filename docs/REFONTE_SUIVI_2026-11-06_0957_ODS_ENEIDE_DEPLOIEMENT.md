# MYTHOS — Refonte : continuité des archives ODS et déblocage du déploiement de l’Énéide

**Contrôle du 6 novembre 2026 — dépôt** `Bobcribb/Bobcribb.github.io`, branche `main`. Cette note sépare le code enregistré de l’état réellement visible sur `https://bobmythos.fr`.

## 1. Précontrôle éditorial, contenu intégral et garde de numérotation

Les règles actuelles de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été lues sur `main` avant toute écriture. Sont également contrôlés `EDITORIAL_CONTINUITY.md`, `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md`, les répertoires historiques des *Origines du sacré*, le corpus de comédies, les sources philosophiques de l’Énéide, le registre des attributions et `editorial/holds.json`.

**Nouvelle étude universitaire indépendante, approuvée, absente de la publication et introduite dans cette séance : zéro.** Les neuf tomes historiques XXV–XXXIII possèdent déjà chacun un manuscrit Markdown complet et un lecteur HTML ; il serait trompeur de les compter comme neuf nouvelles études. Les dix-huit manuscrits de l’Énéide sont déjà sources du dossier de philosophie et ont reçu des lecteurs HTML dans le générateur, sans constituer dix-huit études inédites. Le texte sur Mithra, Varuṇa et `ṛta` est présent sous deux adresses historiques mais porte le même blob Git `70d6aef3fcdecb993f6c2d3bbd7d52969821d9a3` : une nouvelle soumission serait un doublon.

Lors du contrôle, `editorial/holds.json` contenait **26 demandes retenues** ; notamment, « Les mains du divin » demeurait en retenue à la suite de la collision historique MC-096 avec « Les ombres du divin ». Les demandes de la file ne sont pas de nouvelles études libres à redéposer, et les archives privées WordPress/Drive ne sont pas présumées approuvées. **Aucun nouveau UUID, numéro, reçu ni fichier de chapitre canonique n’a été fabriqué, ni le registre de numérotation modifié.**

## 2. Liens réciproques et graphisme

Le générateur `scripts/origins_archive_navigation.py` conserve les neuf liens de retour au sommaire et vers les Markdown sources, et ajoute, en respectant les cotes historiques, des liens **tome précédent / tome suivant** dans chaque lecteur, sans en ajouter après XXXIII ni avant XXV. Le test `tests/test_origins_archival_shelf_20261106.py` couvre ces bornes, les URL exactes et la réapplication idempotente sans modification de la prose. `assets/mythos-museum.css` met les liens tactiles en noir, or et ivoire, avec navigation en colonne sous 540 pixels, focus visible et textes longs qui reviennent à la ligne. La bannière photographique existante statue grecque à gauche, temple à droite est conservée.

## 3. Anomalie réelle qui empêchait la publication du contenu universitaire

Les journaux GitHub Actions de publication **42188396415** (job `127796792982`) et **42187493532** (job `127791191952`) terminés en échec exposent la même erreur, dans `scripts/verify_museum_design.py` : absence de `data-mythos-design="20261104"` sur `_site/corpus/philosophie/eneide/13-pietas-destin.html`. La vérification du générateur avait parfois réussi, mais celle de la publication refusait les pages dépourvues de la navigation muséale commune.

Cause déterminée dans `scripts/build_native.py` : les **18 lecteurs HTML intégraux de l’Énéide** étaient créés par `install_eneide_source_access(ROOT, OUT)` **après** `apply_museum_design(OUT)`, et également après le dernier indexage. La réconciliation n’exige ni réécriture ni nouveau numéro scientifique. La génération des lecteurs est désormais appelée **avant** la passe muséale ; un nouvel `reindex(chapters)` après leur création les ajoute au moteur de recherche, au catalogue et au sitemap avant le rendu esthétique. Les sources Markdown originales continuent d’être copiées à l’identique par le module existant. Aucun brouillon privé n’est importé.

Un test ajouté dans `tests/test_eneide_source_access_20261106.py` vérifie sur dix-huit lecteurs de démonstration la présence du bandeau muséal, de la navigation grecque, de la feuille de style, des titres, du texte scientifique et de la bibliographie, ainsi que l’ordre de compilation qui évite la régression.

## 4. Commits de cette séance

| Commit Git | Modification |
| --- | --- |
| `ff29d868101e8bd4a669cfdc51c6cf7d530df03c` | Parcours précédent/suivant entre les neuf tomes historiques ODS. |
| `a5e5528b826796aec9ea068513542aa8bf407a78` | Tests des liens réciproques et de l’absence de troncature. |
| `df6b0f85d065bd39b1a88bee88397a0e65550400` | Responsive et accessibilité du parcours ODS noir et or. |
| `c05fecb9ba9f39262e5bc8aa0e4290dd8853114a` | Déplacer les lecteurs Énéide avant leur habillage muséal. |
| `57914088bba3dfe37c6a2d7f04ab99cd1d30cbf8` | Tests du rendu commun des dix-huit lecteurs intégraux. |
| `4c3b99d3cbf991258017302c16d69c87139a839d` | Réindexation de la recherche et du sitemap après la génération des lecteurs. |

## 5. Séparation des vérifications GitHub et du site public

À la lecture publique de `https://bobmythos.fr/catalog/publication-verification.json`, le manifeste annonçait encore `source_commit=db016f6cbc0bec783e369a1e2874f0c6a1883aa6`, exécution `42175517252`, **1 604 documents indexés, 27 archives et 110 médias** : une version antérieure. Le portail des Origines du sacré affichait déjà les neuf archives dans son sommaire, mais **cela ne prouve pas les nouveaux liens entre tomes**.

Les workflows de validation et publication déclenchés par les commits de la séance sont des demandes de contrôles GitHub ; leurs conclusions n’étaient **pas encore constatées comme succès** lors de la première vérification. Le seul enregistrement des commits ne prouve pas le déploiement. Pour le confirmer, obtenir un workflow `publish.yml` **success** sur un commit descendant des changements, puis vérifier que le manifeste HTTPS porte une nouvelle empreinte `source_commit`, que les 18 lecteurs Énéide disposent de leur bandeau commun et sont indexés, et que les neuf lecteurs ODS proposent les deux navigations limites correctement. Tout échec ultérieur doit être diagnostiqué sur son journal exact, pas masqué.

**Conservation garantie dans le périmètre de ces commits :** aucun manuscrit scientifique, source primaire, bibliographie, cote, reçu, registre, archive, reconstitution photoréaliste ou planification MYTHOS n’a été modifié. Aucune représentation 2,5D n’a été réintroduite.
