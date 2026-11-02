# MYTHOS — Continuité éditoriale, source de vérité et protection contre les pertes

Dernière consolidation : 2 novembre 2026.

## Architecture retenue

- **GitHub** (dépôt `Bobcribb/Bobcribb.github.io`, branche `main`) est la source de publication de `https://bobmythos.fr/`.
- **WordPress** est une source historique à préserver, et non le moteur de déploiement GitHub. Ne pas y publier de nouvelles pages à la place de GitHub : cela crée des écarts.
- Les **134 brouillons de pages et l'article brouillon** restent privés sur Google Drive, jamais dans ce dépôt public.
- Les **110 médias** sont enregistrés dans `media/2026/10/`, contrôlés par `media/manifest.json`. Une seconde copie indépendante est privée sur Google Drive.
- Une **archive intégrale de l'état du dépôt GitHub**, fichiers HTML, Markdown, médias, workflows et scripts, est conservée dans le Drive privé MYTHOS, dossier « Archives intégrales GitHub — MYTHOS — 2026-11-02 ».
- Les exports GitHub ne remplacent pas un export natif WordPress WXR/XML si l'on veut restaurer les blocs Gutenberg, menus et métadonnées d'origine.

## Circuit obligatoire pour chaque nouveau chapitre automatique

1. Vérifier la dernière production **réellement publiée dans la série concernée**, puis rédiger un nouveau chapitre inédit, sourcé, avec bibliographie et distinction entre faits, hypothèses et reconstitutions.
2. Nommer un chemin **unique** sous `chapitres/`, sans caractères spéciaux ni accent dans les noms de répertoires/fichiers :
   - `chapitres/encyclopedie/chapitre-260-nom-du-dieu.md`
   - `chapitres/comparatif/volume-lv-sujet.md`
   - `chapitres/comedies/auteur-oeuvre-analyse.md`
   - `chapitres/tragedies/volume-xcix-oeuvre.md`
   - `chapitres/origines-du-sacre/tome-xxxviii-chapitres-443-450.md`
3. Le fichier doit commencer par un titre Markdown `#` et, si utile, par le front matter simple `title:` / `description:`. Les contenus sont **publics** ; ne jamais publier des brouillons confidentiels.
4. Vérifier qu'aucun fichier de même adresse n'existe déjà. Utiliser le connecteur GitHub pour créer le nouveau fichier sur `main`; pour compléter une étude existante, récupérer son SHA et mettre à jour uniquement ce fichier.
5. Confirmer le commit GitHub. Le workflow de publication reconstruit le site et référence automatiquement les fichiers de `chapitres/` dans le catalogue, la recherche et le sitemap.
6. Vérifier le workflow et la page HTTPS publique ; si cela échoue, **déclarer « version GitHub enregistrée, publication non vérifiée »**. Si la création GitHub échoue, **déclarer « chapitre livré dans la conversation uniquement, à intégrer »**.
7. Conserver l'ordre et la numérotation propre à chacune des cinq séries. Aucune série ne doit déduire son dernier numéro des autres séries.

## Contrôles de perte et de cohérence

- `.github/workflows/audit-integrity.yml` : vérifier pages locales, liens internes, médias et SHA-256 après reconstruction.
- `.github/workflows/backup-complete.yml` : produire une archive du dépôt en parties vérifiables ; ses artifacts GitHub expirent et ne sont **pas** une sauvegarde hors GitHub avant leur copie sur Drive.
- Contrôler régulièrement les publications WordPress résiduelles ou les productions de conversations non transférées sur GitHub : les automatismes de GitHub n'ont pas accès à ces deux sources sans action supplémentaire.
- Avant tout nettoyage, suppression de fichiers, fusion de pages, changement de domaine ou annulation WordPress, vérifier que le contenu demandé existe dans GitHub et dans une archive indépendante.

## Restauration du site GitHub

1. Télécharger **tous** les volumes ZIP de l'archive intégrale du même jeu de sauvegarde, ainsi que le ZIP manifeste.
2. Extraire les ZIP : chacun contient un fichier `MYTHOS-source-integrale.tar.gz.part-NN`.
3. Vérifier les SHA-256 de chaque morceau à l'aide de `VOLUMES_SHA256.txt`.
4. Réassembler dans l'ordre : `cat MYTHOS-source-integrale.tar.gz.part-* > MYTHOS-source-integrale.tar.gz`.
5. Vérifier la somme de l'archive entière dans `ARCHIVE_SHA256.txt`.
6. Extraire dans un nouveau dossier propre avec `tar -xzf MYTHOS-source-integrale.tar.gz`.
7. Pousser les fichiers dans un dépôt GitHub de restauration, exécuter `python scripts/build_native.py` puis `python scripts/audit_integrity.py`; reconfigurer Pages et le domaine si nécessaire.

