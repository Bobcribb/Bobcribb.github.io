# MYTHOS — Désamorçage du contrôle des dossiers grecs : notice Lindos

Date : 5 novembre 2026. Dépôt et branche : Bobcribb/Bobcribb.github.io, main.

## Erreur identifiée sur une véritable exécution de publication

La publication GitHub Actions n° 42026566748 (commit 9d8a57ffe..., journal horodaté à 12:32:43 UTC) a échoué dans `scripts/validate_publication.py` après le test `build_greek_corpus.verify()` avec :

```
AssertionError: Classement incomplet ou inattendu :
{'/mythologie-grecque/concordance-athena-lindia/'}
```

La notice est une concordance documentaire autonome, déjà conservée et accessible, entre deux monographies distinctes, 433 et 438. La validation `primary_folder_urls()` excluait correctement la notice du périmètre des affectations primaires, mais `build_greek_folders.inventory()` la réintroduisait en troisième destination éditoriale lorsque le catalogue associait un lien vers elle.

## Réparation sans perte

Le changement minimal de `inventory().add()` ignore seulement `LINDIA_NOTICE` dans l'affectation **primaire** des dossiers. Il ne supprime ni la notice HTML, ni les liens vers ses sources, ni sa présence dans la recherche et les sommaires généraux. La boîte `data-lindia-concordance="433-438"` continue à lier cette notice depuis le dossier des sanctuaires, et les chapitres 433 et 438 gardent leurs renvois et tous leurs textes.

Test ajouté dans `tests/test_lindia_concordance.py` : une entrée primaire 433, une primaire 438 et une notice secondaire doivent produire **exactement deux** affectations dans le même sous-dossier des cultes.

Cette réparation cible un bloqueur avéré et n'affaiblit pas le contrôle anti-doublon ; les autres destinations restent contrôlées par comparaison stricte. Aucun document numéroté, UUID, `editorial/numbering.json`, ancienne archive, contenu intégral ou automatisation MYTHOS n'est modifié.

## Statut

Cette modification doit encore passer le générateur complet sur GitHub Actions, puis un déploiement conclu par un manifeste public `source_commit` cohérent. Aucun déploiement ni nouveau chapitre attribué n'est annoncé avant ces confirmations.
