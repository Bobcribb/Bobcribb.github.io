# MYTHOS — Refonte : bibliothèques de civilisation illustrées et garde documentaire

**Contrôle : 4 novembre 2026, ~13 h 57 UTC.** Dépôt canonique `Bobcribb/Bobcribb.github.io`, branche `main`. Lecture préalable effective de `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, du registre d'attribution, de la file de soumissions, des blocages, des audits de récupération et du registre `scripts/editorial_media.json`.

## Contenus scientifiques — statut exact

**Nouvelle monographie universitaire intégrale soumise par cette intervention : aucune.** Les candidats déjà identifiés ne doivent pas être dupliqués :

- Au contrôle sur `main` après les trois changements, **199 fichiers JSON** dans `editorial/inbox/` et **194 UUID attribués** dans `editorial/numbering.json` (32 Origines du sacré, 44 Encyclopédie, 25 Comédies, 27 Tragédies, 66 Comparatif). Les **5 autres demandes** sont exactement les 5 UUID conservés dans `editorial/holds.json`.
- Blocages identifiés : `8fbc061a-...` (Apollophanès, *Krêtes*, seconde rédaction), `39c4d20b-...` (*Danaé*, seconde rédaction), `a72fc71d-...` (Sophocle, *Tyro reconnue*, seconde rédaction), `904ece0d-...` (collision de cote historique MC-042, étude autonome Nisaba/Nabû/Thot/Seshat), `3d64880f-...` (collision de cote historique MC-046, étude autonome des noms divins). Aucun texte de ces cinq dossiers n'a été effacé ni renuméroté.
- `editorial/archives/` conserve notamment la monographie intégrale de *Konnos*, sauvegardée hors numérotation pour éviter la duplication d'une œuvre déjà soumise ; les versions parallèles MC-033 et MC-040 sont archivées. Ni ces archives, ni les manuscrits déjà en file ne constituent une nouvelle soumission distincte à republier.
- Le mémoire intégral **L'Horizon d'Aton** est déjà dans `akhetaton-horizon-aton-etude/index.html` avec ses seize chapitres : pas de seconde transcription.
- Les anciens Chiron 118–133 et Nyx 218–224 restent sans manuscrit ancien intégral accessible vérifié selon `docs/REFONTE_AUDIT_2026-11-04.md`; les 15 fichiers Google Drive nommés « Brouillons sauvegardés » ne sont pas approuvés à publication. Aucune reconstitution ou publication de brouillon non autorisée.

Cette décision préserve le texte intégral des manuscrits en place et la garde transactionnelle : **aucune création directe dans `chapitres/`**, aucun changement de `editorial/numbering.json`, `editorial/holds.json` ou des planifications.

## Changements effectifs — accueil et graphisme

L'accueil proposait les trois bibliothèques Égypte, Mésopotamie et Perse comme simples liens textuels. Le constructeur `scripts/improve_reading.py` affiche maintenant **trois cartes documentaires**, sans retirer les accès « Toutes les civilisations » et « Sites et reconstitutions » :

1. **Égypte ancienne** — photographie de la chambre funéraire d'Ounas à Saqqarah, Vincent Brown, CC BY 2.0 ; renvoi à `textes-pyramides-ounas-egypte-ancien-empire/`.
2. **Mésopotamie** — tablette de l'`Enūma eliš` K.3473, Ninive, photographie Zunkir, CC BY-SA 4.0 ; renvoi à `enuma-elish-marduk-tiamat-creation-babylone/`.
3. **Perse/Iran ancien** — relief de la délégation lydienne à l'Apadana de Persépolis, photographie Phillip Maiwald, CC BY-SA 3.0 ; renvoi à `persepolis-apadana-reliefs-delegations-archives/`.

Les images sont locales, proviennent de `scripts/editorial_media.json`, avec leurs **descriptions et notices de crédits intégrales conservées** dans des panneaux accessibles. Les œuvres représentées sont des documents précis, non des images censées caractériser exhaustivement une civilisation. Le constructeur exige l'existence de chaque image, bibliothèque et page-source : si une ressource manque, la génération **échoue explicitement**, sans image de remplacement arbitraire.

Le style `assets/mythos-museum.css` ajoute une grille **3 colonnes / 2 colonnes / 1 colonne** suivant les écrans, avec images sans recadrage, noir/ivoire/or, états de focus clavier visibles, éléments dépliables et liens d'au moins 44 px. La bannière grecque statue à gauche et temple à droite n'est pas modifiée ; aucune ancienne illustration vectorielle 2,5D n'est réintroduite.

## Commits et contrôles

- `41d180a5f8bdba9acfaef911b3183803532c7d19` — cartes dans le générateur, avec crédits issus du registre.
- `56ca789605dbfb9a75d3514e0941dd0b94e2618c` — CSS noir/or et responsive.
- `88ab346768c39f012cf4c6a5e07ca03d26eac590` — trois tests de non-régression de provenance, liens et refus des sources absentes.

Les trois fichiers ont été **relus après écriture sur `main`** : `scripts/improve_reading.py` (blob `7daffbc7b6310a032cf6e50d00fda3478c10528d`), `assets/mythos-museum.css` (blob `11a9403bbffee38799ab431037d561e1e951c09e`), et `tests/test_civilisation_document_cards.py` (blob `4da800e8ef3f7056e2d0d5167b15443a372f3652`).

Au contrôle de 13 h 57 UTC, le workflow de validation du commit `88ab346` (`41842750044`) était **en cours** ; le workflow de publication du correctif CSS (`41842693827`) était **en attente**. La publication antérieure `41840963079` associée à `edc524e` était terminée avec succès, mais **ne démontre pas le déploiement de ces trois commits**. Le contrôle HTTPS direct de `bobmythos.fr` n'était pas accessible à ce client ; la présence publique des nouvelles cartes et du mémoire d'Aton n'est donc pas déclarée vérifiée. Le JSON `catalog/publication-verification.json` dans GitHub demeure une preuve de génération source, à confronter au fichier servi en HTTPS et au workflow Actions.

Contrôles de clôture : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, puis la dernière exécution de publication réussie, l'accueil HTTPS et son rendu mobile. Aucune autre automatisation MYTHOS n'a été modifiée.
