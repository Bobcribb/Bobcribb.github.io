# MYTHOS — Réconciliation du dossier Aphrodite, Sappho et Palaepaphos

**Intervention : 5 novembre 2026.** Dépôt actif : `Bobcribb/Bobcribb.github.io`, branche `main`. Tête contrôlée avant écriture : `db1baa46b86b0cf90f2b11e30de067f8213d67a8`. Les gardes `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relues sur cette branche avant les modifications.

## 1. Inventaire des manuscrits et statut de publication

Au point de contrôle, `editorial/inbox/` contenait **312 UUID**, dont **307 avec allocation** dans `editorial/numbering.json` et **5 soumissions explicitement retenues** dans `editorial/holds.json`. Il n'existait **aucun UUID non attribué et non retenu** au moment de la lecture. Les anciennes études d'Aristophane et les archives historiques présentes dans `Bobcribb/Mythos` sont aussi conservées dans le dépôt actif ; leur recopie n'est pas une publication inédite.

**Nouvelle étude intégrale inédite soumise durant cette séance : aucune.** Aucun manuscrit complet, approuvé, public et encore absent du circuit canonique n'a été identifié parmi les sources accessibles. Ne pas importer les brouillons privés ni inventer une numérotation. Aucun fichier `editorial/inbox/`, `editorial/numbering.json` ou `chapitres/` n'a été modifié.

En revanche, une **étude universitaire intégrale déjà publiée** sous la rubrique Civilisations n'était **pas référencée dans l'entrée unique de l'encyclopédie grecque** : `/bibliotheque-mythologies-du-monde/civilisations-chypre-paphos-aphrodite/`. Le fichier `index.html` associé est un document scientifique de **20 877 caractères** (UTF-8 décodé lors de l'inspection), avec **11 sections de lecture**, présentation du sanctuaire de Palaepaphos, chronologie des royaumes, examen distinct des récits d'Hésiode et d'Homère, sources académiques et appareil critique. Le blob de source était `e5d059c4ca6ffb05b4d89471fb59fe1ae6c77652`. La page publique est déjà accessible ; la nouveauté est **son référencement réciproque dans le corpus grec**, pas une prétendue première publication de son manuscrit.

Deux autres lecteurs intégraux, vérifiés avant intégration dans le parcours :
- `/corpus/mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html` — monographie universitaire `MG · 02`, **37 894 caractères**, dix rubriques de sommaire, sources, philologie, cultes, variantes, analyses et bibliographie ; blob source `4f8d56ff69443686103d9630d684d48d7f31b249`.
- `/sappho-aphrodite-poesie-lyrique-fragments-papyrus/` — étude littéraire intégrale, **46 635 caractères** HTML, dix-neuf sections de lecture, papyrus, fragment 1, éthique de la provenance et bibliographies ; blob source `cb50e4b1b8a0f3c8a22950cb6fa0ada178fbf0f8`.

Ces documents **existaient déjà** sur le site : leur identité, leur contenu, leurs réserves méthodologiques et leurs adresses demeurent inchangés.

## 2. Intégration documentaire effectuée

`scripts/build_greek_corpus.py` référence maintenant l'étude de Palaepaphos dans la liste des lectures associées au portail grec. Ce lien est affiché au même titre que les études philosophiques déjà référencées ; aucun fichier n'est copié.

`scripts/build_greek_folders.py` lui attribue une seule destination primaire **Cultes et sanctuaires → Palaepaphos — Aphrodite et histoire du sanctuaire**. Les autres études conservent leurs familles : **Divinités** pour la monographie Aphrodite, **Sources anciennes** pour Sappho. Chaque lecteur reçoit automatiquement un fil d'Ariane vers son sous-dossier précis ainsi qu'un panneau de deux liens réciproques vers les autres études, **en dehors** de `article`. Une seconde reconstruction enlève et recrée le panneau : aucun lien dupliqué.

Le panneau mentionne explicitement la limite documentaire essentielle : les récits grecs ne démontrent pas à eux seuls la date ni la forme des pratiques au sanctuaire de Palaepaphos. Trois approches complémentaires ne sont pas confondues : monographie divine, papyrologie/poésie archaïque, archéologie et histoire locale.

## 3. Design responsive et accessibilité

`assets/mythos-museum.css` conserve la présentation muséale anthracite/ivoire/or, la bannière grecque déjà présente, les médias documentaires et les cartes sources. Une variante sobre de panneau « Aphrodite » ajoute un liseré doré, une séparation sous le titre, une grille existante de deux colonnes puis une colonne sous **700 px**, une adaptation sous **480 px**, et conserve les zones tactiles de **44 px** et le focus visible. Aucune photographie ou ancienne perspective 2,5D n'est introduite.

## 4. Tests et commits

Les tests ajoutés dans `tests/test_greek_folders.py` vérifient : l'existence et le contenu non trivial des **trois sources intégrales** dans `main`, leur présence dans l'inventaire et leur affectation unique, les renvois bidirectionnels, la page `.html` d'Aphrodite, le respect des balises `article`, l'idempotence de **deux reconstructions**, et le CSS responsive commun.

Commits de l'intervention :
- `ce665d92960eabba70ad9540dccbbf9a86cfd5a3` — ajout de Palaepaphos dans les sources de l'entrée grecque.
- `beea18793b73671e58d84ef0ea2117d9be71e0fc` — classification du dossier, panneaux et contrôle.
- `0a4c643388c9dcc5d88654c4736f02ba88fd289c` — conservation des liens pour la page Sappho (catégorie « Dossier documentaire »).
- `59f5292d156a1e040f0845008b778b378d3c333b` — tests du parcours et de la conservation des textes.
- `590aeea2b6201eb1f4dd47be8597189917b4d3bd` — styles de lecture.
- `dec20fc129dab3c1bd229970bbd59cd0e361c11d` — garde de non-régression visuelle.

## 5. Contrôles GitHub Pages et limite de déploiement

À la consultation HTTPS avant livraison de cette séance, le reçu public `/catalog/publication-verification.json` renvoyait le **commit source `3ff7fd978e59d8bf897226cf2358ec4a653c7815`**, exécution **41961838217**, **1 431 documents indexés**, **27 archives** et **110 médias**. L'étude intégrale sur Chypre et Palaepaphos était accessible, mais le sommaire public du dossier **Cultes et sanctuaires** ne portait pas encore son entrée. La version publique contrôlée ne présentait pas le panneau « Aphrodite : du poème au sanctuaire ».

**Les modifications sont enregistrées dans le dépôt, non encore attestées sur le domaine public**. La publication et les validations consécutives étaient en cours/en attente au dernier contrôle. Avant toute affirmation de mise en ligne, vérifier le succès des tests, la génération, la progression du reçu `source_commit`, les trois panneaux HTTPS, l'entrée Palaepaphos dans les sous-dossiers et l'intégrité des lecteurs.

Aucune modification des autres automatisations, de leur calendrier, du registre canonique ou des textes intégraux.
