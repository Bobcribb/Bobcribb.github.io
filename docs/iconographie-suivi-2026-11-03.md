# MYTHOS — suivi de l'enrichissement iconographique (3 novembre 2026)

## Référence et périmètre

Dépôt source : `Bobcribb/Mythos` · branche `main`.
Inventaire GitHub contrôlé après les modifications de cette intervention : **47 fichiers HTML** et **53 fichiers SVG** présents dans l'arborescence (y compris les documents d'archives). Ces effectifs ne signifient pas que tous les liens, images distantes ou déploiements publics fonctionnent.

Les trois études prioritaires ont été relues depuis GitHub : `philosophie-iliade.html` (**12 sections, 13 éléments `<figure>`**), `philosophie-odyssee.html` (**12 sections, 12 éléments**), `philosophie-theogonie.html` (**13 sections, 15 éléments**). Chaque section `philo-chapter` contient au moins une figure ; **40 figures au total** dans ces trois pages. La condition « dix pages imprimées minimum » **n'est pas certifiée**, car la pagination PDF/navigateur n'a pas été mesurée ; les sections ne sont pas des pages.

## Travail enregistré dans cette intervention

**12 créations vectorielles nouvelles**, distinctes de reproductions d'objets historiques, et **12 pages HTML modifiées** pour les relier avec titre, texte alternatif, date, sources et mention explicite de création contemporaine assistée par IA. Chaque association SVG/page a été relue depuis le dépôt après commit (présence de l'asset, balise `img`, identifiant unique, légende et feuille de style) ; une lecture a nécessité un nouvel essai après une erreur réseau transitoire.

| Page HTML | Nouveau fichier SVG dans `assets/iconographie/` |
| --- | --- |
| `corpus/mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html` | `aphrodite-deux-genealogies.svg` |
| `corpus/civilisations/perse-iran-ancien-behistun.html` | `behistun-trois-langues.svg` |
| `corpus/theatre-grec/comedies/kokalos-etude.html` | `kokalos-trois-niveaux-sources.svg` |
| `origines-du-sacre.html` | `origines-sacre-indices-hypotheses.svg` |
| `mythologie-comparee.html` | `mythologie-comparee-preuve.svg` |
| `philosophie.html` | `philosophie-trois-epopees.svg` |
| `theatre-grec.html` | `theatre-grec-deux-lectures.svg` |
| `civilisations.html` | `civilisations-preuves.svg` |
| `grande-encyclopedie.html` | `grande-encyclopedie-methode.svg` |
| `mythologie-grecque.html` | `mythologie-grecque-sources.svg` |
| `corpus/origines-du-sacre/conv-tome-XXXIII-chapitres-403-410.html` | `origines-voix-rituelles.svg` |
| `sommaire-general.html` | `legende-provenance-mythos.svg` |

**Méthode** : inserts HTML localisés, pas de réécriture des textes d'origine, des sommaires ou de leur numérotation. L'ajout de la feuille de style `mythos-iconographie.css` a été nécessaire pour la page critique Kôkalos et le tome XXXIII des Origines du sacré. Les références de sources antiques sont des indications de textes, non des licences accordées pour des reproductions historiques ; les images ici créées sont des schémas originaux de méthode ou d'interprétation, non des photographies antiques.

## Points de contrôle et limites

- Un conflit GitHub **409** s'est produit lors de l'écriture de `theatre-grec.html`, modifié simultanément. Le fichier a été relu puis l'insertion a été recalculée sur sa version récente avant commit. Aucune ancienne version n'a été écrasée volontairement.
- Les documents historiques déjà présents, y compris les images Wikimedia Commons des trois études philosophiques, **n'ont pas été remplacés** au cours de cette intervention. La validité de chaque URL externe, les licences et les crédits méritent un audit distinct.
- **Aucun test de publication sur bobmythos.fr** n'a été réalisé : présence dans GitHub ≠ déploiement confirmé.
- **Aucune automatisation existante modifiée** dans cette intervention.

## Prochaines cibles sans doublons

1. Mesurer réellement les **pages A4 imprimées** de chacune des trois études avec un rendu du site, en conservant les textes.
2. Revoir les archives grecques et leurs monographies (`corpus/mythologie-grecque/archives/`), en distinguant photos de pièces archéologiques, croquis de restitution et nouveaux schémas.
3. Illustrer les tomes encore dépourvus de figures des `corpus/origines-du-sacre/`, en choisissant des témoins historiques réellement attribuables et des légendes contextualisées.
4. Revoir `corpus/theatre-grec/comedies/aiolosikon-etude.html` et les pages de créations contemporaines, sans transformer la reconstruction en fragment antique.
5. Auditer les images d'accueil externes (`index.html`) et leur pertinence universitaire / provenance ; éviter d'annoncer leur origine sans vérification.
6. Vérifier les images des sites archéologiques et la distinction entre architectures conservées et hypothèses de restitution.

Chaque prochain ajout doit rechercher dans le HTML la présence d'une illustration équivalente et éviter un deuxième `id` ou un second fichier avec le même sujet.
