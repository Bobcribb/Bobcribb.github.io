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


- Volume XIII : `chapitres/comedies/volume-013-eupolis-demoi.md` (Eupolis, *Dēmoi* ; P. Cair. 43227, fragments 99–146 K–A, retour de Solon, Miltiade, Aristide et Périclès, Pyronidès/Myronidès, datations 417–416/412/410, mémoire politique et justice, deux scènes originales distinctes de la notice historique ; commit initial `2adf0e9f88d7efe9802a344493463378f8b89e6b`).

**Prochain volume de la série : XXVII**, après vérification du dépôt, de la reconstruction publique et des notices existantes. Les pages historiques ne sont pas remplacées ; aucune publication WordPress n'est autorisée.

**Pour la suite :** rechercher le prochain numéro libre en inspectant les fichiers de `chapitres/comedies/` et les dossiers historiques ; ne pas réutiliser les numéros I à XVII et ne pas traiter la notice de redirection `volume-002-eupolis-heilotes.md` comme un nouveau volume. Aucun texte privé ni contenu WordPress ne doit être créé ici. Chaque nouveau volume doit être vérifié après commit et après reconstruction du catalogue.

- Volume XIV : `chapitres/comedies/volume-014-eupolis-marikas.md` (Eupolis, *Marikas* ; Hyperbolos, parole populaire, polémique avec Aristophane, deux scènes originales ; commit initial `3a26366de26581b0919f365e702a02d40fa26628`).
- Volume XV : `chapitres/comedies/volume-015-eupolis-baptai.md` (Eupolis, *Baptai* ; frr. 76–98 K.-A., Cotyto, Alcibiade, critique de la noyade légendaire, trois scènes originales, 23 sections ; commit initial `4f33e0e5d4a8743bcae346c3caa2237f8f3f1db2`).

- Volume XVI : `chapitres/comedies/volume-016-eupolis-kolakes.md` (Eupolis, *Kolakes* ; concours de 421, Callias, Protagoras, frr. 156–190 K.-A., économie du banquet et de la flatterie, 29 sections, trois scènes originales ; commit initial `f3b817f85d72fe609a507399a4cfa615cab22801`).

**Contrôle technique du 2 novembre 2026 :** le rendu HTML des volumes XIII–XV ainsi que leurs entrées dans `search.json` et `sitemap.xml` sont présents sur la branche `main`. Le constructeur `scripts/build_native.py` a été corrigé pour reconnaître le front matter YAML simple (commit `1e5509e011a924751c01946a40e7ed204a062d79`), car les métadonnées étaient précédemment affichées comme texte dans le HTML. Les nouveaux fichiers Markdown restent la source canonique ; vérifier après reconstruction que les métadonnées ne sont plus visibles, que le volume XVI apparaît dans l'index et que GitHub Pages a réellement déployé. **Aucune affirmation de publication publique ne doit précéder ce contrôle.**

- Volume XVII : `chapitres/comedies/volume-017-eupolis-noumeniai.md` (Eupolis, *Noumêniai* ; Lénéennes 425 av. J.-C., troisième prix, **aucun fragment verbal conservé**, hypothèse I des *Acharniens*, calendrier religieux et économique, 27 sections et trois scènes contemporaines [C] ; commit initial `45a231487df34e65cc83ff46fe25cafe3c844722`). Navigation retour depuis XVI ajoutée (commit `6a5de1082f863d5c20e7080d59dfbb9aa635f9c1`). **Prochain numéro XXVIII**, après contrôle du dépôt et de l'indexation. 

- Volume XVIII : `chapitres/comedies/volume-018-eupolis-philoi.md` (Eupolis, *Philoi* ; frr. 286–295 K.-A., datation inconnue, sociabilité et amitié, porte proverbiale, costume, musique, transport, cavalerie, allusions à Aspasie et Lycon, trois scènes originales [C], 30 sections ; commentaire Olson FrC 8.2, p. 438–459 ; commit initial `1f00b19b86c066ab00d2e0543aea84d80f0f3f58`). Lien depuis XVII ajouté par commit `9586a60dc17d6085a61b50e4badfad6a7a94becb`. **Prochain volume : XXVIII**, après vérification de l'indexation et du déploiement. Aucun contenu WordPress modifié.

