# MYTHOS — Refonte du 5 novembre 2026 : Bactriane, Gandhara et Palmyre

**Dépôt** `Bobcribb/Bobcribb.github.io`, branche `main`.

## Préconditions et état de publication

Les fichiers `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus. Au début du contrôle, `main` contenait 354 soumissions JSON dans `editorial/inbox`, 331 attributions dans le registre et cinq retenues explicites. Le blocage de la validation datant d'une révision antérieure concernait `MC-069` : deux identités historiques concurrentes. Une révision ultérieure, `5cc2a5af69e215f5b4f3e5b5e618719622a65842`, a réconcilié la soumission sur les scribes comme `MC-071`. Les dernières validations de génération restaient en cours au moment de la préparation de ce rapport ; les travaux concurrents ne sont pas modifiés ici.

**Aucune première publication de manuscrit inédit** : les nouvelles monographies numérotées accessibles étaient déjà soumises sous des UUID immuables à GitHub Actions. Aucun nouveau fichier numéroté, UUID, attribué ou publié n'est annoncé. Les brouillons privés WordPress ne sont pas importés.

## Intégration au catalogue grec de deux études publiques intégrales

Les trois études ci-dessous existaient sous `/bibliotheque-mythologies-du-monde/`, mais seules les deux dernières étaient absentes des lectures associées de l'encyclopédie grecque :

| Texte intégral vérifié | Taille HTML | SHA Git source | Statut |
| --- | ---: | --- | --- |
| Royaumes gréco-bactriens et indo-grecs | 14630 caractères | `c9bba6d4ee082899ef66e448a94377b7aa677309` | Déjà classé dans le catalogue grec |
| Empire kouchan : Gandhara, monnaies et langues | 25560 caractères | `5a10039f77ded767e0ba069fd48799faf6ec5377` | Nouvel accès dans le catalogue grec |
| Palmyre : Zénobie, inscriptions grecques et araméennes | 27094 caractères | `b9b4d92ca1f87876bdcd13dc6ef965750a9df718` | Nouvel accès dans le catalogue grec |

La lecture des articles originaux confirme leurs sections scientifiques, références et bibliographies. Les documents restent à leurs adresses d'origine sans fusion, copie, suppression ou remplacement par un résumé. L'association thématique distingue les États gréco-bactriens (époque hellénistique), les pouvoirs kouchans et la cité caravanienne de Palmyre (époque romaine). Une écriture grecque ou une forme iconographique ne suffit pas à démontrer une identité politique et cultuelle.

## Navigation, graphisme et tests

- `scripts/build_greek_corpus.py` : deux nouvelles références vers les pages intégrales du Gandhara et de Palmyre.
- `scripts/build_greek_folders.py` : classements précis dans **Sources anciennes** : Bactriane–Gandhara / inscriptions et monnaies ; Palmyre / grec, araméen, pratiques cultuelles. Le dossier gréco-bactrien conserve sa classification. Trois panneaux réciproques, **six liens dirigés**, et retours vers les sous-dossiers.
- `assets/mythos-museum.css` : panneau anthracite et accent doré, grille responsive, liens avec retours à la ligne et renforcement de la lisibilité sous 480 px. La bannière statue grecque–temple et les cartes iconographiques sourcées sont préservées.
- `tests/test_greek_eastern_hellenistic_connections_20261105.py` : conservation des sources, classement unique, réciprocité des liens, ancres exactes et idempotence après deux reconstructions.

Le nouveau parcours est placé **hors du texte universitaire** et n'attribue aucune nouvelle cote historique.

## Contrôle de déploiement attendu

La présence du commit dans GitHub ne prouve pas sa publication. Il faut constater la réussite du workflow, la mise à jour du reçu `/catalog/publication-verification.json` et la présence des pages HTTPS avec leur navigation. Tant que ces trois conditions ne sont pas vérifiées, le déploiement public reste non confirmé.

Aucune autre automatisation MYTHOS ni aucune planification horaire n'est modifiée.
