# MYTHOS — Réconciliation éditoriale MC-077 / MC-078 et reprise des publications

**Date :** 5 novembre 2026. **Dépôt :** `Bobcribb/Bobcribb.github.io`, branche `main`.

## Incident constaté

Les validations GitHub Actions `42024892503` (générateur) et `42024892285` (audit), entre autres, échouaient à l'étape `python scripts/editorial_queue.py apply` sur `Collision d’identifiant historique non réconciliée : MC-077`.

Deux études intégrales approuvées, d'objets distincts, avaient revendiqué la même identité historique :

1. `9e762fc3-2e15-4d58-832a-7b01cb9bd077` — « Le parfum du sacré : fumées, résines, encens et offrandes divines », manuscrit de 71 427 caractères Markdown, introduit dans `main` au commit `678068cd4a6b656bdb756c47cc213c5920b01790` à **12:07:37 UTC**. Conserve **MC-077**.
2. `1d8b9a77-c1e5-4b55-9d77-202611050077` — « Entraver les immortels : chaînes, filets et captivité divine », manuscrit de 62 163 caractères Markdown, commit `ba3d78d4b0db10c0151089790583d68ba7938def` à **12:09:19 UTC**. La priorité chronologique lui interdit une deuxième attribution MC-077.

Une autre intervention a déjà protégé le second manuscrit sous `editorial/holds.json`, avec l'empreinte exacte `b677888768c94847d77840756f8c222384814adc26c78a3d2434e1dde90aa2a6`. **Ne pas modifier cette attente ni son fichier historique.**

## Intervention de réconciliation

Après lecture du registre `editorial/numbering.json`, des chapitres existants et des demandes non attribuées, aucune identité MC-078 n'était présente lors du contrôle.

La présente intervention dépose une **nouvelle demande distincte** :

- `editorial/inbox/c8de648c-1dc3-4de3-8ac6-202611050078.json` ;
- collection `comparatif` ;
- titre scientifique : **MC-078 — Entraver les immortels : chaînes, filets, captivité divine et limites de la souveraineté, de l'Olympe à Babylone** ;
- slug `mc-078-entraver-les-immortels-chaines-filets-captivite-divine-souverainete` ;
- 62 538 caractères Markdown après la rectification de trois passages d'identité et de continuité ; aucune section, citation, bibliographie ou scène n'est supprimée.

Les remplacements se limitent au titre MC-077 → MC-078, à la mention de l'identité historique et à la phrase d'antériorité, initialement erronée, qui reconnaît maintenant la première demande. Toutes les autres parties doivent être **identiques octet pour octet après neutralisation de ces remplacements précis**. Le fichier d'origine et sa retenue restent intacts, pour traçabilité.

`{{volume}}` et `{{numero}}` demeurent non résolus : aucun numéro canonique n'est choisi ici. L'attribution atomique, le reçu, le rendu et les contrôles de publication restent exclusivement de la compétence de GitHub Actions, suivant `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`.

## Tests de non-régression

`tests/test_mc077_mc078_reconciliation_20261105.py` vérifie :

- l'empreinte SHA-256 de l'ancien manuscrit et sa présence en attente ;
- la priorité de la première demande MC-077 ;
- l'identité MC-078 dans la seule demande réconciliée ;
- l'absence de numéro canonique réservé ;
- l'intégralité du texte par comparaison exacte avec le manuscrit initial, après trois remplacements délimités ;
- la conservation des dernières sections et de la bibliographie.

## Contrôles de mise en ligne encore nécessaires

La création de la demande ne constitue **pas** une publication. Avant d'annoncer une mise en ligne, contrôler : le reçu `editorial/numbering.json` pour ce nouvel UUID ; `scripts/build_native.py` ; `scripts/verify_publication.py` ; le workflow GitHub Pages ; la nouvelle URL HTTPS, ses 88 sections, ses sources et sa bibliographie ; les liens et le manifeste public `/catalog/publication-verification.json`. Les sorties des Actions doivent être relues après chaque conflit concurrent.

Le contenu du dépôt, les images photoréalistes, la charte noir et or, les manuscrits et archives historiques, les numéros reçus et **toutes les planifications horaires MYTHOS** restent inchangés en dehors du nouveau dossier transactionnel et de ses tests.
