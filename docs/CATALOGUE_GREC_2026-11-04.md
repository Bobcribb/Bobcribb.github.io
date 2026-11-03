# Catalogue grec — audit du 4 novembre 2026

Le portail Grande Encyclopédie ne référençait que les 55 fichiers Markdown de
`chapitres/encyclopedie/`. Le portail grec ajoutait des archives, mais ignorait
notamment le livre des Atrides, l'Iliade scène par scène et l'école de Paris.
Les variantes `.html` et `/index.html` exposaient des catalogues différents.

## Correction

Les quatre entrées publiques sont reconstruites depuis les mêmes sources :
`/grande-encyclopedie/`, `/grande-encyclopedie.html`, `/mythologie-grecque/` et
`/mythologie-grecque.html`.

- 55 manuscrits universitaires numérotés, sans duplication ni réécriture ;
- 18 livres et parcours, avec 547 liens directs vers leurs sections existantes ;
- 15 notices de dieux, 16 notices de héros, une monographie universitaire MG ;
- 28 dossiers documentaires, 14 accès aux archives conservées et des renvois
  vers les collections distinctes.

Les 547 sections sont des subdivisions de livres et ateliers : ce chiffre
n'est ni celui de nouveaux chapitres rédigés, ni celui de manuscrits récupérés.
Les ancres existantes sont préservées ; les nouvelles ancres sont stables.
L'insertion des ancres conserve exactement le texte des articles.
Les deux numérotations GE et MG ne sont pas fusionnées avec les Origines du sacré.

## Limites documentaires constatées

Les numéros individuels présents sont 259–260 et 305–357. Les plages 1–258 et
261–304 n'ont pas de fichier individuel dans cette série : cette absence ne
prouve pas la perte de 302 textes, car les anciennes collections et les livres
possèdent leurs propres divisions. Le registre de récupération identifie plus
précisément Chiron, les chapitres 118–133 et les chapitres historiques 218–224.
Les sections courtes consacrées aux mêmes sujets ne remplacent pas ces études.

Le dépôt historique `Bobcribb/Mythos` contient les mêmes quatorze accès HTML du
corpus MG, sans manuscrits numérotés supplémentaires de cette collection dans
son arbre examiné. La recherche des fichiers archivés a aussi retrouvé
`mythologie-grecque.zip` : son unique page est une présentation synthétique et
ne contient pas les études manquantes. Elle n'est pas publiée comme récupération
de ces textes. Les recueils des Origines du sacré appartiennent à une autre série.

## Contrôles durables

`validate_publication.py` contrôle les quatre sommaires, l'inclusion de chaque
manuscrit GE et de chaque livre attendu, toutes les pages liées et toutes les
ancres du catalogue. Une omission fait échouer la validation avant déploiement.
La vérification existante de l'intégralité des manuscrits, des médias et des
archives est maintenue. Le graphisme commun noir et or est appliqué après la
génération, comme sur le reste du site.

Les corrections concurrentes de numérotation et la file d'attribution atomique
arrivées pendant cet audit sont conservées. Ce changement n'ajoute aucun nouveau
chapitre et ne modifie aucune planification.
