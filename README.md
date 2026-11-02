# MYTHOS — copie statique de test

Ce dépôt prépare une publication gratuite de l’encyclopédie MYTHOS sur GitHub Pages, sans modifier le site WordPress original.

- **Site WordPress d’origine :** https://bobmythos.fr
- **Adresse de test prévue :** https://bobcribb.github.io
- **Import public :** pages et articles publiés via l’API WordPress.com
- **Brouillons privés :** non importés ; ils restent sur WordPress
- **Images :** chargées depuis la médiathèque WordPress (elles ne sont pas sauvegardées ici)
- **Hébergement :** GitHub Pages, sous réserve des limites et conditions de GitHub

## Activer le site test

Dans le dépôt, aller à **Settings → Pages → Build and deployment** et choisir la source **GitHub Actions**. Le workflow de publication fonctionne sur la branche main, à la demande et environ une fois par heure (horaire non garanti).

La synchronisation exige **au moins 400 pages publiques** afin de ne pas remplacer le site par une publication vide en cas d’erreur de l’API WordPress.

## Ne pas changer le domaine pour le moment

Ne pas modifier les DNS de `bobmythos.fr`, ne pas ajouter de `CNAME` à ce dépôt, et ne pas résilier le forfait WordPress avant vérification de l’adresse de test.

L’export HTML ne reproduit pas les fonctions dynamiques de WordPress. Il ne conserve pas non plus les brouillons, commentaires privés, médias originaux ni les mises en page de tous les blocs. Faire une sauvegarde XML WordPress et une sauvegarde indépendante de la médiathèque.

## Technique

Le script de génération `scripts/build.py` récupère les contenus publics WordPress, reproduit leur hiérarchie d’URL, construit l’index, la recherche, le sitemap et les pages HTML dans `_site/`.

La mise à jour des nouvelles pages WordPress est automatique après exécution du workflow GitHub Actions.