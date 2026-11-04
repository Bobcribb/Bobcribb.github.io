# MYTHOS — Refonte et restitution du mémoire intégral sur Akhetaton
**Date :** 4 novembre 2026. **Dépôt de référence :** `Bobcribb/Bobcribb.github.io`, branche `main`.

## Contrôles préalables
Avant toute intervention, lecture de `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, du registre `editorial/numbering.json`, de la file `editorial/inbox/` et des derniers résultats GitHub Actions. Les études des cinq collections numérotées passent exclusivement par la file et ses UUID. Le mémoire restitué est **hors de ces cinq collections**, dans le dossier historique déjà existant `/akhetaton-horizon-aton-etude/` ; sa cote de référence est son titre historique, sans numéro inventé.

L'ancien dépôt public `Bobcribb/Mythos` a été comparé au dépôt actif : aucun nouveau manuscrit universitaire textuel original n'est absent du dépôt principal ; la seule différence documentaire détectée est un rapport technique d'images 3D. Les anciens brouillons WordPress privés présents sur Google Drive ne sont pas versés sur GitHub.

## Contenu scientifique nouvellement intégré
**L'Horizon d'Aton — Akhetaton et la transformation du sacré dans l'Égypte du Nouvel Empire** : manuscrit final Google Docs intitulé `L’Horizon d’Aton — Étude universitaire · Lecture mobile` du 4 novembre 2026, explicitement rédigé pour MYTHOS, vérifié dans son intégralité et comparé à la notice déjà publiée.

- Source universitaire vérifiée : **406 paragraphes**, **652 segments de texte** (74 153 caractères au total, délimiteurs de paragraphes compris), **22 grandes rubriques** dont **16 chapitres**, **59 sous-sections**, **5 tableaux** (35 lignes), **3 figures** et **28 liens documentaires** de Google Docs.
- Destination : `akhetaton-horizon-aton-etude/index.html`, à l'emplacement existant, sans ouverture d'un doublon thématique et sans troncature volontaire. La notice d'origine, ses 12 questions/sections et ses renvois restent avant le mémoire intégral. Une ancre unique `#horizon-aton-memoire-integral` et un sommaire à ancres relient les parties.
- Illustrations conservées sous forme de photographies publiques de référence, à la place des URL éphémères et privées de Google Docs : Met 1985.328.2 (relief d'Akhenaton sacrifiant un canard, https://www.metmuseum.org/art/collection/search/544056) ; Met 31.114.1 (tête de statuette, https://www.metmuseum.org/art/collection/search/544685) ; Met 24.2.11 (lettre d'Aššur-uballiṭ, https://www.metmuseum.org/art/collection/search/544695). Les légendes, numéros d'inventaire et crédits Open Access sont maintenus ; aucune ancienne image vectorielle 2,5D réintroduite.
- La page d'origine comptait **17 431 caractères HTML**, puis **107 998 caractères** après restitution. La présence de **5 tableaux**, **3 figures**, **28 liens « Consulter la source »**, des annexes, de la bibliographie et de **l'unique section intégrale** a été relue sur un commit ultérieur de `main`.
- La collection `bibliotheque-egypte-ancienne/index.html` propose désormais un lien profond vers cette ancre. Le mémoire contient en retour un lien vers la bibliothèque de l'Égypte ancienne. Un test existe dans `tests/test_horizon_aton_integral_publication.py`.

**Concurrence constatée :** une seconde tâche MYTHOS a tenté, presque simultanément, une deuxième insertion du même mémoire sous le commit `7dbfff8`. Le commit ultérieur `411545d` a retiré cette double transcription. La lecture de `main` après réconciliation confirme **une seule section `data-mythos-integral-source=\"horizon-aton-2026-11-04\"`**, sans reprise concurrente restante.

## Graphisme et navigation
- Correction du générateur `scripts/apply_museum_design.py` pour conserver explicitement l'illustration documentaire authentifiée de La Galigo (folio de Leyde CC BY-SA 4.0) dans la carte de collection, sans restaurer les anciens SVG 2,5D.
- Test ajouté dans `tests/test_museum_verified_documentary_card.py` : conservation après trois passes et refus d'une vignette SVG non approuvée.
- Styles ajoutés à `assets/mythos-museum.css` : noir/ivoire/or, sommaire centré sur deux colonnes (une sur mobile), texte lisible, figures documentaires légendées, tableaux défilables sur petits écrans et présentation imprimable. La bannière muséale statue grecque à gauche et temple à droite n'a pas été remplacée.

## Commits propres à l'intervention
- `fbda5adde166d73489da0ecf4ac6033fe9361072` : conservation ciblée du folio de La Galigo dans le générateur.
- `3ed5fc94b33f31916fc576889c228d3f15b456d1` : test d'idempotence du folio.
- `8dfe8312ef7a5f91c99e553b035b4e7845edf8ac` : intégration intégrale du mémoire d'Akhetaton.
- `32869694bb8adb73e915f3e4e61efa69c192233f` : CSS responsive du mémoire.
- Les commits `7dbfff8` et `411545d`, réalisés par un autre chantier concurrent, sont cités pour tracer la suppression du doublon, non comme travail de cette intervention.

## Statut de vérification et limites
Les fichiers modifiés ont été relus directement sur la branche `main`, avec contrôle des ancres, titres, tableaux, figures, liens bibliographiques et du lien depuis le portail. Le test Python de publication du mémoire a été inscrit dans `tests/` par le chantier concurrent ; son **résultat GitHub Actions** reste à vérifier. Les workflows récents pouvaient être en attente ou annulés au profit de versions ultérieures. La présence sur `main` ne prouve pas la présence sur `bobmythos.fr`. La vérification publique doit confronter l'état de `/catalog/publication-verification.json`, le dernier déploiement Pages terminé avec succès et l'ancre `/akhetaton-horizon-aton-etude/#horizon-aton-memoire-integral`. Aucun déploiement non contrôlé n'est revendiqué.

Aucun numéro canonique ni registre n'a été modifié manuellement. Aucune planification horaire ou automatisation MYTHOS distincte n'a été changée. Les archives et les manuscrits existants sont conservés.
