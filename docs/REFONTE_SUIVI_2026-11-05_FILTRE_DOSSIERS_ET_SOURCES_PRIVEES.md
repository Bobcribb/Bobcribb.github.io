# MYTHOS — Refonte des dossiers : filtre local, index préservé, sources examinées

**Date :** 5 novembre 2026. Dépôt : `Bobcribb/Bobcribb.github.io`, `main`. Relecture avant intervention de `AGENTS.md` et de `docs/PUBLICATION_CONCURRENTE.md`.

## Recherche documentaire : aucune publication intégrale nouvelle attribuée à cette séance

L'étude **La Galigo**, issue du brouillon WordPress 1151, est déjà restaurée intégralement sous `/bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/` : sa page source contient **52 355 caractères HTML** au contrôle, ses ancres et sa bibliographie sont présentes. Un nouvel import aurait été un doublon.

L'inventaire privé Google Docs `MYTHOS — LIRE EN PREMIER — index et contrôle des 135 brouillons` couvre **134 brouillons de pages et un article** dans 15 volumes. Il porte l'instruction documentaire explicite **« Ne pas publier ces documents sur GitHub »**. Cette protection est respectée : aucun de ces contenus privés n'est transféré au dépôt public sans validation éditoriale, et ils ne peuvent pas être considérés comme des manuscrits publics approuvés sur le seul critère de leur longueur.

Les autres manuscrits de travail approuvés accessibles sont déjà soumis dans `editorial/inbox/` ; leur attribution et leur déploiement relèvent du workflow transactionnel. Un échec CI récent signalait **MC-069** ; il a été traité par un commit concurrent `5cc2a5af69e215f5b4f3e5b5e618719622a65842`, qui réserve désormais l'identité historique **MC-071** à la monographie distincte sur les scribes divins, sans suppression de source. La validation finale du workflow est à contrôler et ne doit pas être présumée.

**Bilan d'intégration universitaire nouvelle de cette intervention : 0.** Motif vérifiable : documents candidats déjà publiés, déjà déposés en file, ou expressément conservés comme brouillons privés. Aucun numéro, UUID, manuscrit ni archive n'a été modifié.

## Intervention effective sur le site

Les **huit dossiers thématiques** de `/mythologie-grecque/dossiers/` reçoivent un outil de **filtrage local** des textes intégraux et des sections des livres. Il permet la recherche immédiate par auteur, titre, nom divin, sanctuaire ou thème, sans déplacement d'un article ni altération des sources :

- `scripts/build_greek_folders.py` ajoute un champ de recherche accessible, un bouton d'effacement et un compteur annoncé aux lecteurs d'écran, tout en maintenant les sommaires ancrés des sous-dossiers.
- `assets/greek-folder-filter.js` fournit une recherche multi-termes insensible aux accents, affiche ou masque les seules entrées HTML du sommaire et ajuste la liste des sous-dossiers visibles. La touche Échap efface la recherche. Les liens directs vers un sous-dossier réaffichent le catalogue si nécessaire. Sans JavaScript, le catalogue reste complet et immédiatement consultable.
- `assets/mythos-museum.css` apporte un bloc anthracite et or, des commandes tactiles d'au moins **48 pixels**, un rendu sur une colonne sous 480 pixels, une annonce lisible des résultats et l'impression de la liste complète.
- `tests/test_greek_folder_filter_20261105.py` vérifie qu'après **deux générations successives** les textes originaux sont identiques, les URL intégrales uniques, les ancres de sommaire valides, les filtres présents sans duplication et les styles responsive établis.

Les huit familles, leurs cotes, renvois réciproques, la bannière photo avec statue grecque et temple, les sommaires et images existants, les 27 archives de `Origines du sacré` et les publications des autres rubriques restent inchangés. Aucun SVG 2,5D n'est réintroduit.

## Vérification et statut

Pour cette intervention, les modifications de fichiers sont atomisées en un seul commit sans forçage de la branche. Le script est servi comme ressource statique de `assets/` par `scripts/build_native.py`. La validation finale requiert la réussite des workflows GitHub, une régénération complète, la lecture de `/catalog/publication-verification.json` et la vérification du filtre sur `https://bobmythos.fr/mythologie-grecque/dossiers/sources-anciennes/`.

Aucun fichier `editorial/numbering.json`, `editorial/holds.json`, manuscrit universitaire, archive ou automatisation MYTHOS n'est modifié.
