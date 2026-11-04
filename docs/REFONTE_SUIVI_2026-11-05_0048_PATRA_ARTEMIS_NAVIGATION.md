# MYTHOS — Refonte du 5 novembre 2026 : Patras, Artémis Sôteira, sommaires longs et garde de publication

**Site :** https://bobmythos.fr · **Dépôt :** `Bobcribb/Bobcribb.github.io`, branche `main`.

## 1. État préalable de `main`, garde et inventaire

État initial du dépôt contrôlé : `96064458c4d4cb2135ae0cdb3a4d4c9426600523` (4 novembre 2026, 23:36:34 UTC). Avant toute décision de numérotation, relecture explicite de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`, identiques aux versions accessibles sur `main`.

L'arbre complet du dépôt actif expose au début de l'opération **3 188 fichiers** (3 189 après création d'un nouveau test). Inspection de `editorial/inbox/`, `editorial/numbering.json` et `editorial/holds.json` : **288 demandes persistantes**, **283 reçus attribués**, **5 retenues** et **0 demande valide sans reçu** au contrôle. Aucune demande de publication nouvelle ne doit être créée pour un manuscrit déjà attribué ou retenu.

Contre-vérification de la source historique : le dépôt `Bobcribb/Mythos` possède **205 fichiers**, dont **37 Markdown**. La branche active conserve **36** de ces Markdown au même chemin. L'exception `docs/etat-publication-images-3d.md` est une note de suivi des images, et non un nouveau manuscrit universitaire intégral à attribuer. Les anciennes compilations et les neuf comédies sont préservées. Les anciens brouillons WordPress privés, sans statut d'approbation publique, restent exclus du circuit.

**Contenus universitaires intégraux nouvellement soumis ou publiés dans cette intervention : zéro.** Aucune étude publique intégrale nouvelle, approuvée et absente de la publication n'est identifiée par ces vérifications. Ne pas inventer une cote, une synthèse substitutive ou un nouvel UUID.

## 2. Monographies universitaires publiées, vérifiées et mieux reliées

Deux manuscrits **déjà publiés** ont été relus dans leur intégralité, conservés sous leur cote originale et dirigés vers des sous-dossiers mieux adaptés au sujet historique :

- **Chapitre 398 — Artémis Sôteira**, `chapitres/encyclopedie/chapitre-398-artemis-soteira-megare-trezene-pellene-salut-cites.md`. **10 151 caractères**, **24 sections numérotées**, bibliographie et références à Pausanias. Il concerne Mégare, Trézène, Pellène, les serments, l'épiclèse et les sanctuaires ; il relève du dossier **Cultes et sanctuaires / Mégare, Trézène et Pellène — Artémis Sôteira et salut civique**. Ancien classement : **Divinités / Les Olympiens et les dieux des Enfers**.
- **Chapitre 424 — Dionysos Aisymnètès**, `chapitres/encyclopedie/chapitre-424-dionysos-aisymnetes-patras-eurypyle-triklaria-fete-rites.md`. **56 838 caractères**, **52 sections numérotées**, bibliographies des sources anciennes et modernes, dossier d'Eurypyle et d'Artémis Triklaria, étude de Pausanias VII. Il relève du dossier **Cultes et sanctuaires / Patras — Dionysos Aisymnètès, Artémis Triklaria et Eurypyle**. Ancien classement : **Divinités / Les Olympiens et les dieux des Enfers**.

Modification exclusivement dans `scripts/build_greek_folders.py` : deux règles de classement prioritaires, fondées sur le sujet de l'étude et non sur des noms seulement cités en passant. La nouvelle génération des dossiers reliera les **textes intégraux** à leur sous-dossier exact avec un sommaire et insérera dans les lecteurs leurs **renvois réciproques** vers l'ancre de ce sous-dossier. Les intitulés restent distincts : les autres études générales sur Dionysos ou Artémis ne changent pas de rubrique. **Ni le corps du texte, ni la bibliographie, ni les numéros, ni les archives n'ont été retouchés.**

## 3. Refonte responsive du lecteur universitaire

`assets/mythos-discovery.css` améliore le sommaire natif `<details class="mythos-reading-toc">` sans ajouter de JavaScript ni supprimer les ancres :

- Commande `<summary>` de **44 px minimum**.
- Chaque lien d'une section dispose d'une cible tactile **44 px minimum**, d'une bordure de séparation et d'un indicateur de focus clavier doré.
- Le sommaire ouvert est défilable à hauteur limitée (**60 vh**, maximum **630 px**) ; sur écran inférieur à 700 px, il plafonne à **55 vh** et utilise une marge/padding adaptés.
- La liste conserve l'ordre et les **52 ancres** de l'étude de Patras ; le lecteur intégral, les sources et la bibliographie restent dans le flux documentaire.

Un test dédié `tests/test_greek_cult_titles_mobile_20261105.py` contrôle les deux sources, leurs cotes, les nombres de sections, les bibliographies, le classement, les sujets voisins non concernés, les règles tactiles et le sommaire réel du chapitre 424. Les règles s'appliquent aux lecteurs sur smartphone, tablette et ordinateur, avec les couleurs ivoire/or existantes et la bannière statue/temple inchangée.

## 4. Détection et correction d'un autre blocage de CI

L'examen des logs des runs `41937129458` et `41936901333` révèle un échec préexistant : `tests/test_verify_live_site_assets.py`, méthode `test_all_thirty_one_documentary_figures_and_six_pages_verified`, attendait **31 résultats HTTPS** alors que le vérificateur retourne **un résultat par page HTML (6) et un par fichier image distinct (24)**, soit **30 résultats pour 31 occurrences de figures**. Une image de Rembrandt est légitimement réutilisée sur deux pages.

Correction : garder l'exigence documentaire de **31 figures**, calculer le nombre de vérifications réseau à partir de **`len(pages) + len(assets)`** et comparer séparément la somme des figures effectivement contrôlées à 31. **Aucun fichier image ni témoin archéologique n'est supprimé.**

## 5. Commits et preuve de déploiement

Commits enregistrés pendant cette intervention :
- `ee20e53a` : règles initiales de rattachement.
- `61b7f8bb` : correction immédiate des bornes de mots dans les expressions régulières.
- `67e8ce6a` : sommaires de lecture tactiles et défilables.
- `d24fe9df` : ajout des tests de conservation des deux monographies.
- `d1a29155` : correction de la regex du test.
- `996544f3` : correction du décompte des contrôles HTTP de 31 figures.

Au contrôle HTTPS du **5 novembre 2026**, `https://bobmythos.fr/catalog/publication-verification.json` indiquait toujours `source_commit=98a0abac86d56e24902f3dcafe804f91fb96a1f8`, GitHub Actions **41933951937**, **1 407 documents**, **27 archives** et **110 médias**. Le chapitre public 424 renvoyait encore au dossier « Divinités ». Ce reçu **antérieur aux commits de cette intervention** ne prouve pas le déploiement des corrections ; la publication publique des nouveaux renvois n'est pas encore confirmée.

Contrôles attendus après reconstruction sur la dernière révision : exécution intégrale des tests, génération autonome `scripts/build_native.py`, vérification `scripts/verify_publication.py`, puis concordance du reçu public, de l'ancre de Patras dans `/mythologie-grecque/dossiers/cultes-sanctuaires/` et des liens de retour des chapitres 398/424.

Aucun changement des cinq registres de numérotation, de `editorial/inbox/`, des manuscrits, des archives, du menu unique de mythologie grecque, des illustrations vectorielles 2,5D supprimées, ni des autres automatisations et de leurs horaires.
