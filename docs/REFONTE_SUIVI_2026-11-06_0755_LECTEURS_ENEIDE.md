# MYTHOS — Refonte et accès intégral à l'Énéide (6 novembre 2026, séance du matin)

## Source de vérité, publication et numéro

- Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main` ; `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relus avant l'écriture.
- Dernier état initial examiné : `c6a90d24640b05d6deebb93b3b2a0ff88d49a039` ; aucune intervention sur `editorial/numbering.json`, `editorial/inbox/`, `editorial/holds.json` ou `chapitres/`.
- Le site public servait déjà l'étude intégrale `/philosophie-eneide.html` et les manuscrits originaux `/corpus/philosophie/eneide/00-introduction.md` et `17-reperes-et-sources.md`, contrôlés en HTTPS. Le manifeste public `/catalog/publication-verification.json` annonçait encore `source_commit = db016f6cbc0bec783e369a1e2874f0c6a1883aa6`, exécution `42175517252`, 1 604 documents indexés, 27 tomes et 110 médias. Ce manifeste décrit le déploiement antérieur ; il ne valide pas les commits ci-dessous.
- Les 18 sources Markdown de `corpus/philosophie/eneide/` ne sont **pas 18 études inédites** : elles étaient déjà présentes dans le texte universitaire réuni. Leur diffusion sous forme de 18 **lecteurs HTML individuels**, directement lisibles sur mobile, représente une nouvelle modalité de publication du corpus existant et non une attribution de volume.

## Sources examinées et blocage pour une nouvelle monographie distincte

- Contrôle ciblé des 18 fichiers originaux et du sommaire de l'étude ; validation automatisée avant rendu de chaque titre et de la présence de la bibliographie dans la dernière section.
- Les archives `editorial/archives/` (variantes MC-033 et MC-040, proposition Konnos) n'ont pas été resoumises : les premières correspondent à des dossiers déjà attribués, et Konnos a deux études canoniques, volumes 68 et 69.
- `editorial/holds.json` comptait 23 identifiants de demandes suspendues au contrôle. Les motifs explicitent des collisions de contenu ou de périmètre. Les publier sous un nouveau numéro contreviendrait aux règles de concurrence.
- Les brouillons historiques privés dans Google Drive ne peuvent pas être présumés approuvés pour une publication automatique. Aucun texte inédit indépendant, à la fois vérifié, approuvé et dépourvu de soumission préalable, n'a été constaté dans ce périmètre. **Aucun nouveau manuscrit numéroté n'a donc été déposé.**

## Modifications enregistrées dans le dépôt

1. `scripts/eneide_readers.py` : construit les 18 pages HTML en conservant chaque source Markdown octet pour octet dans `_site`, sans modifier le registre d'attribution.
2. `scripts/eneide_source_access.py` : chaque entrée du sommaire des sources mène désormais au lecteur HTML intégral de la section ; celui-ci renvoie à la version Markdown originale, à l'étude réunie, au sommaire et aux lecteurs précédent/suivant.
3. `assets/mythos-eneide-sources.css` : bannière de référence `mythos-museum-banner.webp` (statue grecque et temple), fond anthracite, typographie or et ivoire, lecteurs à une colonne, liens tactiles, navigation clavier, débordements contrôlés et style imprimable.
4. `tests/test_eneide_source_access_20261106.py` : tests de présence des 18 pages, du texte, de la bibliographie, des liens vers Markdown, de la navigation réciproque et de la stabilité du rendu. Conservation du contrôle de comparaison source/lecteur sur les 18 titres.

Les sources originales, archives, numéros canoniques et autres automatisations MYTHOS sont inchangés.

## Commits de la séance

- `6056cd69c3a199b49e10765121dff149c18783e3` — rendu autonome.
- `eb481d3e16bb4a1c6f68ad3162b0f9270b409578` — suppression des imports circulaires.
- `cd381e17199f3d70bae4f097b3b4a42a818a0607` — liaison entre les sources et les lecteurs.
- `594a65674a0fca659e426144a3766595ee0ac354` — CSS mobile et bannière muséale.
- `71cd5686b70b74c1aee9954c6e2574402558221f` — tests de non-troncature et d'accès aux références.

## Vérifications, limites et suite logique

Au contrôle documentaire, le fichier `/corpus/philosophie/eneide/00-introduction.md` était accessible publiquement, alors que `/corpus/philosophie/eneide/00-introduction.html` répondait encore **404** : nouveau rendu **non encore déployé**. Les workflows de validation et publication déclenchés à 07:02 UTC étaient en cours, non pas validés par avance.

Avant d'annoncer le déploiement, exiger cumulativement : validation du générateur, exécution de publication réussie, manifeste avec le SHA de source attendu et accès HTTPS aux 18 nouveaux lecteurs, notamment `00-introduction.html` et `17-reperes-et-sources.html`. Vérifier la navigation sur écran étroit. Ne pas confondre dépôt et site publié.
