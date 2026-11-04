# MYTHOS — Refonte, garde MC-042 et hygiène HTML
**Séance :** 4 novembre 2026, début d'après-midi (heure de Paris).

## Règles lues avant toute modification

- Dépôt de référence : `Bobcribb/Bobcribb.github.io`, branche `main`.
- Documents vérifiés : `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`.
- Pour les cinq collections numérotées, seuls les manuscrits publics approuvés placés dans `editorial/inbox/<uuid>.json` peuvent être numérotés par GitHub Actions, avec attribution, source et reçu atomiques. Interdiction d'écrire directement dans `chapitres/` ou de modifier le registre d'attribution. Les numéros historiques MC sont distincts des numéros canoniques de volume.
- Les archives universitaires et les textes existants sont conservés ; aucun changement d'horaire ni d'autre automatisation.

## Diagnostic précis du blocage de publication

Les journaux des workflows GitHub Actions du 4 novembre, notamment `41830469905` et `41829777837`, montrent que `scripts/editorial_queue.py apply` échouait à `comparative_history.validate` avec :

```
ValueError: Collision d’identifiant historique non réconciliée : MC-042
```

Deux demandes publiques possèdent `MC-042` dans le titre du second niveau, **pour deux objets différents** :

1. **Demande antérieure :** `editorial/inbox/10b51d0c-5fc3-4acf-92b4-5b67b6b04242.json` ; collection `comparatif`, slug `mc-042-mesurer-le-sacre-poids-justes-balances-morts-etalon-justice-cosmique` ; étude `Mesurer le sacré : poids justes, balances des morts, étalons royaux et justice cosmique` ; 85 099 caractères de texte Markdown au contrôle. Création dans le commit `afe377c9fdac9e62ff8e43324016c06357c079cd` à **11:59:40 UTC** le 4 novembre ; correction ultérieure de détail documentaire à 12:00:25 UTC, sans création d'une seconde demande.
2. **Demande ultérieure :** `editorial/inbox/904ece0d-5591-4e6b-bfea-e39e7143c4c1.json` ; collection `comparatif`, slug `mc-042-qui-ecrit-pour-les-dieux-nisaba-nabu-thot-seshat-ecriture-et-autorite` ; étude `Qui écrit pour les dieux ? Nisaba, Nabû, Thot et Seshat` ; 62 938 caractères Markdown. Dépôt au commit `5f0d8e306f580d5dc5bb127969d55ab42b3db3f4` à **12:05:34 UTC**. Empreinte SHA-256 du JSON UTF-8 intégral (fichier conservé inchangé) : `cf2f1af13a6b7d8f9e2440b239444c582d75fcbff94e79db4da5c942f511dc45`.

### Décision prudente et réversible

Le fichier `editorial/holds.json` conserve maintenant la **seconde demande** sous son UUID et son SHA-256, avec un motif scientifique explicite. Cette opération n'efface aucune ligne du texte et ne lui attribue **aucun nouveau numéro**. La première étude, déposée antérieurement, reste admissible au parcours transactionnel normal.

Il faudra choisir une cote historique distincte pour l'étude Nisaba/Nabû/Thot/Seshat, sous contrôle éditorial, puis réconcilier sans réécrire ni réutiliser arbitrairement la demande d'origine. Les deux monographies ne doivent pas être fusionnées comme si elles portaient sur le même sujet.

Commit de correction : `ad7005406f0b741c2028e3ca223ab91e31c786fe`.

## État de la file au contrôle après correction

- **181** fichiers JSON présents dans `editorial/inbox/` (recensement des chemins sur `main`).
- **154** demandes disposant d'une attribution dans `editorial/numbering.json`, à la photographie du contrôle.
- **27** fichiers présents sans attribution ; parmi eux **4** retenus explicitement dans `editorial/holds.json`, **1** demande historique au nom UUID invalide conservée en quarantaine par `scripts/editorial_queue.py`, soit **22** autres demandes encore sans reçu et non bloquées par ces mécanismes précis.
- Ne pas déclarer ces 22 demandes « déployées » ou forcément toutes publiables tant que les contrôles GitHub Actions et HTTPS n'ont pas été réussis.

Aucune étude inédite supplémentaire n'a été déposée lors de cette intervention : les candidats intégraux accessibles sont **déjà enregistrés dans la file** ou déjà publiés, et leur réémission sous de nouveaux UUID ferait double emploi. Aucun brouillon WordPress privé n'a été exposé.

## Nettoyage du thème noir et or, sans changement scientifique

Une page publique telle que `religion/index.html` avait accumulé de nombreuses occurrences identiques de la classe CSS `mythos-chrome-label` sur un seul élément, par répétition du passage de `scripts/apply_museum_design.py`. Ce n'est pas une perte de texte, mais un défaut d'idempotence et une source d'HTML inutilement chargé.

Le générateur dédoublonne désormais les classes de ces étiquettes éditoriales, préservant leur style et leurs contenus. Une vérification de non-régression reproduit trois générations consécutives avec une page de sources grecques, et vérifie les paragraphes, les liens, le titre, l'étiquette et l'unicité du bandeau.

Commits :
- `076248e040538485af6e03ad6220553413084cae` — correctif du générateur.
- `970872ef852ef23ec0c87709e71067dbf5eb5220` — nouveau test `tests/test_museum_chrome_idempotence.py`.

La charte noire, ivoire et or, la bannière statue grecque / temple, les cartes illustrées et les images photoréalistes sont conservées. Aucune illustration 2,5D n'est réintroduite.

## Contrôles et preuves à distinguer

Au moment du contrôle intermédiaire, les commits étaient présents dans `main` et les exécutions Actions `41831190733` et `41831190919` traitaient encore la reconstruction. Les nouvelles exécutions ultérieures étaient en attente ou en cours. Le correctif de collision et le correctif HTML sont donc **enregistrés**, mais il faut vérifier séparément :
1. un reçu d'attribution pour la première demande MC-042 (l'UUID `10b51d0c-...`) dans le registre, avec son numéro canonique réel ;
2. le résultat de GitHub Actions incluant ce reçu ;
3. le commit source et l'exécution affichés dans `https://bobmythos.fr/catalog/publication-verification.json` ;
4. une page publique HTTPS contenant le manuscrit intégral et ses liens.

Aucun déploiement n'est annoncé sans ces contrôles. Aucune automatisation horaire MYTHOS n'a été modifiée.