- Volume XIX : `chapitres/comedies/volume-019-eupolis-taxiarchoi.md` (Eupolis, *Taxiarchoi* ; complément de la notice historique, Phormion, Dionysos, discipline militaire, P.Oxy. 2740, fragments et trois scènes originales [C] ; commit `dee63fdc1346a55cde929bc37125ee6ae500fcb1`). **Prochain volume : XXVIII**, après contrôle de l'indexation et du déploiement.

- Volume XX : `chapitres/comedies/volume-020-aristophane-gerytades.md` (Aristophane, *Gerytades* ; ambassade de poètes, satire de la maigreur, poétique et comparaison avec les *Grenouilles*, deux scènes [C] ; commit initial `64f6b0049b0aab3740fcfe87c78539a564028f24`). **Prochain volume : XXVIII**, après vérification du dépôt et du déploiement.

- Volume XXI : `chapitres/comedies/volume-021-aristophane-amphiaraos.md` (Aristophane, *Amphiaraos* ; consultation héroïque, incubation, limites de la reconstitution, comparaisons philosophiques et deux scènes contemporaines [C] ; commit initial `6a6176e0aff3625e10f409d50a10f39a48089df7`). **Prochain volume : XXVIII**, après vérification du dépôt.

- Volume XXII : `chapitres/comedies/volume-022-aristophane-georgoi.md` (Aristophane, *Geōrgoi* / *Les Paysans* ; dossier sur la terre, la guerre et la citoyenneté, 15 sections, deux scènes originales [C], bibliographie critique ; commit initial `57d2537a6b262dda2b7ee66364924ad0d07e40b7`). **Prochain volume : XXVIII**, après contrôle de la reconstruction et du dépôt.

- Volume XXIII : `chapitres/comedies/volume-023-aristophane-anagyros.md` (Aristophane, *Anagyros* ; tradition de la Souda, héros local, sanction, responsabilité familiale, méthode des lacunes, 23 sections et trois scènes originales [C] ; commit initial `9b9cd652595042b099e83993f8a855f46a398345`). **Prochain volume : XXVIII**, après contrôle du dépôt et de l'indexation.

- Volume XXIV : `chapitres/comedies/volume-024-aristophane-babylonioi.md` (Aristophane, *Babylōnioi* ; Dionysies de 426, Cléon, empire athénien, allusions des *Acharniens*, 19 sections et trois scènes originales [C] ; commit initial `b899c0a197de5bd498d7fd37d66094676bb3ae29`). **Prochain volume : XXVIII**, sous réserve de vérification du dépôt et du déploiement.

- Volume XXV : `chapitres/comedies/volume-025-aristophane-polyidos.md` (Aristophane, *Polyidos* ; dossier critique du mythe de Glaucos, distinctions entre sources mythographiques et fragments comiques, Hegel/Nietzsche/Vernant/Détienne/Dumézil, trois scènes originales [C] ; commit initial `1da2d369f05aa4338f726a009d697887e7d93db9`). **Prochain volume : XXVIII**, après inspection du dépôt, des notices et du déploiement. Aucun fichier WordPress modifié.

- Volume XXVI : `chapitres/comedies/volume-026-aristophane-daidalos.md` (Aristophane, *Daidalos* ; titre attesté d'une comédie perdue, traditions de l'artisan, labyrinthe, statues, responsabilité technique, trois scènes originales [C], distinction stricte entre mythographie et fragments de comédie ; commit initial `2dbbc2134ec2112d2112caf3abc887ecec04d4b6`). **Prochain numéro théorique XXVIII**, après contrôle du dépôt et du déploiement. Aucune publication WordPress.