**Limite documentée :** l'archive intégrale contient les fichiers de travail de la version GitHub, mais pas l'historique interne `.git`, ni l'état privé des automations, ni un export complet natif WordPress. Les archives privées de brouillons et médias doivent donc être conservées séparément.

## Architecture de navigation pérenne — demande du 2 novembre 2026

**Principe directeur : MYTHOS est une encyclopédie des mythologies du monde**, et non un simple catalogue alphabétique d'articles grecs. La Grèce antique est traitée en priorité et particulièrement visible, mais l'Égypte, la Mésopotamie, la Perse, l'Inde, la Chine, le Japon, les sociétés africaines, les Amériques et l'Océanie doivent rester accessibles au même niveau encyclopédique.

La navigation officielle, commune à toutes les pages, est :
1. **Mythologies du monde** — panorama des grandes traditions, dieux et récits ;
2. **Grèce antique** — porte d'entrée mise en avant : dieux, héros, Homère, Hésiode, cultes et sanctuaires ;
3. **Théâtre grec** — section indépendante pour tragédies, comédies, œuvres perdues, reconstitutions et commentaires ;
4. **Études philosophiques** — section indépendante pour Hegel, Nietzsche, historiographie, lectures philosophiques et mythologie comparée ;
5. **Civilisations du monde** — accès **par continent** : Afrique, Europe, Asie, Amériques, Océanie. Ce classement est un outil de navigation moderne, non une catégorie historique figée ;
6. **Index intégral** — tous les dossiers, consultables alphabétiquement, sans suppression ;
7. **Recherche** — moteur transversal des documents publiés.

L'accueil doit présenter ces parcours, jamais une sélection arbitraire des premiers dossiers par ordre alphabétique. Maintenir la présentation muséale **noir/anthracite, ivoire et or** et une navigation lisible sur téléphone. Ne pas faire disparaître un dossier à l'occasion d'une réorganisation.

