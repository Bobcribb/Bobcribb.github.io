# MYTHOS — Refonte des Origines du sacré : neuf tomes historiques rattachés

**Contrôle : 6 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`. Lecture effective préalable de `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md` et du générateur `scripts/build_navigation.py`. Aucune réaffectation de cote canonique.

## 1. Statut des contenus universitaires

**Premières publications universitaires imputables à cette intervention : aucune (0).** La recherche documentaire n'a identifié aucun manuscrit *nouveau, public, intégral et approuvé* absent du dépôt ou de la file. La Galigo est déjà publié intégralement. Les 135 anciens brouillons WordPress conservés dans Google Drive ont un statut de travail privé et un index imposant de ne pas les publier dans GitHub ; ils ne sont donc pas admissibles à un transfert automatique.

Photographie du circuit éditorial à ce contrôle : 482 fichiers JSON dans `editorial/inbox/`, 457 allocations reçues dans `editorial/numbering.json`, 23 retenues explicites dans `editorial/holds.json` et 2 autres demandes sans reçu (un ancien nom non UUID `20261105-mc-069-souffle-vent-vie-philologie` et une soumission nouvelle `92b006f2-e5c3-49da-82ac-202611060352`). Les deux dernières relèvent du workflow / de la réconciliation de la file, et ne sont pas redéposées. Ces effectifs évoluent avec les autres séances horaires et ne sont pas des promesses d'attribution.

## 2. Lacune d'accès réellement contrôlée

Le portail canonique `origines-du-sacre/index.html` ne présentait pas les liens vers neuf manuscrits historiques intégraux, pourtant présents dans `corpus/origines-du-sacre/` et cités par `corpus/sommaire-general.md` et par le portail historique `origines-du-sacre.html`. Les neuf couples source Markdown / lecteur HTML ont été relus pour leur présence, leur longueur, leurs cotes, leurs références et leur structure de lecture, avant intervention :

| Cote historique | Tome | Chapitres du manuscrit historique | Titre documentaire | Markdown (caractères) | HTML (caractères) |
| --- | --- | --- | --- | ---: | ---: |
| ODS-CONV-XXV | XXV | 339–346 | Sanctuaires et espaces sacrés | 47 280 | 58 353 |
| ODS-CONV-XXVI | XXVI | 347–354 | Les eaux sacrées | 35 509 | 46 691 |
| ODS-CONV-XXVII | XXVII | 355–362 | Le feu sacré | 51 508 | 60 235 |
| ODS-S28 | XXVIII | 363–370 | Montagnes, grottes et profondeurs | 54 221 | 74 761 |
| ODS-CONV-XXIX | XXIX | 371–378 | Arbres sacrés | 41 064 | 49 925 |
| ODS-CONV-XXX | XXX | 379–386 | Pierres sacrées et bétyles | 56 903 | 74 224 |
| ODS-CONV-XXXI | XXXI | 387–394 | Images divines | 64 741 | 74 097 |
| ODS-CONV-XXXII | XXXII | 395–402 | Corps, possession et masques | 60 944 | 73 466 |
| ODS-CONV-XXXIII | XXXIII | 403–410 | Voix, hymnes et musique sacrée | 54 867 | 67 373 |

Ces sources sont **déjà hébergées publiquement dans le dépôt**, pas des manuscrits inédits. Les cotes historiques ODS-CONV et ODS-S28 sont distinctes des numéros canoniques de la collection. Le tome XXVIII indique toujours une révision scientifique à poursuivre.

## 3. Modifications effectives de `main`

- `scripts/origins_archive_navigation.py` : inventaire explicite des neuf couples Markdown/HTML ; contrôle de la présence du texte long et de son appareil documentaire ; génération d'un sommaire de neuf cartes directes et de neuf retours réciproques sur les lecteurs **rendus dans `_site` uniquement**, sans modifier l'article scientifique ni les fichiers d'archives.
- `scripts/build_navigation.py` : insertion permanente du sommaire `#origines-archives-documentaires` dans la reconstruction du portail `/origines-du-sacre/`, juste après les 27 tomes.
- `assets/mythos-museum.css` : cartes anthracite, ivoire et or, grille 3/2/1 colonnes, focus clavier, retour accessible, petits écrans et préférence de mouvement réduit. La bannière statue grecque à gauche / temple à droite est conservée.
- `tests/test_origins_archival_shelf_20261106.py` : garde sur les neuf sources, les liens sans doublons, la conservation du texte de `main` dans deux reconstructions, l'idempotence des retours et le refus d'une archive absente.

**Commits GitHub confirmés** : `5d8d6d5f1547a0db16f0c7a9f722ca57ec2f00a6`, `94c2901be1634941d29819aff9ce55eac9cb81d2`, `ce81aee5c701146350f60ef5c54740e6eddcc8bf`, `28ccfbcf24d3725d962c3072ca3a6b7ede1f482c`.

## 4. Tests et déploiement : ne pas confondre GitHub et HTTPS

Après ces commits, GitHub Actions a enregistré des exécutions de validation et de publication ; plusieurs étaient encore **en cours / en attente** au dernier contrôle, et la publication associée à `28ccfbc` (`42153974918`) a été **annulée par une nouvelle publication concurrente**, sans constituer une preuve d'échec du code. La dernière publication précédemment confirmée en HTTPS renvoyait `source_commit=8bb55618a72a46f99ddd180192ff586dc2fe1d31`, exécution `42064120533`, 1 583 documents, 27 archives et 110 médias ; le nouveau sommaire de neuf tomes n'était pas encore servi. La vérification finale doit comparer une exécution GitHub Actions **réussie, postérieure aux quatre commits**, le `source_commit` du manifeste public et la présence des neuf liens dans `https://bobmythos.fr/origines-du-sacre/#origines-archives-documentaires`.

Aucun texte, PDF, numéro, reçu, contenu de `editorial/inbox/`, archive d'origine, workflow, domaine ou planification horaire MYTHOS n'a été modifié.
