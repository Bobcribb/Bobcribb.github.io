# MYTHOS — Refonte : traçabilité des neuf tomes historiques ODS

**Date du contrôle : 6 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`. Les règles `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md` et `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md` ont été relues avant toute intervention. L'ensemble des numéros, des manuscrits et des planifications reste inchangé.

## 1. Vérification des contenus et des doublons

**Nouvelle monographie universitaire publiée lors de cette séance : aucune (0).** Le contrôle a porté sur les sources accessibles de `corpus/origines-du-sacre/`, `corpus/mythologie-grecque/archives/`, `corpus/theatre-grec/comedies/`, `corpus/philosophie/eneide/`, `editorial/inbox/`, `editorial/archives/` et la documentation de publication. Les neuf archives historiques ODS des tomes XXV à XXXIII, ainsi que l'étude *La Galigo*, avaient déjà un lecteur HTML public dans GitHub. Leur publication ne doit pas être annoncée une seconde fois.

L'étude « Iran et Inde : Mithra, Varuṇa, ṛta et vérité de la parole » sous la cote historique 487 est présente à `corpus/origines-du-sacre/chapitre-487-iran-inde-mithra-rta-satya.md`, mais ce texte est **strictement identique**, blob Git `70d6aef3fcdecb993f6c2d3bbd7d52969821d9a3`, au manuscrit canonique `chapitres/origines-du-sacre/487-iran-inde-mithra-rta-satya.md`. Il ne constitue donc pas un nouvel inédit à soumettre.

Les sauvegardes WordPress sur Google Drive contiennent des **brouillons privés** : le protocole éditorial interdit de les transférer automatiquement dans le dépôt public sans examen et approbation individuels. Les autres études déjà présentes dans `editorial/inbox/` relèvent du mécanisme transactionnel d'attribution ; aucun nouvel UUID, slug ou numéro n'a été créé pour les redéposer. Sur le périmètre exploré, aucun texte nouveau à la fois **intégral, approuvé, distinct et absent du circuit de publication** n'a pu être retenu.

## 2. Amélioration effectivement inscrite dans main

Neuf lecteurs existants `/corpus/origines-du-sacre/conv-tome-XXV...XXXIII...` (dont le tome XXVIII : `tome-XXVIII-chapitres-363-370`) disposent, après la prochaine reconstruction, d'une navigation documentaire à deux choix : **retour au sommaire** et **accès direct à l'original Markdown conservé sur GitHub**. L'URL source est dérivée de l'identifiant réel de chaque manuscrit, sans chemin inventé ni copie du texte. La page d'index explique maintenant la présence de ces sources consultables.

Le traitement `scripts/origins_archive_navigation.py` vérifie toujours les neuf couples source/lecteur, leur longueur, la bibliographie et les références ; il conserve strictement le texte de la section `main` de chaque lecteur lors de l'ajout de navigation. Les changements ne portent que sur le rendu issu de `_site`, non sur les éditions scientifiques archivées.

`assets/mythos-museum.css` améliore les deux liens (cibles d'au moins 44 pixels, contraste noir/or, focus clavier, retour à la ligne sur petit écran, colonne unique sous 540 pixels, exclusion de la navigation à l'impression). La bannière statue grecque à gauche et temple à droite, les collections, les images documentaires, les bibliographies et la numérotation restent intactes. Aucun visuel 2,5D n'est introduit.

Le test `tests/test_origins_archival_shelf_20261106.py` exige désormais une et une seule URL source Markdown exacte pour chacun des neuf lecteurs, avec vérification de `rel="noopener noreferrer"`, absence de doublons au second rendu et comparaison de l'intégralité du texte principal avant/après.

## 3. Commits et contrôles de publication

Commits enregistrés sur `main` au moment de la séance :

- `4098ea3a3af5376867c1d28733da887f85457b11` — liens vers les neuf manuscrits sources.
- `a6d88643a1569b7c93d2bf7ddf5f903539eee879` — garde de régression.
- `942e21624273701e37b80f577e59946e459e7402` — mise en page accessible et responsive.
- `df40f986bb64952815d3ac2eeafd81b397ef4149` — libellés documentaires et sommaire.

**Constats publics distincts des commits :** le portail `https://bobmythos.fr/origines-du-sacre/` et le lecteur `https://bobmythos.fr/corpus/origines-du-sacre/conv-tome-XXV-chapitres-339-346.html` ont été consultés en HTTPS ; ils présentaient déjà les neuf archives et le retour au sommaire, **mais pas encore le nouveau lien Markdown**. Le manifeste `https://bobmythos.fr/catalog/publication-verification.json` annonçait alors `source_commit=db016f6cbc0bec783e369a1e2874f0c6a1883aa6`, `github_run_id=42175517252`, 1 604 documents indexés, 27 archives, 110 médias. Le workflow `42175517252` a été vérifié dans GitHub Actions avec conclusion **success**, mais il est **antérieur** aux commits ci-dessus. Les publications déclenchées par les commits du présent contrôle étaient annulées/remplacées ou en attente de la publication suivante au dernier examen.

**Limite de vérification :** l'écriture sur GitHub est confirmée, mais ni le déploiement HTTPS de la nouvelle fonctionnalité ni l'exécution finale de la suite de tests ne sont encore établis. Pour conclure ultérieurement : contrôler un workflow GitHub Actions de publication terminé avec succès **postérieur** au commit de refonte, vérifier le `source_commit` public, et comparer dans chacun des neuf lecteurs les liens de retour, de source originale, et le texte scientifique conservé.

Aucune demande `editorial/inbox/`, aucun reçu `editorial/numbering.json`, aucun chapitre canonique, aucun manuscrit ancien ni aucune automatisation MYTHOS n'a été modifié.
