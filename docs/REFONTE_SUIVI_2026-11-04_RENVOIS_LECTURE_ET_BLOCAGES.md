# MYTHOS — Refonte : renvois documentaires et examen des manuscrits non publiés

**Date : 4 novembre 2026.** Dépôt public : `Bobcribb/Bobcribb.github.io`, branche `main`.
État initial contrôlé : `613b126a534b6f9f68e1828a77e9ce39310fd2af`.
Les règles de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été lues sur la branche réelle **avant toute modification**.

## 1. Recherche de contenu intégral

L'inventaire effectué après la modification des fichiers techniques comporte **220 soumissions** dans `editorial/inbox/`, **209 reçus d'attribution** dans `editorial/numbering.json`, **5 demandes retenues** dans `editorial/holds.json` et **6 nouvelles soumissions déjà présentes mais non encore attribuées**, au point de contrôle :

| UUID (suffixe) | Collection | Sujet | Longueur Markdown |
|---|---|---|---:|
| `6f5e8c23…` | encyclopedie | Zeus Meilichios | 47 069 caractères |
| `a6c2d570…` | encyclopedie | Achélôos | 10 851 |
| `b33a44d1…` | encyclopedie | Poséidon et les hippocampes | 20 782 |
| `c3fb9c0e…` | comparatif | MC-049, Faire vivre l'image divine | 72 219 |
| `d4b8b764…` | encyclopedie | Asôpos | 10 954 |
| `e6b45c91…` | encyclopedie | Agathos Daimôn | 10 621 |

Ces six objets ont été relus à leur chemin UUID : ils possèdent un titre, une variable de cote provisoire et des références ou une bibliographie. **Ils ne sont pas attribués par cette intervention**. Les renuméroter ou les soumettre une seconde fois créerait un conflit avec la file transactionnelle.

Les archives Google Drive « MYTHOS — Brouillons sauvegardés » comprennent 135 textes expressément conservés en privé. L'index de sauvegarde stipule « Ne pas publier ces documents sur GitHub ». Les documents ne sont donc pas copiés dans le dépôt public. La restauration complète de *La Galigo* est déjà versionnée au chemin `bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/index.html` : cette étude n'a pas été dupliquée.

**Nouvelle étude intégrale déposée lors de cette exécution : aucune.** Le blocage est éditorial et transactionnel : les seuls manuscrits intégraux nouveaux identifiés sont déjà dans `editorial/inbox/`, et les autres copies sont des archives privées. Aucun texte n'est fabriqué, tronqué ou remplacé par un résumé.

## 2. Modifications effectives du site généré

1. `scripts/recent_studies.py` : chaque carte universitaire illustrée dispose d'une description explicite de sa photographie et d'une précision indiquant qu'il s'agit d'un document de collection, non nécessairement d'une image de l'étude mise en avant. Évite les associations iconographiques scientifiquement trompeuses.
2. Le même module ajoute aux lecteurs HTML des cinq dernières études sélectionnées une **navigation réciproque** : retour vers « Dernières études universitaires » sur l'accueil et accès à la rubrique correspondante. L'insertion est idempotente et porte l'attribut `data-reading-owned` pour rester distincte du contenu universitaire.
3. `assets/mythos-museum.css` : présentation noire et or des légendes et renvois, zones tactiles d'au moins 44 px, adaptation aux écrans étroits, masquage des éléments de navigation à l'impression.
4. `tests/test_recent_studies.py` : assertions de non-duplication, de présence des légendes, d'exactitude des liens, de conservation des textes et de stabilité entre deux constructions.

Les manuscrits Markdown, les 27 archives, les médias d'origine et les bibliographies ne sont pas modifiés. La bannière grecque et la navigation principale restent en place ; aucune image 2,5D n'est réintroduite.

## 3. Commits

- `dcfb80b82933c109f53d900b1354d3087e945dbd` — cartes contextualisées et renvois réciproques.
- `333dd790a9fe4f6ced8a5967503fd1cf3ae4180d` — tests de conservation et de navigation.
- `b2185328bb9f36374f4d3b2a9026a6e94cdb1560` — styles responsive noir et or.

## 4. Vérification et statut

Le connecteur GitHub confirme la présence des trois modifications sur `main`. Les workflows de validation et de publication associés sont **en file d'attente** lors de la vérification : notamment le workflow de publication `41865569443` et l'audit `41865569494`.

Les tests automatisés et la validation complète du générateur **ne peuvent pas encore être déclarés réussis**. Une première lecture HTTP a échoué, puis une seconde vérification indépendante HTTPS a réussi. Le document public `https://bobmythos.fr/catalog/publication-verification.json` annonce **`source_commit=05c68a64605501f7dc90889fbd74961c4350528c`**, **1 333 entrées indexées, 27 archives et 110 médias vérifiés** ; l'accueil public correspondant ne contient pas encore la section « Dernières études par collection ». Les nouvelles modifications **ne sont donc pas encore déployées**. Contrôles à mener dès qu'une exécution de publication est terminée : réussite de `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, présence de `#home-etudes-recentes` sur l'accueil, présence du renvoi au bas du lecteur HTML correspondant à chaque collection et actualité de `/catalog/publication-verification.json`.

Aucune modification apportée à `editorial/numbering.json`, `editorial/holds.json`, `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, `.github/workflows/` ni aux automatisations horaires MYTHOS.
