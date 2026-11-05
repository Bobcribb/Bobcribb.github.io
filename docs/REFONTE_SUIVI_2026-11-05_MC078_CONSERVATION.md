# MYTHOS — Reprise de la refonte : collision MC-077 et conservation de MC-078

**Contrôle : 5 novembre 2026.** Site : https://bobmythos.fr. Source : `Bobcribb/Bobcribb.github.io`, branche `main`.

## Incident de publication confirmé

Plusieurs exécutions GitHub Actions échouaient dans `scripts/editorial_queue.py apply` avec `ValueError: Collision d’identifiant historique non réconciliée : MC-077`, notamment l'audit `42024892285` et la validation `42024892503`.

Les demandes approuvées en cause sont scientifiquement distinctes :

- `9e762fc3-2e15-4d58-832a-7b01cb9bd077` : **MC-077 — Le parfum du sacré**, créée à 12:07:37 UTC, commit `678068cd4a6b656bdb756c47cc213c5920b01790` ;
- `1d8b9a77-c1e5-4b55-9d77-202611050077` : **Entraver les immortels**, soumission initiale MC-077 créée à 12:09:19 UTC, commit `ba3d78d4b0db10c0151089790583d68ba7938def`.

Un autre chantier a résolu la collision sans suppression : le deuxième manuscrit, **62 163 caractères Markdown**, reste intact dans `editorial/inbox/` sous un blocage `editorial/holds.json`, lié à sa somme SHA-256 `b677888768c94847d77840756f8c222384814adc26c78a3d2434e1dde90aa2a6`. Un nouveau manuscrit intégral réconcilié est déjà présent sur `main` sous l'UUID `1e78cdda-fd79-4dd8-8ff6-202611050078`, identité **MC-078**, slug `mc-078-entraver-les-immortels-chaines-filets-captivite-divine-souverainete`. Il comporte **62 825 caractères Markdown**.

## Vérification de conservation réalisée

Comparaison des deux versions :

- **88 sections numérotées strictement identiques**, de la première à la synthèse épistémique finale ;
- **205 paragraphes historiques non éditoriaux conservés sans modification** ;
- les ajustements portent sur les titres/identifiants, la note qui établit l'antériorité de MC-077, et une correction documentée du cartel d'une photographie des musées du Vatican ;
- bibliographie, analyses, distinctions attestations/hypothèses, illustrations proposées et appareil philologique restent présents.

Le test `tests/test_mc078_preservation_20261105.py`, ajouté à `main`, empêche la modification silencieuse de l'original retenu, la perte des 88 sections, les suppressions dans les paragraphes scientifiques et une nouvelle collision MC-078 dans la file.

**Aucun doublon de MC-078 n'a été envoyé par ce chantier.** Une soumission redondante préparée sur une branche de travail a été retirée avant toute pull request ou fusion ; seul le manuscrit déjà présent sur `main` fait foi.

## Publication et navigation : points de contrôle

La présence du nouveau JSON ne prouve ni l'attribution du numéro canonique de volume ni la publication HTTPS. Le numéro est attribué par `editorial/numbering.json` uniquement dans le circuit transactionnel GitHub Actions.

Contrôles requis : reçu de l'UUID MC-078 dans le registre, exécution sans erreur du générateur et de l'audit, absence de doublons dans `search.json`, lien de l'étude intégrale dans les portails comparatifs, présence de ses 88 sections sur le lecteur public et `source_commit` à jour dans `/catalog/publication-verification.json`. Ne présenter une URL publique comme effectivement publiée qu'après vérification.

Les reconstitutions photoréalistes, les archives, la charte muséale noir et or, les manuscrits déjà attribués et les planifications horaires MYTHOS restent intégralement préservés. Aucun workflow ou horaire n'a été modifié par ce chantier.
