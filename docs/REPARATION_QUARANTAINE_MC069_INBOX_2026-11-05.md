# MYTHOS — Quarantaine réversible d'une demande non UUID (MC-069, souffle des dieux)

**5 novembre 2026 — réparation du circuit de publication.**

## Blocage constaté

Les exécutions GitHub Actions de validation [41999863047](https://github.com/Bobcribb/Bobcribb.github.io/actions/runs/41999863047) et [41999628760](https://github.com/Bobcribb/Bobcribb.github.io/actions/runs/41999628760) s'interrompaient à `scripts/editorial_queue.py apply`, avant l'allocation du moindre manuscrit, sur `ValueError: badly formed hexadecimal UUID string`.

Le fichier incriminé est `editorial/inbox/20261105-mc-069-souffle-vent-vie-philologie.json`. Il possède un **nom non conforme à la règle UUID**, mais contient une étude scientifique intégrale de **91 145 caractères Markdown** (95 134 octets JSON UTF-8), intitulée « Quand les dieux respirent : souffle créateur, vents divins, principe vital, parole et mortalité ». Son identifiant historique déclaré est **MC-069**, cote revendiquée par une autre soumission valide `5ed94532-0216-4cf3-ae69-2390d43b0069` (« Quand les dieux changent de nom »). Ce sont deux études distinctes : ne pas les fusionner ni supprimer.

## Intervention limitée et vérifiable

Dans `scripts/editorial_queue.py`, ajouter **uniquement ce chemin** à `QUARANTINED_INVALID_REQUESTS` et verrouiller son contenu par l'empreinte **SHA-256 `7e2f4608940e2ba64b76d0970c7e18c7f1a966eff2e99fcfaad09ee32bb0f85c`**. Un contrôle indépendant du calcul UTF-8 a été comparé à l'empreinte d'une retenue existante. Si le texte change, le traitement doit s'arrêter ; si le texte reste identique, le programme signale l'attente et laisse passer les autres soumissions valides.

**Ni suppression ni renommage ni nouvel UUID de substitution.** Aucun numéro canonique, source déjà publiée, reçu, registre historique, sommaire, lien, média, style ni automatisation horaire n'est modifié par le correctif. L'étude et ses références restent intégralement récupérables sous leur chemin d'origine. La réconciliation future de son identité historique nécessitera une décision éditoriale indépendante (MC-069 est occupé), pas une attribution opportuniste.

Le test de non-régression `test_non_uuid_mc069_request_is_hash_locked_and_kept_without_blocking_queue` vérifie la présence, l'empreinte, l'intégrité du manuscrit, le passage d'une autre demande légitime et le refus d'une mutation de l'objet quarantainé.

## Reprise de la publication

Après fusion, laisser le workflow `scripts/publish_site.py` relire `main` et attribuer les numéros uniquement par sa transaction canonique. Les manuscrits résolus **MC-070** et **MC-071**, leurs UUID originaux `3d64880f-6844-4d2a-b94e-b7ea3a2a0460` et `904ece0d-5591-4e6b-bfea-e39e7143c4c1`, restent publiables, sans revenir aux anciennes cotes MC-046 et MC-042. Les reçus d'attribution, les nouveaux fichiers sources, la reconstruction, le catalogue, le sitemap, les liens et la page publique doivent être contrôlés après réussite du workflow. Les autres retenues restent en place.