**Mise en œuvre durable :** \`scripts/build_navigation.py\` génère l'accueil et les portails \`/mythologies/\`, \`/grece/\`, \`/theatre/\`, \`/philosophie/\`, \`/civilisations/\` et les cinq portails continentaux. \`scripts/build_native.py\` l'appelle lors de chaque publication, puis réindexe l'ensemble. Les mises à jour éditoriales ne doivent pas remplacer ce système par l'ancienne page d'accueil à 24 liens ni par la simple liste alphabétique.

Vérifier après chaque modification le fonctionnement des menus, l'accessibilité mobile, les liens internes, le nombre de dossiers et les 110 médias locaux. Conserver l'indépendance de WordPress et ne pas modifier les DNS ou le domaine pour une simple réorganisation de la navigation.

## Trois portes d'entrée fondamentales : Dieux, Héros, Récits — 2 novembre 2026

Le public doit pouvoir accéder directement, depuis **toutes les pages** et dès le début de l'accueil, aux trois grands corpus de l'encyclopédie :

- **Dieux et déesses** — \`/dieux-et-deesses/\` : monographies grecques d'abord, puis divinités de l'Égypte, de la Mésopotamie, des mondes nordiques, de l'Inde, du Japon et d'autres traditions. Conserver la grande étude grecque originale \`/dieux/\` et le dictionnaire mondial des dieux.
- **Héros et héroïnes** — \`/heros-et-heroines/\` : les notices grecques d'abord, puis Gilgameš, Sunjata, Māui, Cú Chulainn, Rāma et Sītā, Rostam, les héros mayas, etc. Conserver l'étude grecque originale \`/heros/\` et les cycles épiques du monde.
- **Grands récits** — \`/recits-mythologiques/\` : théogonie, cycles thébain et troyen, Argonautiques et Odyssée, puis les corpus égyptiens, mésopotamiens, indiens, chinois et japonais, ainsi que les récits héroïques du monde. Conserver l'étude grecque originale \`/recits/\`.

**Navigation commune attendue** : Grèce (mise en valeur), Dieux, Héros, Récits, Mythologies, Théâtre, Philosophie, Civilisations, Recherche. L'index complet reste accessible dans l'accueil, les pages de recherche, le catalogue et le pied de page.

Les trois portails sont générés à chaque publication par \`scripts/build_navigation.py\` et sont recensés dans \`search.json\` et \`sitemap.xml\`. Les nouvelles notices de ces ensembles doivent apparaître automatiquement par extraction des chemins existants du catalogue ; ne pas laisser une liste de six dieux ou six héros comme unique index. Ne jamais inventer de notices non publiées ni supprimer les monographies originales.

Conserver le style noir/or, l'accessibilité du menu sur mobile et l'indépendance de WordPress.


## Série des comédies grecques — numérotation canonique (2 novembre 2026)

- Volume I : `chapitres/comedies/volume-001-eupolis-astrateutoi.md`.
- Volume II : `chapitres/comedies/volume-002-eupolis-chrysoun-genos.md`.
- Volume III : `chapitres/comedies/volume-003-eupolis-heilotes.md` (texte intégral migré depuis l'ancien doublon `volume-002-eupolis-heilotes.md`, devenu une notice d'orientation conservant les anciens liens).
- Volume IV : `chapitres/comedies/volume-004-eupolis-aiges.md`.
- Volume V : `chapitres/comedies/volume-005-eupolis-poleis.md` (Eupolis, *Poleis* ; analyse critique du tribut, des cités personnifiées et de la relation impériale ; commit initial `ef534f949500c2f5ca821629415bda295e9133fe`).
- Volume VI : `chapitres/comedies/volume-006-cratinos-nemesis.md` (Cratinos, *Némésis* ; œuf d'Hélène, Léda, Zeus, satire de Périclès et paratragédie ; commit initial `29ddb63dfc77d79af6e626c9f152abe539c8914c`).
- Volume VII : `chapitres/comedies/volume-007-cratinos-ploutoi.md` (Cratinos, *Ploutoi* ; Titans et puissances de richesse, Cronos, papyrus Cumont, âge d'or, lecture socio-politique, deux scènes originales ; commit initial `1a8ce439afa1ad9cb64db4c7400616603a722e1a`).

- Volume VIII : `chapitres/comedies/volume-008-cratinos-odysseis.md` (Cratinos, *Odysseis* ; Cyclope gastronome, Homère IX, chœur d'équipage discuté, Platônios, deux scènes originales ; commit initial `ad1f1816ccc90a1cf5a4a741eff95a84e9ecf2bc`).

- Volume IX : `chapitres/comedies/volume-009-cratinos-cheirones.md` (Cratinos, *Cheirones* ; fragment 258, théogonie politique de Périclès, Chiron, éducation et satire, deux scènes originales ; commit initial `e06660ead350185cf026628f0e4aaeaa1816e86c`).

- Volume X : `chapitres/comedies/volume-010-cratinos-dionysalexandros.md` (Cratinos, *Dionysalexandros* ; P.Oxy. IV 663, satire de Périclès, parodie troyenne, costume et drame satyrique ; complément de la notice historique, commit initial `92258dfc341c8845d429badb212dae592650787b`).

- Volume XI : `chapitres/comedies/volume-011-cratinos-pytine.md` (Cratinos, *Pytine* ; concours de 423, Comédie personnifiée, vin, rivalité avec Aristophane et deux scènes originales ; commit initial `12625d84cce456304f5a31800f9f7052992b9fac`).

- Volume XII : `chapitres/comedies/volume-012-cratinos-archilochoi.md` (Cratinos, *Archilochoi* ; frr. 1, 2, 6, 7, 12, Métrobios et Cimon, agôn poétique hypothétique, datation disputée, deux scènes originales ; commit initial `9b20112fd994a377c1dba57eac7861d41549d356`).

**Pour la suite :** rechercher le prochain numéro libre en inspectant les fichiers de `chapitres/comedies/` et les dossiers historiques ; ne pas réutiliser les numéros I à XII et ne pas traiter la notice de redirection `volume-002-eupolis-heilotes.md` comme un nouveau volume. Aucun texte privé ni contenu WordPress ne doit être créé ici. Chaque nouveau volume doit être vérifié après commit et après reconstruction du catalogue.
