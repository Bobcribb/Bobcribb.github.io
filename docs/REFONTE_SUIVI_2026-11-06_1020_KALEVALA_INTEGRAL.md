# MYTHOS — Refonte, restitution du Kalevala et contrôle de déploiement

**Intervention du 6 novembre 2026.** Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`. État initial relu : commit `c9281b4af4c09faa92a14a8393779d0e68d0c421`. Les règles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été lues avant toute écriture.

## Contenu universitaire réellement intégré

**Titre historique :** Volume X — *Mythologies finno-caréliennes : Väinämöinen, Ilmarinen, Louhi et le Sampo*.

**Source :** sauvegarde WordPress conservée sur Google Drive, volume privé 02, entrée `1134`, slug d'origine `mythos-volume-10-finno-carelien-kalevala`, statut historique `draft`. Le contenu scientifique a été extrait individuellement et examiné dans le cadre de la demande explicite d'intégrer un manuscrit existant ; **la sauvegarde privée brute et les neuf autres entrées du volume n'ont pas été publiées**. Le contenu de cette page conserve la provenance historique et ne prétend ni être une édition critique publiée par les institutions citées ni avoir fait l'objet d'une évaluation universitaire indépendante.

**Déduplication :** recherche préalable dans les pages et sources GitHub à partir des noms Kalevala / finno-carélien, et absence du dossier cible sur `main`. Des pages historiques comparatives traitent d'autres traditions ; elles n'ont pas été remplacées.

**Nouvelle page source :** `bibliotheque-mythologies-du-monde/mythos-volume-10-finno-carelien-kalevala/index.html`  
**URL publique attendue :** `https://bobmythos.fr/bibliotheque-mythologies-du-monde/mythos-volume-10-finno-carelien-kalevala/`

**Comparaison d'intégrité obtenue après relecture GitHub :**
- 48 625 caractères dans le champ HTML de la source WordPress et **48 625 caractères identiques** après extraction du contenu intégré et retrait des seules ancres ajoutées ;
- 20 sections principales, 62 rubriques et sous-rubriques accessibles par ancres ;
- sections « Sources et documentation » et références bibliographiques conservées, notamment à Lönnrot, à la Société de littérature finlandaise et à la Library of Congress ;
- aucun chapitre académique remplacé, abrégé ou numéroté artificiellement.

La **cote « Volume X » est une cote historique WordPress**, non une attribution canonique nouvelle. Ce dossier appartient à la bibliothèque des mythologies du monde, **hors des cinq séries** `origines-du-sacre`, `encyclopedie`, `comedies`, `tragedies`, `comparatif`. Aucun `editorial/inbox/<uuid>.json` ni registre de numérotation n'a été modifié pour ce transfert : la règle atomique reste intacte pour ses cinq collections.

## Refonte et parcours

- `scripts/build_navigation.py` : ajout d'une carte de lecture directe dans le portail `/mythologies/`, sans second texte ni double entrée « Grande Encyclopédie ».
- La page conserve ses analyses, ses liens de sources et ses références et ajoute un sommaire déroulant de 20 parties, avec 62 ancres.
- Renvois éditoriaux vers `/mythologies/`, `/civilisations/europe/`, `/bibliotheque-mythologies-du-monde/`, `/philosophie/` et `/recherche/`.
- `assets/mythos-museum.css` : noir, ivoire et or ; blocs de lecture étroits, colonnes de sommaire sur grand écran, une colonne sous 720 px, retour à la ligne et cibles tactiles.
- Le lecteur est compatible avec `scripts/apply_museum_design.py`, qui applique automatiquement le bandeau institutionnel existant. La bannière grecque statue–temple et les reconstitutions photoréalistes antérieures ne sont pas modifiées.

## Commits de cette intervention

1. `a322d727eb2292d501ea64e05cf3f8333f4882f1` : restauration du texte intégral et création de la page.
2. `c828b6c7790382c1dc744f824d4cbe5b1adda368` : lien réciproque depuis le portail des mythologies.
3. `b02ba1848440e32677ebee2856b6c65cb8f77b36` : adaptation CSS responsive.
4. `6dae772d9940b5fec857b33252353617a2a0b98b` : tests de conservation, navigation et présentation muséale.

Le test `tests/test_kalevala_archive_integrity_20261106.py` vérifie la reconstruction de la source, l'absence de suppression de paragraphes pendant la présentation, les ancres, le lien de portail et l'absence de numérotation parallèle.

## Distinction GitHub / site public

**GitHub :** création et relecture du nouveau fichier confirmées ; comparaison de son texte à la source WordPress confirmée (égalité stricte de 48 625 caractères). Les tests GitHub Actions ont été déclenchés.

**Contrôle HTTPS au cours de l'intervention :** le manifeste `/catalog/publication-verification.json` annonçait encore le commit ancien `db016f6cbc0bec783e369a1e2874f0c6a1883aa6`, et la nouvelle URL Kalevala répondait `404`. Le portail `/mythologies/` affichait encore l'ancien sommaire sans cette carte. Le déploiement est donc **non confirmé**, malgré les commits. Au premier contrôle, la validation `test-native.yml` associée au commit `6dae772d` (run `42194408188`) était en cours ; le workflow de publication `publish.yml` du commit `b02ba184` (run `42194183286`) était en attente.

**Critères de confirmation à contrôler après exécution des Actions :**
1. succès de la publication sur un descendant des commits de cette intervention ;
2. changement du `source_commit` du manifeste HTTPS ;
3. HTTP 200 et texte complet sur la nouvelle page Kalevala ;
4. présence du lien depuis `/mythologies/` et du bandeau graphique noir et or ;
5. conservation des tests de non-régression.

Les archives privées et publiques, les autres manuscrits et toutes les planifications MYTHOS sont préservés ; aucun réglage de leurs automatisations n'a été modifié.
