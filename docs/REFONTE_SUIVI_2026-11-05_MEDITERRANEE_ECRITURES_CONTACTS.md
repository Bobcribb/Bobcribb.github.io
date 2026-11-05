# MYTHOS — Refonte : écritures et contacts méditerranéens

**Date de l'intervention :** 5 novembre 2026. **Dépôt :** `Bobcribb/Bobcribb.github.io`, branche `main`.

## Statut documentaire et garde éditoriale

`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été consultés. La file observée au début de l'intervention comporte **349 objets JSON**, pour **331 attributions** et **6 demandes retenues**. Les demandes valides non encore attribuées sont déjà en file ; aucun UUID supplémentaire n'est créé et aucun numéro ne peut être annoncé avant son reçu. Les versions parallèles archivées et les manuscrits privés ne constituent pas une autorisation de première publication.

**Aucune première publication intégrale supplémentaire** n'est revendiquée dans cette intervention. Quatre monographies déjà accessibles sur le site général ont été identifiées comme absentes du répertoire de lectures de l'encyclopédie grecque. Elles sont simplement reliées sans copie, suppression, fusion ou résumé de remplacement.

## Quatre documents publics conservés à leur adresse originale

| Étude universitaire existante | URL canonique | Caractères HTML | Empreinte Git blob | Rubrique primaire |
| --- | --- | ---: | --- | --- |
| Levant ancien : Ougarit, Phénicie et royaumes araméens | `/bibliotheque-mythologies-du-monde/civilisations-histoire-levant-pheniciens/` | 23839 | `929ae956069238cda330ee7a9b6a6ada20210c5b` | Sources anciennes |
| Carthage : histoire punique, Tanit et débats sur le tophet | `/bibliotheque-mythologies-du-monde/civilisations-carthage-punique-histoire-religion/` | 22752 | `83b21f56697b01c4e008dde6e0ca660dc74838dc` | Sources anciennes |
| Tartessos : Turuñuelo et contacts méditerranéens | `/bibliotheque-mythologies-du-monde/civilisations-tartessos-turunuelo/` | 21334 | `a9b6741335196e302b3109e2c44f37fee700912e` | Sources anciennes |
| Méditerranée des échanges : Étrusques, Tartessos et Mycéniens | `/bibliotheque-mythologies-du-monde/mythos-mediterranee-ecritures-char-bronze-etrusques-tartessos-myceniens/` | 13984 | `d3f18ab081a1c5f41039307c1cbc8999aa130bd1` | Interprétations philosophiques |

La lecture directe des pages confirme leurs développements universitaires, leurs sous-sections et leurs références. Ces documents précèdent cette intervention : **le nouveau rattachement est une intégration au catalogue grec, pas une première publication**.

Le parcours confronte l'alphabet phénicien et son histoire, les témoignages grecs et latins sur Carthage, les vestiges tartessiens du Sud-Ouest ibérique, ainsi que les pratiques d'écriture du monde mycénien. Il distingue les époques, les langues et les catégories de preuve ; les ressemblances ne démontrent pas une filiation religieuse uniforme.

## Changements de génération, de navigation et de design

- `scripts/build_greek_corpus.py` : quatre nouveaux liens dans les lectures documentaires de l'entrée unique `/mythologie-grecque/`.
- `scripts/build_greek_folders.py` : quatre sous-dossiers thématiques précis, fils d'Ariane vers l'ancre exacte du sous-dossier et panneau **« Méditerranée des échanges : écritures, sources et contacts »** ; trois liens par étude, soit **12 liens dirigés**.
- `assets/mythos-museum.css` : panneau anthracite, accent or, liens tactiles de 44 pixels via la feuille commune, grille d'une colonne sous 700 pixels et adaptation sous 480 pixels.
- `tests/test_greek_mediterranean_crossreadings_20261105.py` : sources intégrales présentes, unicité des URLs, classement par sujet, conservation des articles après deux reconstructions, retour ancré et 12 liens réciproques sans duplication.

Les panneaux sont injectés **hors des articles**, à partir des publications originales sans changer les textes, les sources et les bibliographies. La bannière noire et dorée avec statue et temple, les images documentaires existantes et les archives sont préservées. Aucune ancienne image 2,5D n'est introduite.

## Publication : vérifications nécessaires

Ne pas assimiler un commit source à un déploiement public. Contrôler successivement : tests GitHub Actions ; génération du site ; présence des quatre destinations et des liens croisés ; reçu `/catalog/publication-verification.json` ; et accessibilité HTTPS des pages. Les dernières validations observées étaient encore en cours avec plusieurs reconstructions concurrentes. Le dernier reçu consultable dans le dépôt correspondait à une version antérieure (1 455 documents, 27 archives, 110 médias).

Aucun registre éditorial, manuscrit numéroté, archive, planification ou automatisation horaire MYTHOS n'est modifié.
