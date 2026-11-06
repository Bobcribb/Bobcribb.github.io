# MYTHOS — Refonte du théâtre : éditions universitaires intégrales et navigation réciproque

**Contrôle du 6 novembre 2026.** Dépôt public `Bobcribb/Bobcribb.github.io`, branche `main`; site cible `https://bobmythos.fr`.

## 1. Vérifications éditoriales et statut des manuscrits

Préalables effectivement relus : `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, `EDITORIAL_CONTINUITY.md` et `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md`. La publication des cinq collections numérotées exige la file `editorial/inbox/<uuid>.json` ; aucune attribution directe dans `chapitres/` n'est autorisée.

**Nouvelles études universitaires intégrales publiées pour la première fois par cette séance : 0.** Les manuscrits complets vérifiés ici sont **déjà présents dans le dépôt** : les importer de nouveau créerait des doublons. Les 135 anciens brouillons WordPress ont explicitement un statut privé dans le protocole et ne peuvent pas être considérés comme approuvés pour diffusion. Aucune nouvelle source publique, absente du dépôt, complète et approuvée n'a été certifiée à cette séance. Les demandes déjà déposées dans `editorial/inbox/` ne sont pas dupliquées ni renumérotées.

**Neuf archives critiques existantes**, vérifiées en couples manuscrit Markdown / lecteur critique HTML / scènes contemporaines HTML dans `corpus/theatre-grec/comedies/` : `polyidos`, `daidalos`, `kokalos`, `aiolosikon`, `holkades`, `lemniai`, `geras`, `ploutos-protos`, `triphales`. Il s'agit de **dix-huit lecteurs HTML**, de leurs **neuf sources intégrales** conservées et de leur appareil bibliographique. Les titres/volumes historiques sont repris depuis les sources ; aucun nouveau numéro canonique n'est inventé.

## 2. Modifications effectivement enregistrées sur main

- `scripts/theatre_fragment_index.py` : le sommaire des neuf éditions affiche désormais pour chaque dossier l'accès direct à son manuscrit d'origine en plus des deux parcours déjà distincts (étude critique et scènes modernes).
- Le générateur ajoute à chacun des dix-huit lecteurs **un retour direct vers son dossier du portail Théâtre**, un lien vers l'autre lecteur et un accès à la source Markdown. Il refuse un lecteur d'édition complète sans structure HTML nécessaire ; les sous-séries de tests historiques conservent leur comportement.
- La navigation est ajoutée au **rendu `_site` seulement**, sans correction, coupe ni copie des manuscrits universitaires originaux. Le texte à l'intérieur de l'article critique ou des scènes demeure inchangé.
- Une illustration contextuelle distincte des photographies déjà présentes sur le portail, et non une restitution d'Aristophane, est ajoutée au sommaire : **quinze figurines grecques en terre cuite d'acteurs comiques, fin du Ve–début du IVe siècle av. n. è.**, Metropolitan Museum of Art **13.225.13–.14, .16–.28**, notice `https://www.metmuseum.org/art/collection/search/844483`, image CC0. Elle documente les types comiques sans identifier une pièce perdue.
- `assets/mythos-theatre-archive.css` : présentation anthracite, ivoire et or, navigation tactile d'au moins 44 px, focus clavier et grille adaptée aux petits écrans. La bannière existante statue à gauche / temple à droite n'est pas modifiée.
- `tests/test_theatre_archives_navigation_20261106.py` : gardes sur neuf sources, dix-huit lecteurs, liens réciproques, préservation du texte, idempotence, image contextuelle et style mobile.

## 3. Commits enregistrés

- `d8b6c31aafd8fdca6e87d5dfc413f1a13f438ad1` — premières liaisons réciproques ;
- `d721d06e87987eb3c11cc5275f9b6388a222d364` — feuille de style mobile ;
- `2e843ee299ef26434a22391b41954e2a171c691c` — tests de conservation ;
- `6d31f4c7772598b22c54bfd5797e53d299b1dc5d` — compatibilité des lecteurs Lemniai sans balise `main` ;
- `9361d72bbfd6471a7538ca964d729bcaabe89a89` — crédit muséal documenté ;
- `d21525f548ab168b21475ebde90f06d84f7070b2` — compatibilité avec les tests de sous-séries ;
- `ad778408ca6467a2f8061d9dd8cd03eda38bdbfe` — distinction CSS manuscrit / lecteurs ;
- `840d8476a2ec27317e0c78ac6afbc27f8db23272` — adaptation des tests.

## 4. Contrôle de CI et déploiement : à distinguer

Une première exécution de validation, **42160743143**, a échoué sur le **test historique de sous-série** `test_theatre_fragment_index` après l'introduction des nouveaux retours ; le problème était dû à des fixtures HTML délibérément minimales (sans entête de site) et non à une perte des sources. Le correctif `d21525f` évite de modifier ces fixtures et laisse la vérification stricte active pour les neuf éditions réelles. Une nouvelle exécution `42160962193`, sur le commit `840d8476a`, était encore **en cours** au dernier contrôle de ce rapport. Le résultat final devra être relu avant de déclarer le nouveau comportement validé par CI.

La dernière publication issue des présents commits **n'est pas confirmée en HTTPS** à l'heure de la rédaction. La vérification finale doit confronter la publication GitHub Actions, le `source_commit` du manifeste `/catalog/publication-verification.json`, les neuf cartes du portail `/theatre/#theatre-comedies-editions`, les dix-huit retours et les liens sources, puis contrôler 360–390 px et l'accessibilité clavier. Une écriture GitHub n'est pas une preuve de déploiement.

**Préservation :** aucun manuscrit source, archive, numéro canonique, reçu d'attribution, workflow, image 2,5D, domaine ni programmation horaire MYTHOS n'a été modifié.

- `da2a1e7167815b443b9203906990866961898138` — choix d'une illustration archéologique non dupliquée dans le portail.
