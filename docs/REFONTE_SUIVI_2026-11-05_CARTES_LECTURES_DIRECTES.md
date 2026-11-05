# MYTHOS — Cartes grecques avec accès directs aux études universitaires

Date : 5 novembre 2026. Dépôt : Bobcribb/Bobcribb.github.io, branche main.

## 1. Recherche de textes intégraux non publiés

AGENTS.md et docs/PUBLICATION_CONCURRENTE.md relus. Inventaire consulté :
editorial/inbox/, editorial/numbering.json, editorial/holds.json,
corpus/mythologie-grecque/archives/, corpus/theatre-grec/comedies/,
corpus/philosophie/eneide/ et recherche Google Drive « MYTHOS ».

Les études universitaires déjà visibles dans le portail, dont La Galigo, les
études théâtrales et les analyses de l’Énéide, ne doivent pas être dupliquées.
Les textes approuvés mais encore dans editorial/inbox/ attendent l’attribution
transactionnelle de GitHub Actions : aucun nouveau UUID ou numéro n’est créé.
Les 135 sauvegardes historiques WordPress sur Google Drive sont marquées
privées avec une interdiction explicite de transfert automatique sur GitHub.

**Premières publications supplémentaires vérifiées : 0.**
Motif : aucune source indépendante intégrale, approuvée, non publiée et
absente du circuit éditorial n’a été trouvée. Tous les manuscrits et archives
sont conservés sans modification, troncature ou substitution.

## 2. Modification fonctionnelle

scripts/build_greek_folders.py ajoute dans chaque carte illustrée de
/mythologie-grecque/dossiers/ au maximum trois accès directs distincts vers des
textes intégraux déjà répertoriés. Préférence à un chapitre universitaire,
puis un livre et une étude : aucun texte n’est recopié. Les lecteurs sont
des liens secondaires hors du lien principal de carte, avec cote/titre,
type de source, focus clavier et cibles tactiles de 44 pixels.

Le style noir/anthracite, ivoire/or, les images archéologiques existantes avec
leurs crédits, la bannière statue grecque et temple, les sommaires et les
anciens liens restent inchangés. Aucun SVG 2,5D n’est réintroduit.

## 3. Contrôles

La vérification des dossiers rejette les liens directs non inventoriés ou
dupliqués. tests/test_greek_folder_reading_cards_20261105.py teste deux
reconstructions successives, le sommaire complet, l’intégrité stricte des
balises article des manuscrits, les URL uniques et le CSS responsive.

La validation définitive requiert python -m unittest discover -s tests -v,
python scripts/build_native.py, python scripts/verify_publication.py,
un workflow de publication réussi et un reçu public
/catalog/publication-verification.json à jour.
Le commit GitHub seul ne confirme pas un déploiement sur bobmythos.fr.

Aucun registre de numérotation, aucune demande editorial/inbox, aucune
automatisation ni cadence de publication n’a été modifié.
