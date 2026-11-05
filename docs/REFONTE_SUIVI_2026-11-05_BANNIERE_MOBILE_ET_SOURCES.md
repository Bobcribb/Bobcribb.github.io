# MYTHOS — Refonte : cadrage mobile de la bannière et statut des manuscrits

**Contrôle du 5 novembre 2026.** Source de vérité : `Bobcribb/Bobcribb.github.io`, branche `main`. Ont été lus : `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md`, l'index privé des sauvegardes WordPress dans Google Drive, la file `editorial/inbox/`, `editorial/holds.json`, `editorial/numbering.json` et les sources HTML/CSS de l'accueil. Aucun registre de numérotation ni workflow horaire n'a été modifié.

## 1. Première publication universitaire : aucune attribuable à cette intervention

Le corpus **La Galigo — Volume XIX** est **déjà publié** à `/bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/`, avec étude intégrale, sommaire, références et bibliographie ; le dossier `docs/restauration-la-galigo-2026-11-04.json` documente la restauration. Une seconde création ferait doublon.

L'index de sauvegardes privées WordPress (2 novembre 2026) recense 135 anciens brouillons, 134 pages et 1 article, répartis dans 15 volumes Google Docs. Il porte explicitement la restriction documentaire « Ne pas publier ces documents sur GitHub ». Il s'agit de matériaux privés **non approuvés pour une première publication publique par le seul fait qu'ils sont accessibles**. Aucun contenu brut de cette archive privée n'a été copié, reconstitué ou tronqué.

Photographie de la file publique au contrôle : **453 fichiers JSON**, **413 UUID avec attribution** dans les cinq collections, **40 UUID sans attribution**, dont **20 retenus dans `editorial/holds.json`** et **20 autres sans reçu**. Ces 20 demandes doivent passer par l'attribution transactionnelle du workflow existant : ne pas recréer un UUID, choisir un numéro à l'avance, ni créer directement un chapitre dans `chapitres/`. Les compteurs sont susceptibles de changer dès l'exécution suivante.

**Bilan des nouvelles études intégrales publiées par cette intervention : 0.** Motifs : La Galigo déjà publiée ; fonds privés sans approbation de diffusion ; demandes publiques en file ou en retenue, non attribuables manuellement.

## 2. Correction graphique effective sur `main`

Le WebP muséal `assets/mythos-museum-banner.webp` mesure **2172 × 724 pixels** (rapport 3:1) et porte la statue grecque à gauche et le temple à droite. La règle de téléphone `@media(max-width:700px)` imposait `background-size:auto 160px` et recadrait le centre, supprimant une partie des deux extrémités sur écrans étroits.

Dans `assets/mythos-museum.css`, son cadrage est désormais `background-size:100% auto!important` avec positionnement `center top`, fond sombre et dégradé vertical conservés. **L'image elle-même n'est pas modifiée** : cette correction rend visible l'intégralité de sa largeur sur les smartphones, sans déformation. Elle conserve les titres, sommaires, cartes et textes du site.

Vérification de l'accueil GitHub : 24 balises `img`, 15 chemins de média uniques ; les 15 fichiers existent réellement dans les deux répertoires de médias du dépôt (`media/2026/10/` et `assets/reconstitutions-3d/`). Aucune image disparue n'est remplacée par une illustration artificielle.

## 3. Changements et contrôles

- Commit CSS : `c79f0721609df95d783187951888f51735487e06` — correction du cadrage mobile, sans toucher aux manuscrits ni aux archives.
- Commit test : `7d918e5fc92b6fc79886f84a31109292cf93a6ec` — `tests/test_museum_mobile_fullframe_banner.py`, vérification du dernier bloc CSS mobile, de la présence du WebP original, du sommaire de l'accueil et de l'entrée unique grecque.
- Relecture depuis `main` : le remplacement CSS est présent ; le sélecteur vérifié correspond au bloc mobile final. Le fichier de test est présent et son motif regex a été contrôlé sur le CSS récupéré.
- GitHub Actions : la validation du commit de test (`42050527737`) était **en cours**, de même que l'audit (`42050442377`), au contrôle. Le workflow de publication source `42050442357` était en attente. **Ne pas annoncer réussite ni déploiement sans conclusion explicite.**
- Contrôle public direct : `https://bobmythos.fr/catalog/publication-verification.json` pointait encore vers la source `f677da8325522702913bb69d77498cba6285f333`, avec 1 539 documents indexés, 27 archives et 110 médias. Le CSS servi par `https://bobmythos.fr/assets/mythos-museum.css` contenait encore l'ancienne règle `auto 160px` : **la correction mobile n'était pas encore déployée** au contrôle.

## 4. Vérification de clôture

Contrôler la conclusion de la validation GitHub sur le commit contenant la correction, puis `python -m unittest discover -s tests -v`, `python scripts/build_native.py` et `python scripts/verify_publication.py`. Sur le site public, vérifier l'apparition de `background-size:100% auto!important` dans la feuille CSS, le manifest `source_commit` plus récent et le cadrage réel de la statue et du temple à 320, 375 et 700 px.

Aucun nouvel identifiant historique, numéro canonique, cote de publication, manuscrit universitaire, PDF, archive, galerie 2,5D ou horaire d'automatisation n'est ajouté ou modifié.
