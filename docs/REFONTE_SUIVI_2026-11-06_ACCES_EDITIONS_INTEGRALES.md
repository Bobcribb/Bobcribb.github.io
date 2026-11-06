# MYTHOS — Raccordement à deux éditions intégrales historiques (6 novembre 2026)

## État scientifique et autorisation de diffusion

Lecture préalable réelle de `main`, `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`. Le dépôt contient déjà les deux lecteurs complets, à leurs adresses historiques :

- `corpus/mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html` : monographie `Aphrodite`, 39 995 octets selon l'inventaire GitHub, douze titres H2 et sources/bibliographie dans le document ;
- `corpus/origines-du-sacre/edition-integrale-tomes-I-XXVII.html` : édition historique originale des tomes I à XXVII, environ 1,85 Mo de HTML.

Il ne s'agit **pas de nouvelles publications scientifiques** : ces fichiers étaient déjà versionnés et accessibles comme ressources publiques dans la source GitHub. La présente modification leur crée deux entrées de consultation directe depuis la section « Une bibliothèque documentée » de l'accueil. Les pages restent à leur URL, leur cote et leur texte intégraux. Les liens de la bannière vers l'accueil préexistent dans les lecteurs muséalisés, ce qui assure le trajet retour.

Le fonds Drive contient par ailleurs 135 brouillons WordPress sauvegardés dans quinze Google Docs. Leur document d'index du 2 novembre porte explicitement « Ne pas publier ces documents sur GitHub ». Malgré leur accessibilité privée au connecteur, aucun brouillon brut n'est donc transféré dans le dépôt public : l'autorisation et la validation individualisées de la version publiée manquent. Aucun nouveau chapitre numéroté n'est créé, aucun UUID ne doit être inventé.

## Travail graphique et navigation

- Section `#corpus-status` enrichie de deux cartes illustrées ; lecture intégrale directe, source iconographique et licence à côté de la carte, sans imbrication de liens.
- Photographies déjà versionnées, pas d'image 2,5D : kylix de Pistoxénos (British Museum, CC BY 2.5) pour Aphrodite ; photographie de la chambre d'Ounas par Vincent Brown (CC BY 2.0), signalée comme objet contextuel pour les vingt-sept tomes.
- Grille adaptative 2 colonnes / 1 colonne sur téléphone, contraste noir/ivoire/or, états de focus clavier. La grande bannière grecque et l'unique entrée d'encyclopédie grecque demeurent intactes.
- `add_home_integral_archive_shelf` produit uniquement les liens vers des fichiers réellement présents dans `_site`. Une seconde passe supprime et reconstruit son propre bloc sans dupliquer les entrées ; aucune prose d'archive n'est retouchée.

## Contrôle prévu et statut

Le test `tests/test_home_integral_archives_20261106.py` vérifie conservation binaire de deux lecteurs simulés, liens directs, absence de doublon, maintien du contenu antérieur et non-création de liens cassés lorsque les lecteurs sont absents.

Le commit de proposition et les contrôles GitHub Actions doivent encore être confrontés au déploiement public. Ne pas confondre une branche/PR avec publication effective sur `https://bobmythos.fr/`. Aucun fichier `editorial/inbox/`, aucun registre canonique ni planification MYTHOS n'est modifié.
