# MYTHOS — Parcours de Béotie et futur classement des monographies en file

**Date :** 5 novembre 2026. **Dépôt :** `Bobcribb/Bobcribb.github.io`,
branche `main`. Consignes de publication `AGENTS.md` et
`docs/PUBLICATION_CONCURRENTE.md` relues avant intervention.

## Sources intégrales déjà présentes et conservées

Quatre monographies canoniques, chacune avec source Markdown, lecteur HTML
existant, références et bibliographie :

- 442 — Poséidon Onchestios : Onchestos, chars sans conducteur et
  mémoire fédérale béotienne ;
- 444 — Éros à Thespies : pierre aniconique, Praxitèle, Phryné
  et Érotidies ;
- 445 — Hermès Kriophoros à Tanagra : bélier, maladie et rites
  protecteurs ;
- 448 — Amphiaraos à Oropos : oracle, incubation et guérisons,
  sur une frontière politique entre Béotie et Attique.

Ajout d'un **parcours de lectures croisées à trois renvois réciproques
par monographie**, généré dans l'habillage muséal et hors du texte
scientifique. Les sources sont indépendantes ; la proximité des lieux
ne constitue pas une preuve de rite commun. Aucun passage, cote, titre
original ou bibliographie n'est recopié ou abrégé. Le classement
thématique primaire reste conservé.

## Cinq manuscrits intégraux approuvés et déjà en file

Leur attribution est réservée exclusivement à GitHub Actions.
Le générateur préparera leur classement **après création de la page
canonique**, sans lien de prématuré dans le catalogue :

- Athéna Chalkioikos à Sparte — acropole et droit d'asile ;
- Apollon Isménios à Thèbes — trépieds et Daphnéphories ;
- Apollon Amyklaios — Hyakinthos et sanctuaire d'Amyclées ;
- Trophonios à Lébadée — descente oraculaire et mémoire ;
- Hélène et Ménélas au Ménélaion de Thérapné.

Ces cinq études existent déjà dans `editorial/inbox/` avec des slugs
distincts et un texte long. Aucune nouvelle demande, aucun UUID
et aucune attribution ne sont créés par cette intervention.

## Graphisme et contrôles

Les quatre panneaux réutilisent les cartes noires à typographie
ivoire et liens or, les commandes clavier et la grille responsive
existante à une colonne sous 700 px. Aucun 2,5D ni photographie
sans rapport n'est introduit.

`tests/test_greek_boeotia_reciprocal_20261105.py` vérifie les
quatre sources et lecteurs, les liens réciproques, l'absence de
doublons après deux reconstructions, les classements futurs conditionnels,
la non-injection de pages non publiées et la conservation exacte des
articles et empreintes des Markdown.

**Premières publications universitaires nouvelles dans cette
intervention : zéro.** Les manuscrits non encore attribués sont déjà
enregistrés ; les reproduire contournerait la garde. Les nouveaux
liens doivent être vérifiés sur bobmythos.fr après réussite d'un
workflow de publication. Le présent commit ne constitue pas
une confirmation de déploiement. Les archives, la numérotation,
le domaine et toutes les automatisations MYTHOS restent inchangés.
