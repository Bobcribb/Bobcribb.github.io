# MYTHOS — Refonte documentaire, folio La Galigo et suivi de publication (4 novembre 2026)

## Règles et photographie de travail

Dépôt public : `Bobcribb/Bobcribb.github.io`, branche `main`. Avant les modifications, relecture intégrale de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`. Ces règles sont inchangées : les nouveaux textes des cinq collections numérotées passent exclusivement par `editorial/inbox/<uuid>.json`, avec `{{numero}}` / `{{volume}}`, attribution atomique par GitHub Actions et reçu dans `editorial/numbering.json`. Aucune modification des compteurs, des numéros publiés, des workflows ou des planifications horaires.

## Contenus universitaires examinés et statut

1. **La Galigo — Volume XIX, mythologies du monde.** Manuscrit historique WordPress 1151, volume de sauvegarde 02, texte source Gutenberg de 48 156 caractères selon `docs/restauration-la-galigo-2026-11-04.json` (SHA-256 source : `b1d96d266dec47e2dc4de91916b8f72701a59e9a3d35cbb47c21bbc43ece4bd2`). Le manuscrit avait déjà été restauré **avant cette séance** au chemin public `bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/index.html` ; ne pas le dupliquer. Au contrôle précédant l'insertion, son bloc `section#etude-integrale` contenait 40 776 caractères de HTML, environ 36 027 caractères de texte brut, 69 paragraphes et 21 titres h2 ; bibliographie, sources et ancres sont en place. La présente séance conserve intégralement ce bloc, sans résumer ni retrancher un passage.
2. **Hormè — l'élan divin et la responsabilité de l'action**, étude approuvée de 10 108 caractères : déjà soumise par un autre travail à `editorial/inbox/e3b50ab4-20ef-43f6-972e-8ef13c580c2a.json`, collection `encyclopedie`, slug `horme-elan-impulsion-action-agora-stoiciens`. À la lecture du registre, 137 demandes sur 138 étaient attribuées et cet UUID était encore en attente. Ne surtout pas déposer un deuxième exemplaire ni inventer son numéro. Une soumission de comédie supplémentaire a été observée ensuite sur `main` ; elle n'est pas revendiquée comme travail de cette séance.
3. **Archives WordPress sur Drive.** Quinze volumes de sauvegardes privées sont accessibles, mais leur index les qualifie explicitement de brouillons non destinés à être publiés en masse. La vérification de leur intégralité ne vaut pas validation éditoriale. Aucun import en bloc ou diffusion d'un manuscrit privé n'a été effectué.

**Bilan des études intégrales nouvelles soumises dans cette séance : zéro.** Cause documentée : l'étude La Galigo est déjà publiée, Hormè est déjà en file d'attribution, les archives restantes examinées ne sont pas des nouveaux manuscrits publics approuvés. Le maintien de l'unicité des titres et des UUID prévaut sur la production d'un doublon.

## Modifications concrètes d'iconographie et de navigation

- L'étude La Galigo ne contenait aucune balise `img` ni `figure`. Insertion d'une photographie documentaire d'un folio du manuscrit (1906), conservé par **Leiden University Libraries**, fournie sur Wikimedia Commons sous **CC BY-SA 4.0**. Source photographique : `https://commons.wikimedia.org/wiki/File:La_Galigo_item_29355-0009_(cropped2).jpg` ; notice de l'institution : `https://hdl.handle.net/1887.1/item:29487` ; licence : `https://creativecommons.org/licenses/by-sa/4.0/`.
- La figure précède `section#etude-integrale`. L'ajout a été réalisé par insertion sans modifier ni déplacer les 40 776 caractères du bloc scientifique. Texte alternatif descriptif, chargement différé, lien vers l'institution, crédit et restrictions de portée (« non reconstitution », pas une édition intégrale).
- Style noir/ivoire/or de `assets/mythos-museum.css` : disposition en deux colonnes sur grand écran, image et légende empilées sous 620 px, cadre discret, comportement à l'impression ; la bannière statue grecque / temple et les anciennes illustrations photoréalistes restent en place, sans retour des dessins 2,5D.
- Ajout de la même photographie à la carte `Sulawesi — La Galigo` du portail `mythologies/index.html` et d'un crédit institutionnel visible ; les liens de la carte restent identiques.
- Nouveau test `tests/test_galigo_documentary_illustration.py` : vérifie la conservation d'un bloc long, les ancres et la bibliographie, le crédit/licence, l'illustration de la carte et le CSS mobile.

## Commits enregistrés sur main

- `566e1a32eb9cd7a93912824dfcc76ad874729219` — illustration documentaire et légende dans l'étude.
- `50f2a21f63e15282c95d898959c97469ce9f1f5d` — style responsive du folio.
- `787af69ba46d66ff16ec2f5e1059ab68c317e04e` — tests documentaires initiaux.
- `468180c829f0be17696f55510c065c1d46edaf4a` — carte illustrée dans le portail.
- `0f4026a606881b1f63346de65622e170972148e3` — contrôle supplémentaire de la carte et de son crédit.

## Contrôles et réserves

Les lectures après écriture de GitHub montrent la figure (`data-mythos-illustration="leiden-galigo-1906"`), la carte (`data-mythos-card-source="la-galigo-leiden"`) et les quatre méthodes de test dans `main`. Les balises scientifiques `#bibliographie`, `#sawerigading-voyages`, `#we-cudaiq-heroines` et `#manuscrits-lontara` demeurent présentes.

Une consultation HTTPS de `bobmythos.fr` a trouvé la page d'étude publique, mais **pas encore la nouvelle figure** ; la modification GitHub ne doit donc pas être présentée comme déjà déployée. Plusieurs workflows de publication précédents ont été annulés ou remplacés dans un contexte de soumissions très rapprochées ; le dernier workflow examiné était en attente ou en cours. Une exécution antérieure avait échoué pendant l'installation de Playwright sur Ubuntu 26.04 ; le fichier de workflow actuel est configuré sur Ubuntu 24.04. **N'annoncer ni tests verts ni déploiement effectif sans preuve Actions et contrôle HTTPS postérieurs aux commits.**

Les autres automatisations MYTHOS et leurs horaires ne sont pas modifiés.