- Volume XXVII : `chapitres/comedies/volume-027-aristophane-kokalos.md` (Aristophane, *Kôkalos* ; Cocalos, Dédale et Minos, traditions mythographiques distinguées des témoignages dramatiques, analyses de l'hospitalité et du savoir, Hegel/Nietzsche/Vernant/Détienne/Dumézil, trois scènes originales [C] ; commit initial `660e3eaf6fca159967ae3919df348d356bf8a84f`). **Prochain numéro théorique XXVIII**, après inspection du dépôt et du déploiement. WordPress inchangé.

- Volume XXVIII : `chapitres/comedies/volume-028-aristophane-aiolosikon.md` (Aristophane, *Aiolosikōn* ; dossier critique sur les traditions d'Éole, la parodie d'Euripide, la parenté, deux scènes originales [C] ; commit initial `d3dff2b0f512a8f195fcd59d4e100ced06853bec`). **Prochain volume théorique : XXIX**, après contrôle du dépôt et de l'indexation.

- Volume XXIX : `chapitres/comedies/volume-029-aristophane-holkades.md` (Aristophane, *Holkades* ; navires marchands, Pirée, circulation et puissance athénienne, 19 sections, trois scènes originales [C], témoignages [A] et hypothèses [B] séparés ; commit initial `23d1db97cde3493a6844cf9524ec64fb6c40fb76`). **Prochain volume théorique XXX**, après inspection du dépôt et des notices.

- Volume XXX : `chapitres/comedies/volume-030-aristophane-lemniai.md` (Aristophane, *Lemniai* / *Les Lemniennes* ; 22 sections, mythes de Lemnos et Hypsipyle, distinctions strictes entre témoignages [A], hypothèses [B] et trois scènes contemporaines [C] ; commit initial `dc682272c339c54cae4beaaa79b3c2faa3eb7057`). **Prochain numéro théorique XXXI**, après inspection du dépôt et des notices.

- Volume XXXI : `chapitres/comedies/volume-031-aristophane-geras.md` (Aristophane, *Gēras* / *La Vieillesse* ; 22 sections, âge, famille, citoyenneté et mémoire, distinction [A]/[B]/[C], trois scènes originales ; commit initial `9319314ac644374d36c66170de7e4da1b698a08a`). **Prochain numéro théorique XXXII**, après contrôle du dépôt et de l'indexation.

- Volume XXXII : `chapitres/comedies/volume-032-aristophane-ploutos-protos.md` (Aristophane, premier *Ploutos* perdu, distinct de la pièce conservée de 388 ; 22 sections, richesse et justice distributive, trois scènes originales [C], distinction [A]/[B]/[C] ; commit initial `1f03a13896ebd29e66904ba034a28c279f89610a`). **Prochain numéro théorique XXXIII**, après inspection du dépôt et du catalogue.

- Volume XXXIII : `chapitres/comedies/volume-033-aristophane-triphales.md` (Aristophane, *Triphalēs* ; 22 sections, corps comique, obscénité et pouvoir, philologie du titre, trois scènes originales [C] distinctes des témoignages [A] et hypothèses [B] ; commit initial `3b9cf99ced6bd186b8cf7029859c9ae64235f3d2`). **Prochain numéro théorique XXXIV**, après contrôle du dépôt et de l'indexation.

- Volume XXXIV : `chapitres/comedies/volume-034-aristophane-horai.md` (Aristophane, *Hōrai* / *Les Saisons* ; 25 sections, philologie de ὥρα, Hésiode, calendrier et temporalités civiques, comparaisons philosophiques, trois scènes originales [C] ; sources [A] et hypothèses [B] séparées ; commit initial `f59d76f6588307c6699485faa933ec4164f19400`). **Prochain numéro théorique XXXV**, après inspection du dépôt et du catalogue.

- Volume XXXV : `chapitres/comedies/volume-035-aristophane-proagon.md` (Aristophane, *Proagōn* ; 24 sections, concours dramatiques, philologie du titre, rivalité poétique et limites des reconstructions, trois scènes originales [C] séparées des attestations [A] et interprétations [B] ; commit initial `323e5a0485791a306a880296e14e6c478cf5ffce`). **Prochain numéro théorique XXXVI**, après vérification du dépôt et de l'indexation.

- Volume XXXVI : `chapitres/comedies/volume-036-aristophane-phenissai.md` (Aristophane, *Phoinissai* / *Les Phéniciennes* ; 24 sections, mythes thébains, Cadmos, Euripide, altérité et guerre civile, trois scènes originales [C] distinctes des attestations [A] et hypothèses [B] ; commit initial `a043e17a3655d93b35eb5e1e8d3d44056ec5c681`). **Prochain numéro théorique XXXVII**, après vérification du dépôt et du catalogue.

- Volume XXXVII : `chapitres/comedies/volume-037-aristophane-telmessioi.md` (Aristophane, *Telmessioi* / *Les Telmessiens* ; 25 sections, Hérodote I, 78, divination, interprétation des signes, autorité et comparaisons philosophiques, trois scènes originales [C] distinctes des attestations [A] et hypothèses [B] ; commit initial `b27bf266ac486cdcc557f2f2687b27ff9f4d898d`). **Prochain numéro théorique XXXVIII**, après contrôle du dépôt et du catalogue.

- Volume XXXVIII : `chapitres/comedies/volume-038-cratinos-dionysalexandros.md` (Cratinos, *Dionysalexandros* ; 27 sections, P.Oxy. IV 663, jugement des déesses, Pâris, Hélène, satire de Périclès, trois scènes originales [C] séparées des attestations [A] et analyses [B] ; commit initial `45dee88cb535d990d523bc07df20ef3e0b3a053e`, correction bibliographique `19998fe2f7b3309061074cb2e4d8a6a6ba3016d5`). **Prochain numéro théorique XXXIX**, après contrôle du dépôt et du catalogue.

- Volume XXXIX : `chapitres/comedies/volume-039-cratinos-pytine.md` (Cratinos, *Pytinē* / *La Bouteille* ; 27 sections, victoire de 423, rivalité avec Aristophane, personnification de la Comédie, métathéâtre et trois scènes originales [C] séparées des sources [A] et hypothèses [B] ; commit initial `7c387ab08500955577c1927ea7b4b77f7a8a89cf`). **Prochain numéro théorique XL**, après contrôle du dépôt et de l'indexation.

- Volume XL : `chapitres/comedies/volume-040-cratinos-satyroi.md` (Cratinos, *Satyroi* / *Les Satyres* ; 27 sections, chœur, Dionysos, corps, drame satyrique et comédie, trois scènes originales [C] séparées des sources [A] et hypothèses [B] ; commit initial `b599e4687443c57e48f505e90c8bf02d9a034353`). **Prochain numéro théorique XLI**, après vérification du dépôt et de l'indexation.

- Révision du volume XL : enrichissement critique de `chapitres/comedies/volume-040-cratinos-satyroi.md`, sections 28–36, distinction renforcée entre iconographie, drame satyrique et comédie, protocole de collation des fragments et quatrième scène originale [C] ; commit `55bdd1f78e7c433aec27ab634db8e0b8d6ec46ca`. Aucun nouveau numéro créé ; prochain volume théorique XLI, à déterminer après vérification des attestations et des doublons.

- Volume XLI : `chapitres/comedies/volume-041-hermippos-artopolides.md` (**Hermippos, *Artopōlides* / *Les Marchandes de pain*** ; 33 sections de monographie plus thèse liminaire, env. 4 600 mots ; corpus primaire fr. 7–12 K–A, *Nuées* 553–557 et scholies, Peisandros, Hyperbolos, travail féminin, invective, lectures philosophiques et trois scènes originales [C] séparées des attestations [A] et hypothèses [B] ; sources critiques PCG V (1986), Comentale FrC 6 (2017), Dover OCD, Sonnino (2012), Schofield Klos (2012) ; nouveau fichier commit `3fe91a2629bef06b29c0539f97d99c48db16de9c`, liens de site corrigés commit `c6438480ae9a932406d0bd2818d5df60297373e3`). Le volume XL renvoie au XLI par le lien public du dossier (commit `898e4c896d0fda68cfdcddb74923062f3b95756a`). **Prochain numéro théorique XLII**, uniquement après inspection des volumes, index et notices historiques. La construction du site public doit être vérifiée séparément du commit GitHub. Aucun contenu WordPress ni brouillon privé n'est utilisé.

- Volume XLII : `chapitres/comedies/volume-042-hermippos-moirai.md` (Hermippos, *Moirai* ; 20 sections, fragments 46–49 K.-A., attribution disputée du fragment 47, Nothippos, armement, hypothèse d'une armée de satyres, deux scènes originales [C], sources Comentale FrC 6 ; commit initial `72ef3bbe58069d40e1b5b75d9c74ba4cb47f8379`). **Prochain numéro théorique XLIII**, après contrôle du dépôt et de l'indexation.

- Volume XLIII : `chapitres/comedies/volume-043-hermippos-stratiotai.md` (Hermippos, *Stratiōtai* / *Les Soldats* ; 19 sections, variantes Stratiōtai/Stratiōtides, fragments 51–59 K.-A., proverbe du fragment 58 et commentaire Tammaro 2023, deux scènes originales [C] ; commit initial `b35f45b5f0c7123f65c36df4e863e24e3033b3eb`). **Prochain numéro théorique XLIV**, après vérification du dépôt et de l'indexation.

- Révision du volume XLIII : `chapitres/comedies/volume-043-hermippos-stratiotai.md`, ajout des sections XX–XXIX (critique des titres, transmission, proverbe 58, guerre/agriculture, comparaisons et troisième scène originale [C]), commit `18dd5558eaaa456ff8b0aa737eae9b90d0dae905`. Aucun nouveau volume créé ; numéro suivant à déterminer après contrôle de la série, actuellement XLIV théorique.

- Volume XLIV : `chapitres/comedies/volume-044-hermippos-phormophoroi.md` (Hermippos, *Phormophoroi* / *Les Porteurs* ; 24 sections, fragment 63 K.-A., Athénée, Eustathe et Hésychios, catalogue des importations méditerranéennes, trois scènes originales [C] ; commit initial `a22bd222bbd9c0d037e45f157defeb4152becdfa`). **Prochain volume théorique XLV**, après contrôle du dépôt et de l'indexation.

- Volume XLV : `chapitres/comedies/volume-045-hermippos-athenas-gonai.md` (Hermippos, *Athēnas gonai* / *La Naissance d'Athéna* ; **35 sections, environ 5 050 mots**, fragments 2–6 K.-A., mention disputée de fr. 73, transmission Photios/Souda, textile, Heures, Accô, analyses philosophiques et comparatives [B], trois scènes originales [C] séparées des sources [A] ; consultation des pages 47–64 de N. Comentale, *Fragmenta Comica* 6 ; commit initial `66013e154941334c490c01ae9b65e846f16a84f0`). Catalogue et déploiement public à vérifier séparément. **Prochain volume théorique XLVI**, sous réserve du contrôle des titres, notices anciennes et fichiers GitHub ; ne pas créer de doublon.

- Volume XLVI : `chapitres/comedies/volume-046-hermippos-kerkopes.md` (Hermippos, *Kerkōpes* / *Les Cercopes* ; 23 sections, dossier critique fondé sur Comentale, *FrC* 6, p. 143–158, fragment 36 K.-A. et distinction des parallèles mythographiques ; analyses Hegel, Nietzsche, Vernant/Détienne, limites de Dumézil, trois scènes originales [C], séparation [A]/[B]/[C] ; commit initial `fd36abacbccabd6879049563b9da891a55c289b5`). **Prochain numéro théorique XLVII** sous réserve de contrôle des notices et de la publication. Ne pas confondre commit Markdown, reconstruction de l'index et déploiement public.

- Volume XLVII : `chapitres/comedies/volume-047-hermippos-demotai.md` (Hermippos, *Dēmotai* / *Les Membres du dème*, **35 sections, environ 4 685 mots**, frr. **13–22 K.-A.**, Pollux, Athénée, Antiatticiste, Eustathe, Photios/Souda, analyse de la citoyenneté, du voisinage et des proverbes ; 3 scènes originales [C] ; distinction [A]/[B]/[C], confrontation explicite avec *Dēmoi* d'Eupolis sans confusion ; commentaire N. Comentale, *FrC* 6, 2017, p. 84–99 ; commit initial `fca4891828d4265d71eb86cba90aa0d6e0ea9c67`). **Prochain numéro théorique XLVIII** après inspection du dépôt et vérification du catalogue et du déploiement public. Aucun brouillon privé ni document WordPress utilisé.

## Point de reprise des comédies — 3 novembre 2026 : volume XLVIII

- Volume XLVIII : `chapitres/comedies/volume-048-hermippos-theoi.md` (**Hermippos, *Theoi* / *Les Dieux*** ; 32 sections, examen des douze numéros de fragments **24–35 K.-A.**, tableau des témoins antiques, vin, procession, lampes, jeux, gages, parole sacrée et transmission lexicographique ; analyses historiques et philologiques, lectures comparées de Hegel, Nietzsche et Vernant, trois scènes originales [C] séparées des sources [A] et hypothèses [B] ; bibliographie distinguant la dissertation de Comentale effectivement consultée et l'édition *FrC* 6, 2017, p. 104–142 identifiée bibliographiquement ; commit de création `5bb5519da3bb9aa98e9e8012c49f1be1ae713854`).
- Navigation réciproque XLVII–XLVIII enregistrée ; mise à jour du volume XLVII par commit `7c59e6c9ba2a47d2f5f0fcf5a1800e01a2e008e0`. La révision ne change que trois lignes de navigation, conserve le corps de l'étude et utilise les chemins publics `/chapitres/comedies/.../` plutôt que des liens Markdown relatifs inadaptés au rendu en sous-répertoire.
- Contrôle initial du 3 novembre : les volumes XIII, XLVI et XLVII sont présents dans le répertoire des comédies, dans `search.json` et dans `sitemap.xml` sur `main`. Le volume XLVII existait déjà avant cette exécution et n'a pas été recréé. La recherche du titre *Theoi* dans le dépôt et les notices indexées n'a trouvé, avant création, que des mentions de suite possible.
- Les tentatives de lecture HTTPS de `bobmythos.fr` n'ont pas permis de vérifier le rendu public. Cette limitation du contrôle ne démontre pas une panne du site. Pour XLVIII : **version GitHub enregistrée, publication non vérifiée** ; contrôler séparément le HTML généré, le catalogue, le sitemap, le workflow et la page publique à la prochaine reprise.
- **Prochain numéro théorique : XLIX**, uniquement après nouvelle inspection de `chapitres/comedies/`, des notices historiques et des éventuelles livraisons non archivées. Les indications « prochain volume » plus anciennes restent des jalons historiques, non le point de reprise actuel. Aucun fichier ni texte antérieur supprimé ; aucune publication WordPress ; aucun brouillon privé utilisé.

## Point de reprise des comédies — 3 novembre 2026 : volume XLIX

- **Volume XLIX** : `chapitres/comedies/volume-049-hermippos-europe.md` (**Hermippos, *Eurōpē* / *Europe***), 35 sections, environ 4 700 mots, unique fragment transmis **23 K.-A.**, Photios et Souda, leçon `ῥύζων`, variantes textuelles, ambiguïté de l'objet « doigts », comparaisons avec Homère, Hérodote, Eschyle, Platon le Comique et Euboulos, analyses Hegel/Nietzsche/Vernant/Détienne, justification du non-recours à une grille dumézilienne, 3 scènes contemporaines [C]. Chaque section distingue [A] attestations, [B] hypothèses, [C] créations. Source critique consultée directement : N. Comentale, *Fragmenta Comica* 6 (2017), p. 100–103 (https://digi.hadw-bw.de/view/frc6/0104 à /0107). **Commit de création : `c468631998a0e5635ef14e29eedf6abdf9608524`.**
- Vérification préalable : le dépôt `main` comporte les Markdown de la série I–XLVIII, sans volume XLIX ; le volume XIII `volume-013-eupolis-demoi` possède un HTML généré et figure dans `search.json` et `sitemap.xml`. Contrôle des notices historiques indexées et des titres homonymes : pas de notice publique déjà consacrée à l'*Eurōpē* d'Hermippos, à distinguer expressément des œuvres homonymes de Platon le Comique et d'Euboulos.
- Navigation XLVIII → XLIX actualisée sans retrait du corps de l'étude précédente : commit `6b95bfa53d61e746d51bdf68c3e635c1c3a57764`. Le volume XLIX renvoie à XLVIII et aux portails généraux.
- **Prochain numéro théorique : L**, uniquement après nouvelle inspection de `EDITORIAL_CONTINUITY.md`, de `chapitres/comedies/`, des notices historiques et d'éventuelles livraisons non archivées ; prochain titre éventuel dans Comentale, *Agamemnōn* (p. 43–46), sous réserve du même contrôle de l'attribution et des doubles entrées.
- **Statut de publication :** l'enregistrement GitHub et la reconstruction du catalogue et du sitemap sont deux étapes distinctes ; le rendu HTTPS de bobmythos.fr est à confirmer. Ne jamais annoncer « publié sur le site » sans test indépendant. Aucune suppression, aucun brouillon privé, aucune publication WordPress.

## Point de reprise des comédies — 3 novembre 2026 : volume L

- **Volume L** : `chapitres/comedies/volume-050-hermippos-agamemnon.md` (**Hermippos, *Agamemnōn* / *Agamemnon***), 25 sections, fragment **1 K.-A.** transmis par le *Lexicon Messanense*, examen de la lacune et des suppléments éditoriaux, origine, identité, autorité et vérité ; comparaisons distinctes avec Homère, Eschyle, Nicocare, Platon, Plutarque, Hegel et Nietzsche ; trois scènes originales [C]. Le texte, les hypothèses éditoriales et les créations restent séparés. **Commit de création contrôlé dans l'historique du fichier : `e9884307b1f54e6b606982df5230ba07e59d3882`.**
- Source effectivement consultée : transcription numérique de la dissertation de N. Comentale, *Ermippo comico*, 2015–2016, p. 23–25. L'édition publiée *FrC* 6, 2017, p. 43–46, est identifiée et son ouverture contrôlée ; aucune collation intégrale des quatre images ni du manuscrit médiéval n'est revendiquée. Le supplément `⟨με⟩` est expressément présenté comme proposition de la dissertation, non comme leçon garantie du témoin ou choix automatiquement attribué à PCG.
- Contrôle préalable : XLIX existait déjà ; aucun fichier du volume L n'existait à l'adresse choisie. Recherche des notices historiques et distinction des *Agamemnon* d'Eschyle et de Nicocare. Aucun texte non archivé supplémentaire de cette série n'a été retrouvé lors du contrôle de continuité disponible.
- Navigation réciproque XLIX–L enregistrée. L'ajout dans XLIX est vérifié par le commit `8ac66ed6e903f31fba7b873c74afb271a8e3ec7c` : deux lignes ajoutées, aucune supprimée. Le corps de l'étude précédente et son ancien jalon théorique sont conservés ; le renvoi nouveau actualise explicitement ce jalon.
- **Reconstruction GitHub vérifiée :** les volumes XIII et L figurent dans `search.json` et `sitemap.xml` ; leurs fichiers `index.html` existent sur `main`, avec titres et contenu. Le rendu initial du volume L conserve la séparation [A]/[B]/[C] et le lien public de retour vers XLIX. Cette vérification des fichiers générés n'est pas une vérification du service HTTPS.
- Les lectures publiques des pages XIII et L sur `bobmythos.fr` n'ont pas abouti avec l'outil disponible ; cela ne démontre pas une panne du site. **Version GitHub enregistrée, publication non vérifiée.** Recontrôler le déploiement indépendamment à la prochaine reprise.
- **Prochain numéro théorique : LI**, uniquement après nouvelle inspection du dépôt, des notices et des éventuelles livraisons non archivées. Les indications antérieures de prochain numéro restent historiques. Aucun titre futur réservé, aucun fichier supprimé, aucune publication WordPress, aucun brouillon privé utilisé.
