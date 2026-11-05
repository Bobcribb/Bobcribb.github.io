# MYTHOS — Lycie, Commagène, Bactriane : rattachements universitaires
**Contrôle initial : 5 novembre 2026, 05:54 UTC.** Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`, révision initiale `2ea76cd8c4a8e3fb0e200ed7072a397802044f96`.

## Contrôle de publication
Les consignes `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été lues sur la branche principale avant modification. La file publique contenait 324 demandes JSON à la date du contrôle. Le registre de numérotation contenait 319 attributions (origines-du-sacre 68, encyclopedie 73, comedies 46, tragedies 46, comparatif 86), laissant 5 retenues documentaires : aucun manuscrit approuvé supplémentaire non attribué n'a été établi lors de cet examen. Aucun UUID ni numéro n'est inventé.

## Trois études universitaires intégrales retrouvées dans les archives publiques
Les trois ouvrages sont **déjà publiés** dans `Bibliothèque des mythologies du monde / Civilisations` ; leur texte HTML complet, les sections, les sources et les bibliographies ont été inspectés. Ils étaient absents de la collection de liens `RELATED` du catalogue grec avant intervention. Ils deviennent consultables depuis ce catalogue sans altération ni duplication de leur article.

| Étude | Ancien chemin conservé | Blob Git initial |
|---|---|---|
| Lycie, Xanthos et Létoon | `/bibliotheque-mythologies-du-monde/civilisations-lycie-xanthos-letoon/` | `0bcf1e10be61d8348ab50b1613caacdd82cc1967` |
| Commagène, Antiochos Ier et Nemrut Dağ | `/bibliotheque-mythologies-du-monde/civilisations-commagene-antiochos-nemrut/` | `79f02cbecd98edfa9563c49a1c9c412d203c87f8` |
| Royaumes gréco-bactriens et indo-grecs | `/bibliotheque-mythologies-du-monde/civilisations-royaumes-greco-bactriens-indo-grecs/` | `a69fca5738dfc17f9811cbce63eb6add3b3afe14` |

Le sanctuaire lycien est classé sous Cultes et sanctuaires / Létoon, Commagène sous Cultes et sanctuaires / Nemrut Dağ, les royaumes gréco-bactriens sous Sources anciennes / monnaies et échanges. Pergame est maintenu à sa cote et son chemin existants.

## Liens, charte graphique et contrôles
Quatre études originales (Lycie, Commagène, Pergame, Bactriane) forment un nouveau parcours documentaire de 12 renvois réciproques au total, en panneaux **hors article**. Les pratiques religieuses et les époques ne sont pas confondues. Les sommaires, retours aux sous-dossiers et liens du catalogue sont reconstruits automatiquement.

La charte muséale noir, ivoire et or est conservée. Le parcours bénéficie d'une typographie et d'un encadrement dorés, d'une grille responsive à une colonne sous 700 px, d'un traitement des libellés sous 480 px, de liens tactiles de 44 px et du focus clavier existant. Aucune image 2,5D n'est ajoutée.

Le nouveau test `test_hellenistic_contacts_integral_sources_classification_and_reciprocity` contrôle la présence des articles complets, leurs références, leur classement unique, la conservation de l'article avant/après deux reconstructions, le fil d'Ariane, l'absence de doublon, les trois liens réciproques et les styles communs.

**Statut au moment de la rédaction** : contrôle de sources et préparation des modifications. La publication publique sera confirmée seulement après la réussite du workflow et la consultation du reçu `/catalog/publication-verification.json` et des pages HTTPS. Les textes, registres, archives et autres automatisations sont inchangés.

## Commits et validation effective

- `2555432eac3bcdffb91229cfcebfeefbf0059e2d` : référencement des trois textes, quatre parcours réciproques, classement, style et tests, dans un seul commit atomique.
- `57f81890f4a4f2f4d3c99b1a107e1e8cc6e7461d` : correction du test obsolète des figures récentes. Celui-ci exigeait exactement 37 notices alors que 40 sont désormais documentées. La correction conserve l'exigence de présence des figures et ajoute un contrôle d'unicité des entrées.
- `2803e3247c05443dc3d01ab67368654a693bc8d8` : amélioration spécifique des titres et liens sur écran mobile, et déclenchement du workflow de publication (les changements CSS sont inclus par la liste de chemins GitHub Actions).

Contrôles effectués après écriture : `main` contient les modifications ; les trois fichiers HTML sources conservent leurs blobs originaux `0bcf1e10be61d8348ab50b1613caacdd82cc1967`, `79f02cbecd98edfa9563c49a1c9c412d203c87f8` et `a69fca5738dfc17f9811cbce63eb6add3b3afe14`.

Les tests unitaires du workflow de validation `41977532452` (correctif inclus) et ceux du workflow de publication `41977662548` ont franchi leur étape de vérification des régressions. Lors du dernier contrôle, la génération du site et la synchronisation se poursuivaient : **aucun succès de déploiement public ni nouveau reçu n'est encore revendiqué**. Reçu GitHub précédent : 1 443 documents indexés, 27 archives et 110 médias au commit source `9c0063cd9e4c229ed5a95c096d0ba8948de58dcf`.

Consulter les journaux : `https://github.com/Bobcribb/Bobcribb.github.io/actions/runs/41977532452` et `https://github.com/Bobcribb/Bobcribb.github.io/actions/runs/41977662548`. 
