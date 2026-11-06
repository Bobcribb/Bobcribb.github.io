# MYTHOS — Refonte et restauration du volume XV : Hudhud des Ifugao

**6 novembre 2026** — Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`. Contrôle préalable de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ; respect des cinq collections à numérotation concurrente. Tous les fichiers sont conservés.

## Source et déduplication

- Manuscrit : **Volume historique XV — Philippines, Ifugao : Hudhud, héros ancestraux et récits chantés du riz**.
- Origine : sauvegarde WordPress MYTHOS de Google Drive, « Brouillons sauvegardés — Volume 02 », entrée historique `1139`, statut initial `draft`, slug `mythos-volume-15-philippines-ifugao-hudhud`.
- Nouvelle adresse source : `bibliotheque-mythologies-du-monde/mythos-volume-15-philippines-ifugao-hudhud/index.html`. L'ancienne cote XV est une cote documentaire WordPress, non un numéro nouveau d'une des cinq séries atomiques.
- Vérifications avant écriture : le corps scientifique compte **46646 caractères Unicode** ; l'extraction du nouveau lecteur, après retrait des seules 62 ancres ajoutées, correspond **exactement** au corps source ; 20 parties H2 et 62 titres H2/H3, sans réordonnancement, abrègement ni modification de la bibliographie ou des références.
- Documentation citée dans le manuscrit : UNESCO, *Hudhud chants of the Ifugao* et *Rice Terraces of the Philippine Cordilleras*, analyses des variantes et de la transmission orale. La consultation du texte n'est pas une validation universitaire indépendante de toutes ses affirmations.
- Déduplication : recherche par « Hudhud Ifugao » et slug exact, puis absence du dossier cible dans la branche `main`. Les archives voisines restent inchangées.
- La sauvegarde privée brute, les neuf autres entrées du document Drive, les métadonnées privées et les textes non examinés ne sont pas publiés.

## Navigation et graphisme

- Ajout d'un sommaire déroulant avec **20 entrées principales** et **62 ancres** au lecteur.
- Cartes vers le document sur l'accueil, le portail `/mythologies/` et `/civilisations/asie/` ; liens de retour depuis le lecteur vers les deux portails, puis renvois documentaires vers les volumes XIV (Khmer et Angkor) et XIX (La Galigo).
- Photo de paysage contemporaine : rizières de Batad (Ifugao), par **Pogidawako1234**, 7 septembre 2022, Wikimedia Commons : https://commons.wikimedia.org/wiki/File:Banaue_Rice_Terraces_-_Ifugao.jpg ; **CC BY-SA 4.0** : https://creativecommons.org/licenses/by-sa/4.0/. Cette image contextualise le paysage agricole ; elle ne représente pas une performance chantée. Crédit et licence visibles dans la page et les cartes. Image distante, non présentée comme nouveau fichier GitHub.
- Style muséal noir, anthracite, ivoire et or conservé, bannière grecque statue–temple inchangée ; sommaire à une colonne sous 720 px, liens utilisables au clavier et cible de 44 px, photo responsive, respect des préférences de réduction du mouvement.
- `tests/test_ifugao_hudhud_integrity_20261106.py` protège l'intégrité et le rendu sans prétendre vérifier scientifiquement la totalité du manuscrit.

## GitHub versus publication HTTPS

Les écrits source et les commits ne sont pas à confondre avec une page réellement déployée. Avant l'intervention, le manifeste public annonçait `source_commit=aaab3583b522dbd945f4014332e3f682325e5947` et 1 673 documents indexés ; la publication des volumes X (*Kalevala*), XII (Koush) et XIII (Arménie) a été constatée. Le volume XIV (Khmer) répondait encore 404 lors du contrôle. Les changements présents ici doivent recevoir un déploiement GitHub Actions réussi puis un contrôle HTTP 200 du nouveau volume XV, de la présence des liens dans les sommaires, de l'image, des crédits, du contenu intégral et du manifeste public.

Les autres automatisations MYTHOS et leurs planifications horaires demeurent inchangées.
