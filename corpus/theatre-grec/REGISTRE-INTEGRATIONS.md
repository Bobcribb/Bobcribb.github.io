# Théâtre grec — Registre des intégrations contrôlées

## 3 novembre 2026 — *Triphalēs* (Aristophane), comédies grecques XXXIII

**Provenance :** [manuscrit historique complet](https://github.com/Bobcribb/Bobcribb.github.io/blob/dedd1e488dd4300479e2c430f7ce435f7fe4b136/chapitres/comedies/volume-033-aristophane-triphales.md), blob Git `d59cac3b1838b36b3879e9bcfd4f12c9e4bc7ad4`, 12857 octets, préambule et 22 sections. [Copie exacte](comedies/triphales-source.md), sans intervention sur l'archive d'origine. Aucun lecteur Triphalēs publié dans le dépôt courant avant cette intégration.

**Publication éditoriale :** [TH-03-TRI, étude critique](comedies/triphales-etude.html) = sections 1–17, 21 et 22 (19 sections, sources et bibliographie incluses) ; [TH-02-TRI, scènes modernes](comedies/triphales-scenes-modernes.html) = 18–20, sans attribution antique. Texte visible de 22 sections et introduction comparés avec le rendu historique, sans raccourcissement. Contrôle de fidélité automatisé ; aucune collation philologique indépendante n'est revendiquée.

**Interface :** sommaires, liens réciproques depuis *Ploutos I*, accueil, Théâtre, Philosophie et sommaire général ; bannière statue/temple, thème noir/or, figure schématique et responsive. Archives et autres automatisations préservées. Déploiement public à confirmer.


## 3 novembre 2026 — Ploutos I, comédies grecques XXXII (TH-COM-PL1)

Source complète : [manuscrit du dépôt historique](https://github.com/Bobcribb/Bobcribb.github.io/blob/f740d6a4ef3b02d30f9e41cafbc5a9b640c8f5dc/chapitres/comedies/volume-032-aristophane-ploutos-protos.md), commit `f740d6a4ef3b02d30f9e41cafbc5a9b640c8f5dc`, blob Git `83d0ebf6f67e6092baf27d120b7440fea65d3d8a`. Copie identique dans [ploutos-protos-source.md](comedies/ploutos-protos-source.md) : 12319 octets, 11931 caractères. Aucun dossier Ploutos I publié auparavant dans `Bobcribb/Mythos` au commit `40cc6bad5b6f` : la référence depuis Gēras était un lien vers l'archive historique.

**TH-03-PL1** : [étude critique](comedies/ploutos-protos-etude.html), préambule et 19 sections (1–16 et 20–22), bibliographie complète. **TH-02-PL1** : [scènes modernes](comedies/ploutos-protos-scenes-modernes.html), trois créations [C] (17–19), non attribuées à Aristophane.

Contrôle éditorial : copie source exacte ; 22/22 sections comparées en texte visible avec le Markdown d'origine, répartition sans omettre ni répéter de section. Accueil, Théâtre, Philosophie, sommaire général et liens réciproques depuis Gēras mis à jour. Mise en page noir/or, bannière statue/temple, cartes illustrées, repères 408/388 et styles responsives. Le texte original et toutes les archives restent conservés. La comparaison de texte ne constitue pas une collation philologique ; publication publique à confirmer dans Actions.


## 3 novembre 2026 — Daidalos, dossier TH-COM-DAI

### Source et statut antérieur

Source intégralement lue : `Bobcribb/Bobcribb.github.io`, `chapitres/comedies/volume-026-aristophane-daidalos.md`, version `f865cd391413301f9f2788c2caf4026c257a28c4`.

Ce manuscrit existait déjà dans le dépôt historique. Il s'agit d'une **nouvelle intégration dans Bobcribb/Mythos**, non d'une nouvelle rédaction ni de la découverte d'un texte antique. Avant cette intégration, la rubrique `theatre-grec.html` de Mythos ne proposait que des entrées d'inventaire ; aucune page Daidalos n'y était présente.

Archive locale exacte : [daidalos-source.md](comedies/daidalos-source.md). Taille : **18 594 octets, 18 028 caractères, 202 lignes**. Empreinte Git de la source originale et de la copie : **7e700ab6e72f26208e47d6e3eb600e41f95af78c**. SHA-256 : `a60bd8b676b534e3ff444823112f50acd04847905a671575b191e7dc1966f4c1`.

### Classement sans mélange des genres

- **TH-03-DAI — Étude critique** : sections I–XVII, XXI–XXII ; 19 sections, dont le bilan et la bibliographie. Lecture : `comedies/daidalos-etude.html`.
- **TH-02-DAI — Scènes modernes** : sections XVIII–XX ; trois créations contemporaines explicitement signalées comme non antiques. Lecture : `comedies/daidalos-scenes-modernes.html`.

Les 22 sections et le préambule sont conservés sans résumé. Une comparaison locale indépendante avec MarkdownIt et BeautifulSoup a confirmé l'identité de tous les textes lisibles de section : **22/22**. Le classement du site ne remplace pas les numéros historiques, conservés comme métadonnées de provenance. Les deux parcours ont des liens réciproques ; la bibliographie reste unique dans l'étude.

### Publication reproductible

`python3 scripts/build-daidalos.py` produit les deux pages HTML statiques et `daidalos-controle.json` dans le répertoire des sources, avant l'envoi de l'artefact GitHub Pages. **Les pages sont générées au déploiement** : le texte maître est le Markdown versionné, jamais une copie abrégée. Le script ne dépend ni du réseau ni de bibliothèques tierces. Une empreinte source inattendue, une section absente, un mauvais classement [C] ou une ancre locale manquante bloque la génération.

Les entrées Théâtre et Philosophie renvoient au même dossier. L'étude est classée parmi les analyses liées aux pièces, pas parmi les études philosophiques autonomes. Le sommaire général préexistant ouvre déjà la rubrique Théâtre ; chaque lecteur retourne également au sommaire général.

### Graphisme et contrôles

Nouveau lecteur noir et or, motif existant `assets/mythos-hero.svg` (statue stylisée à gauche, temple à droite), deux cartes illustrées, sommaire repliable, repères de focus, largeur de lecture limitée et styles d'impression. Les motifs sont décoratifs, **pas des restitutions archéologiques**.

Rendus locaux inspectés en Chromium à 360, 390, 768 et 1 440 pixels, sur les deux pages : huit tests sans débordement horizontal. Les ressources locales ont été incorporées au document de test afin de ne pas utiliser de réseau ; ce contrôle ne prouve pas l'affichage du domaine public.

### Limites explicites

Le contrôle établit la fidélité au manuscrit et sa répartition, pas une validation scientifique exhaustive. Les réserves du manuscrit sur la collation des fragments et l'interprétation moderne sont conservées. Aucune nouvelle scène n'a été inventée pendant cette intégration. Le succès du déploiement doit être vérifié séparément dans GitHub Actions ; l'accès indépendant à bobmythos.fr n'est pas certifié par ce registre.

Les tomes des Origines du sacré déjà intégrés, tous les anciens textes et toutes les archives demeurent inchangés. Aucun autre dépôt n'a été modifié. Aucune programmation horaire MYTHOS n'a été changée.

## 3 novembre 2026 — Polyidos, dossier TH-COM-POL

### Source et conservation

Source : `Bobcribb/Bobcribb.github.io`, `chapitres/comedies/volume-025-aristophane-polyidos.md`, version `fafe12416fc918d2576116cd0a4e0a9a2836ee11`. Manuscrit préexistant, absent de la collection Théâtre du dépôt cible lors du contrôle ; nouvelle intégration dans Mythos, non nouvelle rédaction.

[Manuscrit source intégral](comedies/polyidos-source.md) : **16 288 octets, 15 806 caractères, 165 lignes, 19 sections**. Empreinte Git originale et copie : `46c2cd20c5d797aee436bd83b429a8ffeef0e76b`. SHA-256 : `02e0491573f1f495cf993124f5bf45a7b564c776368ff09de37bc19df53885e2`.

### Lectures et classement

- **TH-03-POL** : [étude critique](comedies/polyidos-etude.html), sections I–XIII et XVII–XIX, soit 16 sections, préambule, bibliographie et conclusion conservés.
- **TH-02-POL** : [scènes modernes](comedies/polyidos-scenes-modernes.html), sections XIV–XVI, soit trois dialogues contemporains expressément non antiques.

Aucune section n'est abrégée, omise ou publiée deux fois dans les lecteurs. Les repères du volume source XXV sont conservés. La copie Markdown contient aussi le front matter et les liens historiques originaux. Les URL de navigation sont adaptées uniquement dans le rendu, avec renvoi aux archives historiques pour les dossiers non transférés.

### Génération, navigation et graphisme

`python3 scripts/build-polyidos.py`, après `build-daidalos.py`, génère les deux lecteurs et le rapport technique. Il insère les cartes dans Théâtre, le renvoi dans Philosophie parmi les analyses liées aux pièces, l'entrée au sommaire général et les liens réciproques depuis Daidalos. Ces ajouts sont produits dans l'artefact Pages : les sources HTML préexistantes restent conservées dans Git. Une seconde génération ne crée aucun doublon.

Bandeau noir et or avec le SVG existant (statue stylisée à gauche, temple à droite), cartes illustrées décoratives, raccourcis vers texte/bibliographie/source, sommaire repliable et zones de navigation tactile d'au moins 44 pixels dans le lecteur. Aucun visuel n'est présenté comme une reconstitution archéologique.

### Contrôles et limites

Comparaison indépendante locale avec MarkdownIt et BeautifulSoup : **19 sections sur 19 et préambule identiques en texte lisible**. Empreinte source exacte, séparation des trois sections [C], ancres, absence de doublons et idempotence contrôlées. Huit essais Chromium sur les deux lecteurs, à 360, 390, 768 et 1 440 pixels : aucun débordement horizontal, premier lien du sommaire fonctionnel. [Résultats locaux](comedies/polyidos-verifications-locales.json).

Les essais locaux incorporent les CSS et le SVG exacts du dépôt ; les pages de destination hors lecteurs sont des fixtures locales et ne prouvent pas le déploiement. GitHub Actions vérifie séparément les vrais fichiers de destination et les ancres, puis publie l'artefact. Le rapport `comedies/polyidos-controle.json` est généré à cette étape. La comparaison de texte ne constitue pas une collation scientifique exhaustive des fragments. La disponibilité du domaine public doit être confirmée indépendamment du succès de Pages.

Toutes les archives précédentes restent conservées. Aucun autre dépôt ni aucune programmation MYTHOS n'a été modifié.


## 3 novembre 2026 — Kôkalos, volume XXVII, dossier TH-COM-KOK

### Source et transfert
Source historique : `Bobcribb/Bobcribb.github.io/chapitres/comedies/volume-027-aristophane-kokalos.md`, blob Git `346275f9a6ea5d889f02060123fe8da981445d5a`. Avant transfert, aucun `kokalos-source.md` ni lecteur `kokalos-*.html` n'existait dans l'arbre du dépôt `Bobcribb/Mythos` contrôlé.

Archive conservée textuellement : [kokalos-source.md](comedies/kokalos-source.md), **17 835 caractères** (176 lignes par découpage textuel), avec front matter et 22 sections. Ce document est une **étude moderne d'une comédie perdue**, non un texte authentique d'Aristophane.

### Classement
- **TH-03-KOK** : [étude historique, philologique et philosophique](comedies/kokalos-etude.html), préambule et sections **1 à 16 puis 20 à 22** (19 sections). Bibliographie et protocole de vérification conservés, avec les réserves de source.
- **TH-02-KOK** : [trois scènes modernes](comedies/kokalos-scenes-modernes.html), sections **17 à 19** du même manuscrit, explicitement signalées comme créations contemporaines.
- Les deux lectures ont des liens réciproques et un lien vers le Markdown source. Chacun des 22 identifiants de section a été relu dans GitHub : **22/22 présents dans un seul des deux lecteurs**.
- Entrées ajoutées à `theatre-grec.html`, `philosophie.html` (analyse seulement) et `sommaire-general.html`. Les pages utilisent le thème sombre et doré, le fichier CSS théâtral existant, son motif local de statue et temple, des sommaires cliquables et une mise en page mobile.

### Limites
La fidélité de l'archive et la répartition de ses sections ont été contrôlées par relecture GitHub. Les paragraphes dans les lecteurs sont affichés avec leur syntaxe Markdown d'origine pour éviter toute reformulation ; ce n'est pas une nouvelle édition philologique. Ni la collation exhaustive des sources anciennes ni le rendu visuel et le déploiement effectif sur le domaine public n'ont été certifiés dans cette intervention. Aucun ancien manuscrit n'a été écrasé, aucun autre dépôt ni aucune automatisation MYTHOS n'a été modifié.


## 3 novembre 2026 — *Aiolosikōn* d'Aristophane, volume historique XXVIII — TH-COM-AIO

### Contrôle d'antériorité, provenance, intégralité
Avant le transfert, le fichier `aiolosikon-source.md` et les deux lecteurs `aiolosikon-*.html` étaient absents du catalogue des fichiers de `Bobcribb/Mythos` ; une archive du dossier existait dans `Bobcribb/Bobcribb.github.io/chapitres/comedies/volume-028-aristophane-aiolosikon.md`. Manuscrit historique : **blob Git `e4b75423fe8691c74594b31b4af5a158da64b947`**. Le même blob a été retrouvé après copie dans `corpus/theatre-grec/comedies/aiolosikon-source.md` : **11 173 caractères, 17 sections numérotées I à XVII**. Il s'agit d'un **travail universitaire moderne sur une comédie perdue**, non d'une restitution antique authentique.

### Classement, deux lectures sans doublons
- **TH-03-AIO**, [étude intégrale](comedies/aiolosikon-etude.html) : sections I–XII puis XV–XVII, soit **15 sections**, avec introduction méthodologique et texte complet de la section XVII « Sources primaires et bibliographie de vérification ». Thèmes : titre et lacunes, traditions d'Éole, tragédie perdue d'Euripide, parenté, normes familiales et comparaisons Hegel, Nietzsche, Vernant, Détienne et Dumézil.
- **TH-02-AIO**, [créations modernes](comedies/aiolosikon-scenes-modernes.html) : sections XIII–XIV, soit **deux scènes** préexistantes au transfert. Les personnages et répliques sont explicitement modernes et jamais attribués à Aristophane.
- La [copie source](comedies/aiolosikon-source.md) conserve sans altération l'ensemble du manuscrit et ses liens historiques. Les liens source internes de l'interface renvoient au vrai classement MYTHOS ; le lien vers le tome XXIX non encore intégré renvoie expressément au dépôt historique, non à une fausse page MYTHOS.
- Chaque section apparaît dans **une seule des deux lectures**. Un contrôle préalable à l'écriture a comparé, pour **17/17 sections**, le texte lisible des paragraphes HTML au texte Markdown d'origine après seule suppression des marqueurs de style Markdown. Les sources citées et les réserves de collation sont conservées.

### Graphisme et circulation
Utilisation de `assets/mythos-theatre.css` et du motif décoratif local `assets/mythos-hero.svg` (statue grecque à gauche, temple à droite) ; lecteur sombre à filets dorés, sommaire latéral ancré, mode mobile et liens clavier, styles d'impression. Cartes illustrées ajoutées à `theatre-grec.html` et `philosophie.html`, entrée au `sommaire-general.html` et à l'accueil. Navettes entre étude et scènes, renvoi vers le volume XXVII `Kôkalos`, et renvoi réciproque depuis le lecteur de Kôkalos. Le sommaire général avait une ouverture d'article HTML manquante autour de la carte Philosophie ; correction effectuée au passage.

### Contrôle continu et limites
Le vérificateur `python3 scripts/check-aiolosikon.py` recalcule l'empreinte Git du manuscrit (byte-for-byte), confronte le texte lisible des 17 sections et le préambule aux pages HTML, contrôle les ancrages et les fichiers des liens locaux, et produit `aiolosikon-controle.json`. L'étape est insérée avant la publication dans `.github/workflows/pages.yml` ; elle bloque le déploiement en cas de régression. Cette intégration **ne constitue pas une collation philologique indépendante** des textes antiques, ni une attestation d'affichage du domaine public avant le succès de Pages. Aucune suppression de fichier ou modification des autres automations MYTHOS.


## 3 novembre 2026 — *Holkades* (Aristophane), volume historique XXIX

### Source intégrale, contrôle préalable et provenance

Le manuscrit existait dans le dépôt historique `Bobcribb/Bobcribb.github.io`, sous le chemin `chapitres/comedies/volume-029-aristophane-holkades.md`, avec le blob Git `775999ca4ba7bbeb668802eb8b7dfc7f56643a93`. Le contrôle de l'arbre du dépôt `Bobcribb/Mythos` avant transfert n'identifiait ni `holkades-source.md` ni les deux pages `holkades-*.html` : il s'agit d'une **nouvelle intégration sur MYTHOS**, non d'une nouvelle composition ni d'une découverte de vers antiques.

- **Archive complète** : [holkades-source.md](comedies/holkades-source.md), copie textuelle sans réécriture, **12 387 caractères**, 19 sections numérotées, front matter, préambule, bibliographie et notes finales conservés.
- **TH-03-HOL — Étude critique** : [holkades-etude.html](comedies/holkades-etude.html), **16 sections** (1–14 et 18–19), avec préambule, sources antiques, analyses et bibliographie.
- **TH-02-HOL — Scènes littéraires contemporaines** : [holkades-scenes-modernes.html](comedies/holkades-scenes-modernes.html), **3 sections** (15–17) explicitement identifiées comme créations modernes. Ces scènes ne constituent ni fragments grecs ni reconstitutions certifiées d'Aristophane.

### Relecture et navigation

Les 19 sections ont été confrontées au manuscrit d'origine : le texte lisible après interprétation des marques Markdown correspond au texte des deux parcours sans résumé, omission ou duplication. Les liens historiques du préambule vers Théâtre et Philosophie ont été adaptés aux rubriques effectives ; le volume XXVIII pointe vers l'étude `aiolosikon-etude.html`, tandis que le volume XXX, non encore migré, pointe explicitement vers le dépôt historique. Le fichier source conserve **tous ses liens initiaux**.

Les nouvelles pages utilisent `assets/mythos-theatre.css` et `assets/mythos-hero.svg` (bandeau sombre à statue stylisée gauche, temple droite). Elles présentent des sommaires cliquables, navigation sur téléphone, sources en accès direct, bibliographie et liens réciproques entre étude et créations. Des cartes illustrées et liens ont été ajoutés dans `theatre-grec.html`, `philosophie.html` (étude seulement), `sommaire-general.html`, `corpus/sommaire-general.md` et `index.html`. Le lecteur du volume précédent `aiolosikon-etude.html` renvoie au volume XXIX.

Le script [check-holkades.py](../../scripts/check-holkades.py), déclenché avant publication par `.github/workflows/pages.yml`, vérifie l'empreinte exacte du manuscrit, la partition des 19 sections, l'identité des textes lisibles et du préambule, les ancres, la présence des fichiers cibles et les liens de navigation. Il bloque le déploiement en cas de régression et produit `holkades-controle.json` dans l'artefact Pages.

### Limites scientifiques et techniques

Le contrôle porte sur la fidélité de l'intégration et le fonctionnement des liens, **non** sur la collation philologique exhaustive de *Poetae Comici Graeci* III.2. Aucune réplique nouvelle n'a été ajoutée. Le rendu sur le domaine public dépend de la réussite du déploiement GitHub Pages et doit être confirmé indépendamment. Le dépôt historique, les archives antérieures et les autres automatisations MYTHOS restent inchangés.

## 3 novembre 2026 — Lemniai (Les Lemniennes), volume historique XXX

### Source contrôlée et absence initiale dans le dépôt cible

Le manuscrit existait dans l'archive GitHub historique `Bobcribb/Bobcribb.github.io` : `chapitres/comedies/volume-030-aristophane-lemniai.md`, empreinte blob `92ea495425566b16125151268f07729478b9d0ec`. Il n'était pas présent dans l'arbre `Bobcribb/Mythos` lors de l'inventaire précédent l'opération. **Il s'agit du transfert d'un texte antérieur, non d'une nouvelle rédaction.**

- Copie exacte : [lemniai-source.md](comedies/lemniai-source.md). **13 461 caractères**, **162 lignes**, **22 sections** numérotées 1–22 ; source et copie Git possèdent le **même SHA de blob**.
- **TH-03-LEM — Étude documentaire, philologique et philosophique** : [lecture intégrale](comedies/lemniai-etude.html), sections **1–16 et 20–22** (19 sections), préambule, bilan des degrés de certitude et bibliographie.
- **TH-02-LEM — Créations dramatiques contemporaines** : [trois scènes distinctes](comedies/lemniai-scenes-modernes.html), sections **17–19 [C]**. Aucune de ces scènes n'est présentée comme fragment de comédie antique.
- L'interprétation des marques Markdown (liens, emphases, listes) a été contrôlée sur les **22 blocs de prose** après publication : **22/22 identités du texte visible** par normalisation des espaces et suppression des balises de présentation. Ni suppression de section ni remplacement par un résumé.
- La source conserve tous ses liens historiques ; les lecteurs adaptent les liens de navigation vers les rubriques MYTHOS actuelles.

### Mise en ligne et navigation

Les pages sont des documents HTML statiques **versionnés directement** dans `main`, à la différence des lecteurs Polyidos et Daidalos générés pendant le déploiement. Les cartes illustrées de la rubrique Théâtre et le renvoi vers l'étude dans Philosophie ont été ajoutés ; le sommaire général HTML et Markdown et l'accueil pointent vers la lecture. Le volume précédent *Holkades* renvoie désormais localement à la nouvelle étude ; chaque parcours des *Lemniennes* possède un sommaire à ancres, un lien vers son complément, vers le manuscrit source et vers le sommaire général.

Le bandeau emploie le SVG existant `assets/mythos-hero.svg` (composition éditoriale statue grecque à gauche et temple stylisé à droite), dans une présentation noir et or. Les deux cartes utilisent le même motif, une à gauche et l'autre à droite. Les lecteurs contiennent une grille de navigation adaptée aux écrans étroits, un lien d'évitement et des repères de focus ; ces visuels sont contemporains et **ne représentent pas une reconstitution archéologique**.

Contrôle avant déploiement : `scripts/check-lemniai.py`, branché dans `.github/workflows/pages.yml`, vérifie l'empreinte du manuscrit, la partition des sections, l'identité du texte lisible, la bibliographie, les liens et les ancres. **À vérifier après exécution du workflow** : succès de l'action et état effectif de la page publique. Les sources scientifiques sont citées dans le chapitre mais leur exactitude philologique doit faire l'objet d'une vérification distincte, non couverte par l'audit de transfert. Aucune archive n'a été supprimée et les autres automatisations MYTHOS ne sont pas modifiées.


## 3 novembre 2026 — Gēras, La Vieillesse (Aristophane), volume historique XXXI

**Inspection préalable :** le manuscrit `Bobcribb/Bobcribb.github.io/chapitres/comedies/volume-031-aristophane-geras.md` a été lu intégralement (blob Git `cacecbb6b24cfb736e33b4dbd092b7bb9c4b82a3`, 12197 caractères). Le dépôt courant ne possédait ni page de lecture ni archive de ce volume ; le volume XXX *Lemniai* était déjà publié et n'a pas été dupliqué.

**Copie et classement :** [manuscrit Markdown original](comedies/geras-source.md) conservé exactement ; [TH-03-GER, étude documentaire, philologique et philosophique](comedies/geras-etude.html) : sections 1–16 et 20–22 (19 sections), avec préambule, tableau des preuves et bibliographie ; [TH-02-GER, créations modernes](comedies/geras-scenes-modernes.html) : trois scènes [C] (17–19), sans attribution antique. Les 22 corps des sections ainsi que le préambule ont été comparés au texte HTML lisible après interprétation des seuls marqueurs de style Markdown ; aucun résumé ne remplace les sections.

**Interface :** sommaires cliquables, navigation étude/scènes, renvoi réciproque depuis *Lemniai*, accueil, Théâtre, Philosophie et sommaires HTML/Markdown. Bandeau SVG local `assets/mythos-hero.svg` (statue à gauche, temple à droite) étendu aux rubriques, cartes illustrées et responsive. La suite XXXII demeure signalée comme archive historique et non comme volume publié sur le nouveau site.

**Garde-fou :** `scripts/check-geras.py` ajouté au workflow Pages. Contrôle source par Git SHA, 22/22 sections, distinction 19/3, sommaires et bibliographie. Cela vérifie la fidélité de la publication, pas l'authenticité des fragments antiques ni la totalité des références savantes. Aucune archive ni autre automatisation n'est modifiée.
