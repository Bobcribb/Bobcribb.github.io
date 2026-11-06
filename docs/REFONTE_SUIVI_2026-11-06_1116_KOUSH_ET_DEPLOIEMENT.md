# MYTHOS — Refonte du 6 novembre 2026 : Koush, Méroé et contrôles éditoriaux

## Contrôles de départ

La branche `main` de `Bobcribb/Bobcribb.github.io` a été relue avec les deux règles de publication `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`. Les anciens numéros des collections `origines-du-sacre`, `encyclopedie`, `comedies`, `tragedies`, `comparatif` restent sous le circuit atomique `editorial/inbox/<uuid>.json`, avec reçus GitHub Actions. Cette intervention n'ajoute aucun texte à ces cinq files et ne modifie ni numéro ni registre.

## Étude universitaire intégrale restaurée

- **Cote historique :** Volume XII — *Royaume de Koush et Méroé : Amon, Apédémak et la royauté sacrée*.
- **Source primaire de migration :** sauvegarde WordPress privée de MYTHOS, volume 02, entrée `1136`, état historique `draft`. Une seule entrée de cette archive a été sélectionnée pour le transfert demandé ; les autres textes du Drive demeurent privés.
- **Classement :** `bibliotheque-mythologies-du-monde/mythos-volume-12-koush-meroe-apedemak/index.html`, distinct du dossier historique déjà publié `/bibliotheque-mythologies-du-monde/civilisations-histoire-koush-meroe/`. Pas de nouveau numéro canonique.
- **Intégrité de l'archive :** 48 114 caractères HTML originaux, reproduits dans le même ordre avec seules 63 ancres de navigation ajoutées ; 20 grandes sections et 63 titres de sections/sous-sections. La bibliographie, les références à l'UNESCO, au DAI, au British Museum et les analyses sont conservées sans troncature.
- **Garde de prose scientifique :** 36 371 caractères après normalisation des balises (empreinte SHA-1 Git `fc817178632b87b3d413afdb28794bb13d4659d4`), calculée depuis le corps WordPress d'origine ; vérification réexécutable hors réseau dans les tests.

L'étude est éditorialement restituée, non validée par une évaluation académique indépendante. Les témoins archéologiques et les hypothèses interprétatives gardent le statut exposé dans le manuscrit.

## Navigation, image et responsive

Le document est doté d'un sommaire vers 20 parties, de 63 ancres, et de renvois vers le portail mondial `/mythologies/`, le portail africain `/civilisations/afrique/`, la monographie historique de Nubie et les bibliothèques égyptienne et comparée. Les générateurs d'accueil, des mythologies et du portail Afrique proposent des cartes vers **une seule page intégrale**, sans dupliquer la prose.

Figure historique externe sourcée (pas une restitution 2,5D) : vestiges du temple d'Apédémak à Naqa, photographiés par **LassiHU en 2005**, Wikimedia Commons : https://commons.wikimedia.org/wiki/File:Naqa_Apedamak_temple.jpg ; licence **CC BY-SA 4.0** : https://creativecommons.org/licenses/by-sa/4.0/. Le crédit et la nature archéologique de l'image figurent dans la légende. La feuille de style muséale noir, or et ivoire conserve le bandeau grec et donne une largeur maximale à l'image, adaptée à l'écran mobile.

## Réparation des échecs constatés dans GitHub Actions

Les exécutions `42201083614` et `42201059070` de `publish.yml` ont échoué sur les tests d'intégrité des lecteurs *Kalevala* et *David de Sassoun*. La transformation HTML des sources par le constructeur modifiait les séparateurs et attributs sans modifier les mots ; les tests comparaient alors des morceaux de HTML sérialisés plutôt que la prose. Comparaison avec les archives WordPress :

- *Kalevala* : 36 741 caractères de prose normalisée, empreinte Git `7de312d8772e13ed48cc71936cb596da2bacde90` ; égalité entre le manuscrit d'origine et le corps HTML actuellement sur `main`.
- *David de Sassoun* : 35 162 caractères, empreinte Git `3e63c2dfcb74c4a66866169c0bc4a36fb9011e38` ; égalité également confirmée.

Le nouveau module `scripts/archival_prose_integrity.py` est ajouté pour le volume XII : il compare chaque mot du texte normalisé à son empreinte de référence malgré les reformatages HTML. Les tests de Kalevala et Sassoun ont été réparés **par une autre intervention concurrente** (commit `7ea70cd618a7e51cf40f84edde3ba6aa851dd718`) ; leurs lecteurs et ces tests ne sont pas modifiés par le présent lot. La comparaison des deux volumes avec leurs sources a été effectuée séparément au cours de ce contrôle.

Un second incident, déjà corrigé par une autre intervention de la branche principale, concernait les neuf lecteurs `*-source.html` du Théâtre, créés après la charte graphique ; `daidalos-source.html` déclenchait un échec de `verify_museum_design.py`. Ce point a été **corrigé par une intervention concurrente déjà enregistrée** au commit `7c1e86f2ae`, qui génère ces neuf lecteurs avant la passe muséale et l'indexation. Ce rapport ne revendique pas cette correction comme une écriture de la présente intervention. Un nouveau test vérifie que cet ordre reste préservé.

## Statut de vérification

La création GitHub, la présence du code sur `main`, la réussite des validations, puis l'accessibilité HTTPS constituent des états **distincts**. Ne confirmer une mise en ligne qu'après workflow `publish.yml` réussi sur un commit descendant et contrôle HTTP 200 du nouveau lecteur. Un simple commit ou un audit de génération ne suffit pas.

Aucun autre manuscrit ou archive, média d'origine, registre ou planification horaire MYTHOS n'est modifié dans ces changements.
