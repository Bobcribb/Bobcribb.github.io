# MYTHOS — Restitution intégrale du volume historique XIV : Khmer et Angkor

Date : 6 novembre 2026. Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`. Parent examiné : `2a0bcb066d2f4781890d8e738a208f2f55ad77d8`.

## Contrôle préalable et intégration universitaire

Les règles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relues. L'archive privée Google Drive **« MYTHOS — Brouillons sauvegardés — Volume 02 (10 pages) »**, document `1ed1FzEvwiIk942EzqhUHTFwR8zy3NPUooFNnucTAfpE`, a été inspectée pour isoler l'unique entrée WordPress **ID 1138**, ancien slug `mythos-volume-14-khmer-angkor-cosmogonies`, statut historique `draft`. Les autres entrées sont restées privées.

Titre exact : **Volume XIV — Khmer et Angkor : Viṣṇu, Śiva, le barattage de l'océan et les récits royaux**. Le corps HTML WordPress comporte **47507 caractères**, **20 titres H2**, **43 sous-titres H3**. Texte, citations, variantes, analyses philosophiques, « Sources institutionnelles et méthodologie », liens et bibliographie sont conservés dans leur ordre original. Les 63 identifiants de sommaire sont de simples attributs HTML ajoutés aux en-têtes existants. Leur retrait restaure **strictement** les 47507 caractères du source initial. Empreinte Git blob du corps original UTF-8 : `b04f7fdecb1ef6c76fb394797b6a58b477e8462d`. Vérification reproductible avec `hashlib.sha1(b'blob '+len(bytes).encode()+b'\\0'+bytes)` et le test fourni.

L'ancien corpus `bibliotheque-mythologies-du-monde/civilisations-histoire-khmers-angkor/index.html` était déjà publié : c'est une étude historique distincte (22 286 caractères), non le volume XIV. Aucun autre fichier intégral de cette cote n'a été trouvé sous le nouveau chemin ni dans la recherche GitHub. Cette publication restaure un **volume de bibliothèque**, pas un nouveau chapitre numéroté parmi les cinq séries soumises à `editorial/inbox/`. La cote **XIV** est historique et conservée, non attribuée par GitHub Actions.

Nouvelle page GitHub : `bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/index.html`, URL prévue `https://bobmythos.fr/bibliotheque-mythologies-du-monde/mythos-volume-14-khmer-angkor-cosmogonies/`.

## Navigation et identité graphique

- Carte illustrée vers l'étude depuis `/mythologies/`, l'accueil et `/civilisations/asie/`, tous reconstruits dans `scripts/build_navigation.py`.
- Renvois réciproques entre le volume XIV et `/bibliotheque-mythologies-du-monde/civilisations-histoire-khmers-angkor/` ; la prose de la notice historique existante ne change pas.
- Sommaire de 20 parties avec les 43 sous-titres accessibles, cibles clavier, lecture en une colonne sur smartphone, charte muséale anthracite–ivoire–or et bannière grecque inchangée.
- Photo archéologique du relief du barattage de l'océan de lait à Angkor Wat : **Jadamta, 8 novembre 2012**, Wikimedia Commons `https://commons.wikimedia.org/wiki/File:Angkor_Wat_-_Churning_of_the_Sea_of_Milk.JPG` ; licence **CC BY-SA 3.0**, `https://creativecommons.org/licenses/by-sa/3.0/`. Il s'agit de vestiges photographiés, non d'une restitution 2,5D. Le générateur muséal préserve cette photo et les cartes des volumes XII et XIII avec leurs crédits.
- Le volume n'est pas présenté comme une édition critique validée par comité scientifique : c'est la restitution du manuscrit éditorial de MYTHOS.

## Garde d'intégrité, validations et publication publique

`tests/test_khmer_angkor_integrity_20261106.py` conserve l'empreinte binaire, le nombre de sections, les sources et bibliographies, vérifie l'unicité des ancres, les retours, la photographie sourcée et deux passes d'habillage sans perte de prose.

Avant intervention, le manifeste HTTPS `/catalog/publication-verification.json` indiquait `source_commit=db016f6cbc0bec783e369a1e2874f0c6a1883aa6`, **1604 documents indexés**, **27 tomes** et **110 médias**. Les lecteurs Kalevala, Arménie et Koush récemment créés sur `main` étaient encore indisponibles en HTTP 404. Le présent commit ne prouve pas la mise en ligne : vérification exigée par GitHub Actions `publish.yml` et HTTPS 200 pour cette page, puis présence des liens et des sources sur le site.

Aucun UUID, reçu, registre de numérotation, ouvrage préexistant, archive privée complète, automatisation horaire ni configuration d'autres séries MYTHOS n'a été modifié.
