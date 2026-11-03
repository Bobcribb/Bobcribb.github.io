# MYTHOS — Refonte, contrôle documentaire du 4 novembre 2026

## Périmètre et méthode

Contrôle de la branche `main` du dépôt `Bobcribb/Bobcribb.github.io` avant toute intervention éditoriale : `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` lus en priorité. Inventaires examinés : `editorial/inbox/`, `chapitres/` (collections `encyclopedie`, `tragedies`, `comparatif`, `grece`), `corpus/mythologie-grecque/`, `corpus/theatre-grec/comedies/`, `corpus/origines-du-sacre/`, `contenus/philosophie/`, `corpus/REGISTRE-INTEGRATIONS.md`, `corpus/mythologie-grecque/REGISTRE-RECUPERATION.md` et `docs/CATALOGUE_GREC_2026-11-04.md`.

Ce contrôle est **un inventaire ciblé, non une collation de l'ensemble des manuscrits**. Les fichiers Markdown universitaires déjà présents dans `chapitres/` ont des chemins de publication ; leur présence ne justifie pas une seconde copie. Les volumes conversationnels des *Origines du sacré* XXV–XXXIII ont déjà des archives Markdown et des pages de lecture dans `corpus/origines-du-sacre/` ; les republier comme un chapitre inédit créerait un doublon. Les dossiers de théâtre récupérés disposent déjà de leur source intégrale et de leurs deux lecteurs (analyse / scènes modernes).

## Textes recherchés mais non publiables à l'issue du contrôle

- **Chiron**, volume historique XXVII, chapitre 118, et sa suite 119–133 : mentionnés dans `corpus/mythologie-grecque/REGISTRE-RECUPERATION.md`, mais le manuscrit intégral source n'a pas été retrouvé dans les emplacements accessibles inspectés. Aucun chapitre recomposé n'a été ajouté.
- **Série historique 218–224**, Nyx à Hypnos/Thanatos/Némésis/Moires : un index de référence est conservé dans `corpus/mythologie-grecque/05-sources-et-variantes/index-historique-216-224.md`, **sans les textes universitaires intégraux correspondants**. Aucune publication de substitution.
- **Homère et Hésiode** : `contenus/philosophie/homere-hesiode-dossier-preparatoire.md` est un document préparatoire, et non trois monographies intégrales inédites. Les trois pages de philosophie existantes sont conservées, sans double publication.
- **Archives privées** : l'existence de sauvegardes de brouillons sur Drive ne constitue pas un feu vert de publication. Le protocole du dépôt impose de ne pas les rendre publiques sans validation explicite de leur statut éditorial.

Les demandes déjà enregistrées dans `editorial/inbox/` conservent leur UUID. Aucun numéro n'a été attribué ou réservé manuellement, et aucun registre de numérotation n'a été modifié.

## Modification concrète du graphisme

`assets/mythos-museum.css`, commit `bfe02fff0f49e2894f403e93993d9372076cdb0d` :

- sommaires universitaires centrés comme blocs, titres de sommaire centrés, lignes de références toujours alignées pour faciliter la lecture ;
- navigation du menu mobile contrainte à la fenêtre visible, avec défilement interne ;
- cartes des collections et des tomes sur une colonne sous 420 px, visuels conservés et lisibilité améliorée ;
- foyers clavier visibles sur les cartes, liens longs sans débordement et colonnes de lecture resserrées.

Le bandeau musée noir et or, avec statue à gauche et temple à droite, et l'ensemble des ressources iconographiques existantes sont préservés. Ce correctif CSS **ne modifie aucun manuscrit, aucune cote, aucun paragraphe, aucune image ni aucune automatisation horaire**.

## Vérification et limites

Contrôle effectué après la modification : `assets/mythos-museum.css` relu depuis `main`, empreinte Git `acb3c754361701f25c6a3dc286481bf9724689f7` ; bloc responsive et accolades contrôlés. Les workflows GitHub Actions de publication et d'audit étaient encore en cours au moment de cette relecture. Une réussite de commit n'est **pas** une preuve d'un déploiement public.

Contrôles de livraison recommandés : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, `python scripts/verify_museum_design.py`, puis consultation HTTPS de l'accueil et de lecteurs représentatifs sur mobile et ordinateur. Lorsque le réseau externe n'est pas consultable, le résultat des workflows et les pages publiques doivent rester distingués.

## Règle pour les intégrations ultérieures

Pour les cinq collections numérotées, déposer seulement le manuscrit approuvé, intégral et vérifié dans `editorial/inbox/<uuid>.json`, avec `{{numero}}` ou `{{volume}}`. Le traitement GitHub Actions seul attribue le prochain numéro et produit un reçu ; aucune création manuelle dans `chapitres/` ni modification du registre. Conserver le même UUID si une écriture est incertaine.