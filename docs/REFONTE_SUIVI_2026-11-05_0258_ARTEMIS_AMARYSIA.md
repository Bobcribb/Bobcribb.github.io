# MYTHOS — Refonte du 5 novembre 2026 : Artémis Amarysia, dossier scientifique et lectures croisées

## État réel des sources, avant modification

Dépôt de publication : `Bobcribb/Bobcribb.github.io`, branche `main`. Tête initiale lue : `4c0849e4d82b468f63c5f09e9a67bdfb24459ea4` (5 novembre, 01:41 UTC). Règles relues : `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`.

La file contenait **300 demandes**, dont **295 reçus d'attribution** répartis dans les cinq séries, **5 demandes placées en attente documentée** (`editorial/holds.json`) et **aucune demande valide non attribuée**. Les documents historiques vérifiés dans `editorial/archives/` sont des versions parallèles sauvegardées précisément pour empêcher un doublon ; le manuscrit du *Konnos* d'Amipsias est conservé intégralement en archive de prépublication sans numéro. Les cinq demandes retenues ne doivent pas être intégrées en contournant le contrôle de collision. Le dossier `contenus/philosophie/homere-hesiode-dossier-preparatoire.md` se déclare lui-même préparatoire, non publiable comme étude définitive. Aucun nouvel original public, approuvé, intégral et absent du circuit de publication n'a été identifié dans les sources inspectées.

**Nouveau manuscrit intégral déposé à cette intervention : aucun.** Aucun UUID ni numéro éditorial n'a été créé, réattribué ou recyclé. Aucun brouillon WordPress privé n'a été importé.

## Manuscrit public complet vérifié et mieux relié

Le **chapitre canonique 426**, `chapitres/encyclopedie/chapitre-426-artemis-amarysia-amarynthos-eretrie-sanctuaire-procession-epigraphie.md`, compte **46 445 caractères** ; le registre d'attribution le rattache à la demande `4e61ad87-26c1-4f10-b979-96d356a8a5ca`. La page intégrale et son sommaire étaient déjà accessibles. L'étude traite le sanctuaire eubéen d'Amarynthos, Érétrie, les décrets, les processions, Strabon, Pausanias, l'épigraphie et les preuves archéologiques ; elle contient son appareil critique. Son texte n'a pas été modifié.

**Anomalie attestée sur le domaine public antérieur :** le fil d'Ariane du chapitre 426 ramenait au dossier `/mythologie-grecque/dossiers/divinites/#theme-2`, sous **« Les Olympiens et les dieux des Enfers »**. Ce classement générique écartait la monographie d'un dossier de sanctuaire bien plus pertinent.

**Correction apportée :** le générateur `scripts/build_greek_folders.py` classe le chapitre 426 dans `/mythologie-grecque/dossiers/cultes-sanctuaires/`, sous le sous-dossier **« Amarynthos et Érétrie — Artémis Amarysia, fêtes et inscriptions »**. Le sommaire et l'ancre de retour à ce sous-dossier utilisent les mêmes données, sans copie ni troncature du texte.

## Quatre études croisées, sans confusion cultuelle

Les quatre monographies déjà numérotées et vérifiées sont :
- **426**, Artémis Amarysia : Amarynthos et Érétrie ;
- **398**, Artémis Sôteira : Mégare, Trézène et Pellène ;
- **395**, Britomartis et Dictynna : Crète ;
- **424**, Dionysos Aisymnètès et Artémis Triklaria : Patras.

Le générateur ajoute, **à l'extérieur des articles originaux**, un panneau réciproque de trois liens par étude. Chaque renvoi conduit au **texte complet existant**, avec cote inchangée, sources et bibliographie conservées. Les légendes distinguent explicitement les sanctuaires et les témoignages ; une même divinité ne signifie pas un rituel identique d'une cité à l'autre. La génération répète ces panneaux sans doublon.

## Maquette muséale et ergonomie

Les nouveaux panneaux utilisent **`assets/mythos-museum.css`**, effectivement chargé sur toutes les pages de monographie, et non le CSS local réservé aux sommaires. Style sobre **anthracite, ivoire et or** cohérent avec la maquette commune ; cartes en deux colonnes puis une colonne sous **700 px** ; liens de **44 px** minimum, retour à la ligne des textes et focus clavier contrasté. Les illustrations, leurs crédits et la bannière photographique statue/temple existants sont préservés. Aucune reconstitution vectorielle 2,5D n'a été ajoutée.

## Commits de cette intervention

1. `f046b1b33295fdcda9d5ccf3081112a80c3263a9` — classement du chapitre 426, lectures croisées et gardes de cohérence.
2. `7bf527ab4d5f5d26700080a4cebe36440eef87fd` — tests des quatre manuscrits attribués, conservation des sources, liens réciproques et reconstruction répétée.
3. `5022a2b08a6a9ea9c873057baaf6f15bb5db46a9` — déplacement de la présentation depuis le CSS local réservé aux sommaires.
4. `2d4d83a4258332976b424ff7549b29a2040d33b2` — CSS muséal commun des panneaux, écran mobile et navigation accessible.
5. `e3a1e3a39cc109ef973adead10fdcef060a8155a` — test de garde du CSS commun.

## Contrôle de publication et limites

Au contrôle HTTPS initial, `https://bobmythos.fr/catalog/publication-verification.json` indiquait `source_commit=1bb2598f362efb766656d489fcddf71483379f69`, run **41948877607** (réussi), **1 419 documents indexés**, **27 archives**, **110 médias**. Cette version publique précède les commits ci-dessus et affiche encore le classement générique du chapitre 426. Les workflows des nouveaux commits ont été déclenchés, mais leur succès final et leur déploiement HTTPS **n'étaient pas confirmés** au contrôle.

Vérifications à effectuer par GitHub Actions sans déroger à la garde : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`. Après un nouveau reçu public : contrôler que le chapitre 426 renvoie vers le sous-dossier d'Amarynthos, que les quatre monographies affichent trois liens réciproques non dupliqués, et que le HTML scientifique et les bibliographies sont toujours intègres.

**Aucun manuscrit existant, reçu canonique, archive, workflow, numérotation ou horaire des autres automatisations MYTHOS n'a été modifié.**
