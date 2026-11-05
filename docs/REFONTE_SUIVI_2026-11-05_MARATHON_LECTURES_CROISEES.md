# MYTHOS — Refonte du 5 novembre 2026 : parcours intégral de Marathon

**Dépôt officiel :** `Bobcribb/Bobcribb.github.io`, branche `main`.  
**Règles de publication :** `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`, relues avant toute modification.  
**Politique :** ne pas attribuer directement de cote, ne pas dédoubler de demandes, ne pas toucher aux manuscrits scientifiques ni aux autres automatisations.

## 1. Recherche de contenus intégrals non publiés — résultat

Une inspection préalable a porté sur l'arbre GitHub principal (3 208 fichiers), le dépôt historique `Bobcribb/Mythos` (206 fichiers), les sources universitaires nommées dans les manuscrits, la file `editorial/inbox/` et les reçus du registre `editorial/numbering.json`.

Dans le dépôt historique, **37 fichiers Markdown** ont été recensés ; **36** sont présents sous le même chemin dans le dépôt actif. L'unique fichier absent est `docs/etat-publication-images-3d.md` (5 325 octets), une **ancienne note opérationnelle**, non un chapitre universitaire inédit. Sa conservation dans l'ancien dépôt n'est pas remise en cause et son contenu daté ne doit pas réintroduire les anciennes représentations 2,5D.

**Photographie de la file à cette exécution : 295 demandes, dont 289 attribuées, 5 en attente pour conflits déclarés et 1 demande publique intégrale encore non attribuée.** Cette dernière est `editorial/inbox/6a91c061-6b22-4c19-ae61-202611050061.json`, collection `comparatif`, manuscrit `MC-061` *Quand les dieux ne savent pas*, 79 617 caractères, déjà déposé avec les variables `{{volume}}` et `{{numero}}`. **Aucune seconde demande ni numéro provisoire n'a été créé : seule la transaction GitHub Actions peut lui attribuer son volume.** La présence de cette demande ne constitue pas encore une publication.

Dans les sources accessibles inspectées, aucun autre texte universitaire complet, approuvé, inédit et non encore inscrit dans le circuit de publication n'a été retrouvé. **Nouveaux manuscrits intégrals publiés par cette intervention : zéro.** Aucun texte privé, incomplet ou dupliqué n'a été importé.

## 2. Corpus intégraux vérifiés et nouvel itinéraire de lecture

Quatre manuscrits existants, numérotés et présents en Markdown et HTML sur `main`, ont été contrôlés en parallèle :

1. **Chapitre 425 — Échétlos / Échétlaios**, environ 41 736 caractères, 45 sections, Pausanias, Stoa Poikilè, paysage de Marathon, comparaisons philosophiques, bibliographies primaires et critiques.
2. **Chapitre 326 — Hécalé et le taureau de Marathon**, environ 23 893 caractères, Thésée, Callimaque, hospitalité et mémoire cultuelle attique, sources et bibliographie.
3. **Chapitre 371 — Pan**, environ 5 635 caractères, sept développements et « Sources et pistes de lecture », dont le coureur athénien et le souvenir de Marathon.
4. **Chapitre 393 — Eukleia**, environ 41 745 caractères, Artémis Eukleia, renommée civique et mémoire de Marathon, avec bibliographie et examen des témoignages.

**Leurs quatre textes sont déjà publiés et accessibles : il ne s'agit donc pas de quatre nouvelles intégrations.** Le parcours créé est un index transversal vers **ces textes intégrals**, sans en réécrire le contenu ni les citations.

## 3. Correction de classement, liens réciproques et ergonomie

Dans `scripts/build_greek_folders.py`, le chapitre **425** rejoint le dossier primaire **« Héros et héroïnes »**, sous l'intitulé « Marathon — Échétlos, araire et mémoire civique ». Le chapitre **326**, auparavant susceptible de rester dans la rubrique générique des sources, est classé lui aussi avec les héros sous « Hécalé — Thésée, hospitalité et mémoire attique ». Les chapitres **371** (divinités) et **393** (cultes et sanctuaires) conservent leurs rubriques primaires respectives.

Le constructeur ajoute, **en dehors de l'article universitaire**, un panneau « Marathon : lectures croisées » à chacune de ces quatre pages lorsqu'elles sont présentes dans l'inventaire. Chaque panneau relie directement les **trois autres** monographies. Chaque auteur, volume, bibliothèque, source et paragraphe demeure à son emplacement ; ces renvois n'interviennent pas dans le comptage de l'affectation primaire. La procédure supprime ses anciens panneaux puis les recrée pour éviter tout doublon lors des reconstructions répétées.

Le nouveau panneau s'accorde avec la charte **anthracite/noir, ivoire et or** ; sa grille passe à **une colonne sous 700 px**, les liens possèdent une cible tactile d'au moins **44 px** et une mise au point clavier explicite. La bannière statue grecque/temple, les visuels photoréalistes, les légendes et les sources archéologiques sont conservés. Aucun fichier 2,5D n'est réintroduit.

## 4. Commits et tests

- `c0350f3c95fffb351a2c4ba8a9c97fd6decd1c8a` — création de l'itinéraire Marathon et premier classement.
- `b416cc063c64326c2f2040224f2ede224be40fdd` — grille noir et or, accessibilité et adaptation mobile.
- `ccde88f084957c26f1a41f58262cf31b0a3ecff0` — tests des quatre sources, des liens directs et de l'idempotence.
- `6f86fed7e08ecfc5dc0403740434199219ff7bc2` — correction de la borne regex et classement historique d'Hécalé.
- `6f0e22c02731a7a408cc281d0fea5be04190f633` — correction du chemin des sources dans le test.

Tests ajoutés dans `tests/test_greek_marathon_reciprocal_links.py` : existence des sources et des pages, présence des cotes/bibliographies, reçu canonique du chapitre 425, classement thématique, liens bidirectionnels et non dupliqués, reconstruction deux fois, absence de modification de l'élément `<article>`, navigation vers les dossiers et compatibilité smartphone/clavier. La vérification du générateur exige également trois retours exacts par monographie lorsque quatre sont présentes.

Une exécution intermédiaire `41945771455` a détecté une erreur dans le nouveau test (chemin `chapitres/encyclopedie.md`) ainsi qu'une règle regex trop échappée ; ces deux défauts **ont été corrigés**. Le workflow de validation post-correctif est `41945861353` : la suite a franchi l'étape des tests unitaires et était en génération lors de ce suivi. Ne pas déclarer une validation globale terminée avant sa conclusion.

## 5. Contrôle effectif du domaine

Contrôle indépendant de `https://bobmythos.fr/catalog/publication-verification.json` : `source_commit=882aa377c57abd5431c0429444267541cbe7acc0`, GitHub Actions `41944121110`, **1 413 documents indexés, 27 archives et 110 médias**. Le chapitre public 425 et le dossier « Héros » sont accessibles, mais ne comportaient **pas encore** le nouveau panneau et les liens au moment de la requête. Le reçu cité précède les commits ci-dessus ; **la mise en ligne des renvois réciproques n'est pas encore confirmée**.

Contrôle final à effectuer une fois le workflow terminé : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, concordance de la nouvelle empreinte publique et présence de `aside[data-greek-cross-readings="marathon"]` sur les quatre URLs HTTPS.

**Invariants inchangés :** manuscrits universitaires, sources, archives, registres `editorial/numbering.json`, file `editorial/inbox/`, cinq collections éditoriales, suppression de l'entrée en doublon « Grande encyclopédie », et planifications des autres automatisations MYTHOS.
