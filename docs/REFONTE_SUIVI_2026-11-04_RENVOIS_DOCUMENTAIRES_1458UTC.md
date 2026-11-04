# MYTHOS — Refonte : trois renvois scientifiques bidirectionnels

**Contrôle : 4 novembre 2026, vers 14 h 58 UTC.** Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`. Instructions `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relues avant toute opération. Ce rapport décrit séparément les sources examinées, les changements enregistrés et la livraison publique.

## Recherche des contenus universitaires intégrals non encore publiés

- Lecture effective de `editorial/numbering.json`, `editorial/holds.json`, des inventaires du dépôt et des audits de récupération. À la photographie contrôlée : **205 fichiers de demandes dans `editorial/inbox/`**, **200 allocations avec reçu au registre** (34 Origines du sacré, 45 Encyclopédie, 26 Comédies, 28 Tragédies, 67 Comparatif), et **5 demandes retenues** dans `editorial/holds.json`. Ces cinq retenues sont des conflits de double rédaction ou de cote historique MC-042/MC-046 ; aucun manuscrit n'a été supprimé.
- `editorial/archives/` conserve la rédaction supplémentaire de *Konnos* et deux variantes des dossiers MC-033 et MC-040 ; ces sources sont archivées précisément pour ne pas créer une deuxième étude de même identité.
- Recherche dans le Google Drive connecté : les fichiers MYTHOS apparus sous « Brouillons sauvegardés » sont toujours qualifiés de brouillons privés ; les exemplaires de *L'Horizon d'Aton* existent mais leur étude intégrale est **déjà publiée**. Aucun nouveau texte intégral approuvé et absent du site n'a été identifié dans ces résultats.
- Les études historiques annoncées pour Chiron 118–133 et la série Nyx 218–224 demeurent sans source universitaire complète vérifiée, conformément à `docs/REFONTE_AUDIT_2026-11-04.md`.

**Nouvelle étude universitaire numérotée introduite par cette intervention : aucune** : réémettre un des 200 manuscrits attribués, débloquer arbitrairement les cinq retenues ou publier un brouillon aurait contourné la garde éditoriale. Aucun numéro n'a été réservé ou créé manuellement.

## Modifications apportées

La page d'accueil possède déjà trois cartes archéologiques sourcées (Ounas, tablette `Enūma eliš` K.3473, Apadana de Persépolis). L'intervention leur ajoute un bouton de lecture scientifique visible **sans ouvrir le panneau de crédits**, plus une ancre HTML unique par document. Les détails institutionnels, auteurs des photographies, licences et notices restent intacts.

Un bloc strictement navigant est désormais généré **à la fin des trois dossiers existants** correspondants : lien de retour à la bibliothèque scientifique de la civilisation et lien profond vers le document de l'accueil, sa photographie et sa légende. Les trois dossiers concernés sont :

1. `textes-pyramides-ounas-egypte-ancien-empire/index.html` → `/bibliotheque-egypte-ancienne/`
2. `enuma-elish-marduk-tiamat-creation-babylone/index.html` → `/bibliotheque-mesopotamie/`
3. `persepolis-apadana-reliefs-delegations-archives/index.html` → `/bibliotheque-perse-iran-ancien/`

L'ajout s'effectue dans les copies HTML générées de `_site`, et non dans les manuscrits sources. Il intervient **après** `enhance()` : sinon, les outils de lecture suppriment les blocs de navigation qu'ils possèdent. Cette garde a été corrigée pendant l'intervention. Le texte universitaire, les titres, les notes et les bibliographies restent inchangés, sans ajout de contenu académique inventé. Le nouveau style utilise noir/ivoire/or, liens de 44 px minimum, navigation en une colonne sous 650 px et suppression du bloc secondaire à l'impression.

## Commits enregistrés sur main

- `ee285e5ae10c6d1132e35fa75bdec870c598d220` — liens directs et réciproques dans le générateur.
- `235e382889f979290a3db8a71c6d598267a45bfb` — CSS muséal responsive des liens documentaires.
- `d3fbb219b1549ec5e123ec782f80e54eb9f66046` — tests de provenance, réciprocité, conservation du texte, idempotence et refus d'une source absente.
- `d9dcbefea98b148e59f06ad478cd1d6ab4cfc205` et `159a41a93c6ce19226f4889af1f6f3c381482958` — repositionnement de l'ajout après les outils de lecture pour éviter leur effacement.

## Contrôles et état de déploiement

Le générateur modifié, le CSS et les tests ont été relus depuis `main`. La validation GitHub Actions de la première série de commits (notamment `41852393353`) était **encore en cours** au contrôle. Le site public HTTPS a été lu directement : `/catalog/publication-verification.json` annonçait alors `source_commit=3358591f3247571d1aac9dcb5d35688c804f746b`, `github_run_id=41847280339`, **1324 entrées indexées**, **27 archives** et **110 médias**. Cette photographie **précède** les nouveaux commits. Le nouveau bouton et les renvois ne sont **pas déclarés déployés** à ce stade.

Vérifications de fin de parcours : tests unitaires du générateur, `scripts/build_native.py`, `scripts/verify_publication.py`, succès du workflow de publication et contrôle HTTPS de l'accueil ainsi que des trois dossiers et de leurs ancres. Aucune autre planification ou automatisation MYTHOS n'a été modifiée.
