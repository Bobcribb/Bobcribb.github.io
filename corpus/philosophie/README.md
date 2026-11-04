# Études philosophiques longues — édition du 4 novembre 2026

Les trois fichiers canoniques de lecture sont `philosophie-iliade.html`,
`philosophie-odyssee.html` et `philosophie-theogonie.html`, à la racine du dépôt.
Le seuil éditorial est de **100 pages A4 d’analyse par œuvre**, hors illustrations,
bibliographies, notices et notes de référence. Les anciens textes sont conservés.

## Reproduire le contrôle

Depuis la version du dépôt ayant produit l’édition :

```sh
python -m pip install -r corpus/philosophie/requirements-render.txt
python scripts/render_philosophie_a4.py
python scripts/check_philosophie_integrity.py
```

La police **Nimbus Roman** doit être installée et disponible pour Fontconfig.
Le format est A4, marges de 25 mm, corps 12 points et interligne 1,5. Le texte
coule en continu ; il n’existe ni saut obligatoire par chapitre ni hauteur
minimale destinée à augmenter le nombre de pages. Les titres internes restent
dans le contrôle analytique. La dernière page peut être partiellement remplie.

Les six fichiers produits se trouvent dans `assets/philosophie/pdf/` : une
édition illustrée et un contrôle d’analyse seule pour chaque œuvre. Le fichier
`assets/philosophie/pagination-2026-11-04.json` contient les décomptes réels,
les mots extraits par page et les empreintes des fichiers. L’habillage automatique
du site peut modifier la sérialisation HTML après publication : les empreintes
identifient les sources utilisées pour le rendu daté, et non toute future
reconstruction graphique du même texte.

## Conservation et documentation

`reference-avant-extension.json` conserve les empreintes du texte des sections
initiales, avec leur blob Git d’origine, les URL et les légendes des figures.
Le contrôle compare les textes avec normalisation des espaces uniquement.
Il vérifie aussi les ancres, les ressources locales, la présence des chapitres,
la pagination et l’absence de paragraphes longs dupliqués.

Les relevés de consultation des sources sont publiés dans
`assets/philosophie/sources/`. Ils distinguent les textes primaires, les
extraits universitaires et les notices bibliographiques. Une notice ne vaut
pas consultation intégrale d’un ouvrage. Les arguments non attribués sont
les propositions de lecture de l’étude ; les paraphrases nouvelles ne sont
pas présentées comme des citations littérales d’une traduction française.

Les douze images documentaires sont conservées localement sans modification
des pixels et avec leurs crédits. Leur relevé est dans
`assets/philosophie/documents/manifest.json`. Les trois photographies ajoutées concurremment au dépôt sont incluses. Les 31 schémas SVG préexistants
restent inchangés.

Les contrôles logiciels établissent la conservation et la pagination. Ils ne
constituent pas une évaluation philosophique automatique ni une expertise par
les pairs. Le rapport public précise la portée du contrôle éditorial.
