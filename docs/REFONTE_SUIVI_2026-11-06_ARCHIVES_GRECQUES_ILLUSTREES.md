# MYTHOS — Archives grecques illustrées et navigation réciproque

Contrôle éditorial : 6 novembre 2026. Base de cette intervention : `d34278be7d41fcd4dbb5dba29023d3d6bf534efd`.
Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`.

## Inventaire et statut scientifique

Lecture de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` avant toute écriture. Le portail `mythologie-grecque/index.html` comporte déjà 14 liens vers des lecteurs historiques sous `corpus/mythologie-grecque/archives/` : ils ne doivent pas être redéposés ni renumérotés. Les archives Héraclès, Troie et Odyssée figurent dans cet inventaire. Les lecteurs d'Héraclès et de l'Odyssée ont été relus par l'API GitHub (titre, sections, bibliographie). La présence de Troie est établie par l'arbre Git, ainsi que ses liens déjà publiés.

Aucune première publication universitaire n'est revendiquée : les volumes contrôlés sont déjà présents. Les autres manuscrits numérotés doivent passer par leur UUID `editorial/inbox/` et leur reçu GitHub Actions. Les brouillons privés de Google Drive ne sont pas transférés sans validation de leur statut éditorial.

## Refonte et sources iconographiques

- Trois entrées existantes de la liste `#grec-archives` sont enrichies directement, sans nouvelle URL ni duplicata : Héraclès, Troie et Odyssée.
- Les images JPG déjà présentes dans `media/2026/10/` proviennent du Metropolitan Museum of Art, respectivement objets 06.1021.66, 56.171.29 et 09.182.50. Les sujets, datations, limites d'interprétation et liens vers les notices officielles proviennent du catalogue `scripts/editorial_media.json`. Reproductions Open Access (CC0).
- Une illustration n'apparaît que si son archive et son média existent dans le répertoire de publication. Le texte des 14 liens et les sources universitaires d'origine ne changent pas.
- Un lien de retour accessible depuis chacun des lecteurs historiques d'archives vers `/mythologie-grecque/#grec-archives` est créé uniquement dans la copie HTML reconstruite du site ; aucun fichier source d'archive n'est réécrit.
- La charte musée noir, or et ivoire, la bannière statue grecque / temple, la navigation unique de l'encyclopédie, les cartes responsives (mobile) et les repères de focus clavier sont conservés.

## Contrôle et limites

Le test `tests/test_greek_archive_cards_and_return_20261106.py` vérifie les trois images, leurs six liens documentaires, le maintien des URL originales, l'idempotence, le refus des liens manquants, le retour réciproque et la conservation octet par octet des faux manuscrits de test.

L'accès HTTPS direct à `bobmythos.fr` n'a pas été possible pendant cette intervention : la recherche Web retourne une erreur et l'outil navigateur externe a atteint son quota. **Ni la publication effective ni le rendu smartphone ne sont prétendus vérifiés**. Il faudra confirmer une exécution GitHub Pages réussie puis le manifeste public et les lecteurs concernés.

Ni `editorial/numbering.json`, ni `editorial/inbox/`, ni un workflow ou une planification horaire ne sont modifiés.
