# MYTHOS — Refonte : Arménie, Vahagn et David de Sassoun

**6 novembre 2026 — dossier de contrôle.** La source de vérité est la branche `main` de `Bobcribb/Bobcribb.github.io`. `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus avant écriture. Les cinq collections à numérotation atomique, leurs demandes, leurs reçus et leurs planifications sont inchangés.

## Manuscrit existant effectivement restitué

- **Identité :** Volume historique XIII — *Arménie : Vahagn, Anahit et l'épopée de David de Sassoun*.
- **Provenance :** sauvegarde WordPress MYTHOS, Google Drive privé « Brouillons sauvegardés — Volume 02 », entrée `1137`, ancien slug `mythos-volume-13-armenie-vahagn-david-sassoun`. Statut WordPress historique : `draft`.
- **Champ transféré :** uniquement le corps HTML scientifique de cette entrée, sélectionné dans le cadre de la demande de migration des contenus historiques. Aucune autre entrée ni métadonnée privée de la sauvegarde n'est transférée.
- **Chemin :** `bibliotheque-mythologies-du-monde/mythos-volume-13-armenie-vahagn-david-sassoun/index.html`.
- **Volume :** XIII est la cote historique de cette étude, conservée telle quelle. Ce dossier relève de `bibliotheque-mythologies-du-monde`, hors des cinq collections qui passent obligatoirement par `editorial/inbox/<uuid>.json`. Aucun numéro nouveau n'est créé.
- **Intégrité pré-écriture :** `47776` caractères du corps original ; `47776` caractères après retrait des seules 63 ancres de navigation ajoutées ; égalité stricte avant écriture. 20 sections H2 et 63 rubriques H2/H3 originales. Les notes bibliographiques, références UNESCO, sources, variantes et développements philosophiques restent dans le même ordre.
- **Déduplication :** recherches GitHub sur Sassoun, Vahagn/Anahit et le slug ; le chemin cible n'était pas présent dans `main` au contrôle. La publication doit être relue à nouveau après commit.

Le texte restauré conserve ses paragraphes originaux sans réécriture académique. Sa publication n'est pas une validation scientifique indépendante et ne transforme pas l'étude en édition critique de source antique.

## Navigation et présentation

1. Sommaire explicite de 20 grandes parties et 63 ancres, navigation dans les deux sens avec `/mythologies/` et `/civilisations/europe/`.
2. Carte du volume XIII sur les portails « Mythologies du monde » et « Europe » ; accès direct complémentaire depuis l'accueil, sans duplication du texte. Renvoi croisé avec le volume historique X sur le *Kalevala* et le volume XIX sur *La Galigo*.
3. Feuille muséale commune maintenue, bannière statue grecque–temple, fond noir, ivoire et or ; figure et légende adaptatives sur mobile, sommaire en une colonne à moins de 720 pixels, liens clavier visibles.
4. Illustration documentaire ajoutée **hors du corps original** : photographie par **Marcin Konsek**, 5 juin 2014, de la statue de **David de Sassoun** par **Yervand Kochar**, sculpture de 1959, Erevan. Source Wikimedia Commons : https://commons.wikimedia.org/wiki/File:2014_Erywa%C5%84,_Pomnik_Dawida_Sasu%C5%84skiego_(01).jpg. **Licence : CC BY-SA 4.0**, https://creativecommons.org/licenses/by-sa/4.0/. Il s'agit d'une sculpture moderne illustrant la réception, pas d'un objet antique ni d'une reconstitution 3D.

## Tests et publication

`tests/test_armenie_sassoun_integrity_20261106.py` contrôle l'intégrité du corpus, ses ancres, la présence des sources, le statut historique de la cote, les liens réciproques, les crédits de l'image et la stabilité de l'étude après la passe `apply_museum_design`.

**Contrôle HTTPS initial avant écriture :** `/catalog/publication-verification.json` portait toujours le commit `db016f6cbc0bec783e369a1e2874f0c6a1883aa6`. La page du *Kalevala* restaurée lors de l'intervention précédente répondait `404` et le portail `/mythologies/` affichait un ancien sommaire. Ni la disponibilité publique de cette nouvelle étude ni son intégration au site déployé ne doivent être affirmées sans vérification d'un workflow `publish.yml` réussi et d'une réponse HTTP 200 sur `https://bobmythos.fr/bibliotheque-mythologies-du-monde/mythos-volume-13-armenie-vahagn-david-sassoun/`.

**Aucune automatisation MYTHOS, archive existante, attribution ou registre éditorial n'est modifié par cet ensemble de changements.** La nouvelle branche `main` et les GitHub Actions peuvent évoluer concurremment : les états doivent être lus de nouveau après publication.
