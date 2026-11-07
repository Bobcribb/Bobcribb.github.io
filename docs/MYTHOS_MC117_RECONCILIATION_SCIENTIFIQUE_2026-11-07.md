# MYTHOS — MC-117 : réconciliation documentaire et étude critique du complément ougaritique

**Date de contrôle :** 7 novembre 2026.  
**Collection :** mythologie comparée.  
**Statut du document :** notice scientifique et éditoriale non numérotée, conservée dans `docs/`. **Cette note n'est ni une nouvelle monographie canonique, ni une demande `editorial/inbox/`, ni la preuve d'une nouvelle publication sur bobmythos.fr.**

## 1. Conclusion opérationnelle

**Une seule étude canonique sous MC-117, volume CCCXLI (341).** Le texte principal a été attribué à la demande historiquement antérieure `52e03cb4-44ec-47c7-9506-f3f88fc240d1`. La seconde demande `70d8a117-5f4c-46b3-9d07-202611070117`, plus récente, traite en grande partie les mêmes Dioscures, Aśvin, héros du *Popol Wuj* et réceptions romaines. Elle est **retenue** dans `editorial/holds.json` et doit conserver son texte et son empreinte sans nouvelle attribution.

Toutefois, les deux rédactions ne sont **pas textuellement identiques** et ne doivent pas être simplement fusionnées. Le second manuscrit contient un dossier distinct et substantiel sur **Šaḥar et Šalim d'Ougarit**, la tablette RS 2.002 / KTU-CAT 1.23, les difficultés de l'identification des « dieux gracieux » et le rapport entre mythe et rite. Cet apport n'est pas couvert par l'étude principale. Le conserver comme matériau d'un **complément critique non numéroté**, susceptible d'être exploité après vérification philologique, est préférable à une deuxième attribution historique MC-117.

Ce document fixe le résultat de la comparaison ; il ne modifie ni le chapitre publié, ni les JSON de l'inbox, ni les reçus, ni les planifications.

## 2. Éléments GitHub réellement comparés

| Élément | Manuscrit principal, déjà attribué | Manuscrit plus récent, en retenue |
| --- | --- | --- |
| UUID | `52e03cb4-44ec-47c7-9506-f3f88fc240d1` | `70d8a117-5f4c-46b3-9d07-202611070117` |
| Chemin de demande | [Premier JSON](../editorial/inbox/52e03cb4-44ec-47c7-9506-f3f88fc240d1.json) | [Second JSON conservé](../editorial/inbox/70d8a117-5f4c-46b3-9d07-202611070117.json) |
| Attributions | [Volume CCCXLI (341)](../chapitres/comparatif/volume-cccxli-mc-117-jumeaux-sacre-dioscures-asvins-romulus-remus-popol-wuj-ibeji.md) | **Aucun volume** ; statut en retenue |
| Empreinte de demande conservée au registre | `33cb9b3a0b8302329873b046a2ca758ddf130d01149da71fb978b091ea34c156` | `82e95cb831932fc53af108e9d45cdd208b8909972f97a09ad195f63f194806db` |
| Volume de rédaction (caractères Markdown, mesure sur la version lue) | 53 353 | 75 976 |
| Accent principal | Grecs, Veda, Rome, *Popol Wuj*, culture yorùbá des ìbejì | Grecs, Veda, Ougarit, Rome, *Popol Wuj*, méthode philologique |
| Place d'Ougarit et des noms Šaḥar/Šalim | Aucune occurrence dans le corps examiné | Développement autonome, plusieurs sections |
| Limites du dossier | Ne traite pas KTU 1.23 | Ne développe pas Romulus/Rémus ni les pratiques yorùbá des ìbejì |

**Sources de vérité éditoriale :** `editorial/numbering.json`, collection `comparatif`, reçus d'allocation ; `editorial/holds.json` ; `AGENTS.md` ; `docs/PUBLICATION_CONCURRENTE.md`. La cote historique **MC-117** et le volume canonique **CCCXLI (341)** sont deux identifiants distincts. La retenue du second UUID est justifiée par le chevauchement scientifique et chronologique des demandes ; elle **n'est pas une suppression** de leur contenu.

La recherche du mot « Ougarit » dans le texte du volume principal n'a trouvé aucune occurrence ; le résultat est une constatation de couverture textuelle, non un jugement général sur la qualité de l'étude.

## 3. Apport distinct : RS 2.002 / KTU-CAT 1.23

### 3.1. Attestation matérielle [A]

La tablette [AO 17189](https://collections.louvre.fr/ark:/53355/cl010141954), numéro de fouille **RS 2.002**, est conservée au musée du Louvre, département des Antiquités orientales. Le catalogue donne : découverte à Ras Shamra en **1930**, datation **Bronze récent II (1400–1200 av. n. è.)**, support de terre cuite, **19,5 × 12,8 × 3 cm**, objet incomplet, inscription cunéiforme. Le titre descriptif du catalogue est « Naissance des dieux gracieux et beaux ». Il s'agit d'une description institutionnelle d'un artefact réel, non d'une preuve que chaque épisode divin a eu lieu.

Le texte est identifié dans les éditions spécialisées par **KTU/CAT 1.23** ; le [Cuneiform Digital Library Initiative](https://cdli.earth/search?collection=louvre&layout=full&limit=1000&order%5B0%5D=designation&period=middle+bab) rattache cette cote à **AO 17189**, avec renvoi à **KTU³, 1.23** (Dietrich, Loretz et Sanmartín, 2013). Une page de catalogue muséal et une édition de texte ne remplissent pas la même fonction : pour traduire des lignes lacunaires, l'édition et son apparat demeurent indispensables.

### 3.2. Organisation littéraire du document [A/I]

L'analyse de Mark S. Smith, *The Rituals and Myths of the Feast of the Goodly Gods of KTU/CAT 1.23* (SBL, **2006**, *Resources for Biblical Study* 51), distingue les **lignes 1–29**, combinant actions rituelles et récitations, de la **narration des lignes 30–76**. La présentation bibliographique de son ouvrage confirme cette partition et fait de la relation entre liturgie, récit et cadre royal un problème d'interprétation, non un présupposé.

Le récit fait intervenir des relations d'El avec des femmes, des naissances divines et des puissances associées à une opposition d'espaces et de conditions. L'édition doit maintenir la différence entre les figures nommées **Šaḥar et Šalim**, traditionnellement comprises en relation avec l'aurore et le crépuscule, et l'ensemble des **`’ilm nʿmm`** (« dieux gracieux »), dont l'identification a été discutée. Le second manuscrit MC-117 examine spécifiquement les passages situés approximativement dans les **lignes 30–54 et 55–64** ; l'exactitude des restitutions et des subdivisions doit être réévaluée sur une édition philologique, puisque la tablette comporte des lacunes.

**[I]** Deux paires ou groupes de naissances peuvent servir à construire un contraste mythique. **[H]** Une réduction de l'ensemble à deux astres ou à une unique paire universelle de « jumeaux » ne peut être retenue sans démonstration. Il est également risqué de traiter comme certaine l'identification du groupe de « dieux gracieux » aux figures nommées Šaḥar et Šalim. Ces questions doivent être exposées comme des débats exégétiques, non résolues par un schéma comparatif.

### 3.3. Philologie [A/I/H]

Le nom ougaritique **`šḥr`** (Šaḥar) est habituellement associé à l'aurore et **`šlm`** (Šalim) au soir ou au crépuscule. Les désignations montrent une opposition sémantique souvent interprétée comme temporelle ou cosmique. La traduction par « jumeaux » est toutefois une qualification de la narration et de l'exégèse : le **couplage nominal ne suffit pas, à lui seul, à établir une gémellité biologique au sens d'une définition moderne**. La distribution exacte des pronoms, des naissances, du nombre et des désignations doit être confrontée aux reconstructions éditoriales.

Une comparaison avec le sanskrit **`aśvín-`**, nom d'un duo divin associé au cheval, ou avec le grec **Διόσκουροι**, composé traditionnellement analysé par le rapport à Zeus, ne crée pas une équivalence étymologique : les langues, les séquences textuelles et les fonctions diffèrent. Le rapprochement est **typologique**, non la preuve d'une filiation indo-européenne ou d'une transmission directe vers le Levant.

### 3.4. Historiographie critique [A/P]

Le livre de Smith (2006) conteste les lectures trop linéaires du rapport « mythe et rituel » et reconstitue un dispositif complexe de relations de parenté, d'opposition et d'intégration dans un cadre royal. Le [catalogue officiel de SBL Press](https://cart.sbl-site.org/books/060351P) fournit la référence de l'ouvrage et son objet.

Jean-Marie Husser, « [Entre rituel, mémorial et littérature de propagande. À propos de deux textes ougaritiques au genre mal défini](https://archimede.unistra.fr/en/revue-archimede/archimede-7-2020/archimede-7-2020-dossier-1-entre-rituel-memorial-et-litterature-de-propagande-a-propos-de-deux-textes-ougaritiques-au-genre-mal-defini/) », *Archimède* 7 (2020), p. 51–61, DOI **10.47245/archimede.0007.ds1.05**, propose que ces compositions poétiques fixent et réinterprètent la mémoire de cérémonies liées à la famille royale, plutôt que de constituer de simples livrets liturgiques. Son article porte notamment sur **RS 2.002** et **RS 34.126**. **[I]** Cette différence de perspective importe : l'historien ne peut pas déduire une séquence rituelle effectivement exécutée d'une description poétique supposée transparente.

La question d'un « mariage sacré » effectivement accompli doit rester séparée du constat textuel de relations sexuelles divines. Smith la discute également dans « Sacred Marriage in the Ugaritic Texts? The Case of KTU/CAT 1.23 », dans *Sacred Marriages* (2008), p. 93–114, DOI **10.5325/j.ctv1bxgzv8.7**. **[P]** Cette prudence illustre la différence entre l'image narrative d'un acte et la preuve de son institution rituelle.

## 4. Tableau de comparabilité : limites des analogies

| Dossier | Sources contrôlables | Attestation [A] | Analogie possible [I] | Hypothèse à refuser sans preuve [H] |
| --- | --- | --- | --- | --- |
| Dioscures | Homère, *Iliade* III, 236–244 ; *Odyssée* XI, 298–304 ; Pindare, *Néméenne* X, 55–90 | Fraternité, destin partagé, alternatives de vie et de mort suivant les versions | Dualité relationnelle, secours, partage de statut | Mythe initial identique à tous les autres |
| Aśvin | *Ṛgveda* I, 116–119, VII, 69–72 ; Jamison–Brereton, 2014 | Couple de destinataires au duel, interventions salutaires, liens équins | Proximité fonctionnelle gréco-védique exigeant comparaison linguistique | Équivalence littérale de tous les récits |
| Šaḥar et Šalim | RS 2.002 = KTU/CAT 1.23 ; Smith, 2006 ; Husser, 2020 | Figures nommées et naissances dans un récit ougaritique | Dualité de positions et classement cosmique | Identité avec Aśvin ou « Gémeaux universels » |
| Héros du *Popol Wuj* | Manuscrit Ximénez, Ayer MS 1515 ; traductions de Christenson et Tedlock | Générations héroïques, jeu de balle, épreuves de Xibalba | Relation au monde inférieur et à la possibilité du retour | Généalogie indo-européenne ou identité de chaque vase maya |
| Romulus et Rémus, ìbejì yorùbá | Sources textuelles romaines et enquêtes patrimoniales mentionnées dans l'étude canonique | Histoires de souveraineté à Rome ; pratiques relatives à la gémellité yorùbá | Rapports entre paire, filiation, groupe et mémoire | Effacement des différences historiques et religieuses |

Le tableau est une aide à la lecture, **pas une démonstration de diffusion historique**. Les corpus et leurs supports ne sont pas de nature homogène. L'hypothèse d'une proximité indo-européenne ne fournit aucun argument de filiation automatique pour les données ougaritiques ou k’iche’.

## 5. Apports secondaires du manuscrit retenu et précautions de réemploi

Au-delà de KTU 1.23, le second manuscrit propose une discussion plus développée des divergences entre **Tite-Live, Cicéron et Denys d'Halicarnasse** sur les Dioscures à Rome, ainsi qu'un dossier d'objets étrusques du Metropolitan Museum of Art. Des renvois utiles se trouvent dans ses sections **XXV–XXVII**, et la liste d'objets dans **XLIV**. Il propose également un glossaire philologique et des critères de réfutation des rapprochements universalisants. Ces éléments peuvent enrichir une bibliographie raisonnée du volume principal, mais plusieurs se superposent à son propre chapitre de comparatisme.

**Ne pas effectuer de copier-coller intégral.** Toute note destinée ultérieurement au lectorat public devrait isoler les apports réellement distincts, préciser les éditions primaires, contrôler la légende et les droits de chaque image, et signaler explicitement ce qui relève d'une lecture philosophique. Le manuscrit retenu reste une archive scientifique complète et traçable.

Une proposition d'illustration particulièrement solide est la tablette **Louvre AO 17189**, dont la provenance, la cote, la datation et les dimensions sont attestées. La réutilisation de la photographie doit être vérifiée selon les conditions du musée ; ce dossier ne crée ni ne copie d'image et ne réintroduit aucune illustration 2,5D.

## 6. Sources, bibliographie et vérifications documentaires

1. **Musée du Louvre**, [AO 17189 / RS 2.002](https://collections.louvre.fr/ark:/53355/cl010141954), fiche d'objet ; attestation matérielle, datation, provenance, état de conservation.
2. **Dietrich, Manfried, Oswald Loretz et Joaquín Sanmartín**, *Die keilalphabetischen Texte aus Ugarit, Ras Ibn Hani und anderen Orten*, 3e éd., 2013, texte **KTU³ 1.23** ; contrôle des signes et de la segmentation nécessaire avant édition définitive.
3. **Mark S. Smith**, *The Rituals and Myths of the Feast of the Goodly Gods of KTU/CAT 1.23*, SBL *Resources for Biblical Study* 51, 2006 ; [notice éditoriale](https://cart.sbl-site.org/books/060351P). La consultation des éditions textuelles et de l'apparat demeure nécessaire pour juger de chaque restitution.
4. **Jean-Marie Husser**, « Entre rituel, mémorial et littérature de propagande », *Archimède* 7, 2020, 51–61, DOI [10.47245/archimede.0007.ds1.05](https://doi.org/10.47245/archimede.0007.ds1.05) ; discussion du genre des textes et de leur valeur pour l'histoire des pratiques.
5. **Mark S. Smith**, « Sacred Marriage in the Ugaritic Texts? The Case of KTU/CAT 1.23 », 2008, p. 93–114, DOI [10.5325/j.ctv1bxgzv8.7](https://doi.org/10.5325/j.ctv1bxgzv8.7) ; limites de la lecture du récit comme preuve d'un rituel de mariage.
6. **Jamison, Stephanie W. et Joel P. Brereton**, *The Rigveda: The Earliest Religious Poetry of India*, Oxford University Press, 2014 ; source de contrôle pour les noms, fonctions et variantes des Aśvin.

## 7. Décision de réconciliation et conditions d'évolution

1. **Maintenir MC-117 comme une seule cote historique** et **CCCXLI (341)** comme le volume canonique existant. Ne créer ni deuxième MC-117 ni volume autonome avec un autre numéro pour le même objet scientifique.
2. **Maintenir la retenue du second UUID** dans `editorial/holds.json` et préserver intégralement les deux fichiers JSON originaux, le registre et leurs empreintes. Ne pas lever la retenue par une modification manuelle du registre.
3. **Conserver le dossier ougaritique comme complément critique potentiel non numéroté.** Cette notice fournit un premier arbitrage documentaire, non une permission implicite de mettre le manuscrit retenu dans le circuit d'allocation.
4. **Ne pas altérer le volume principal publié** dans l'opération présente ; tout ajout futur serait soumis à une revue philologique et à des tests de conservation de texte.
5. Les autres retenues MC-117, notamment la troisième étude du même sujet et la collision de cote avec un manuscrit sur les os du sacré, sont **distinctes**, ne sont pas résolues ici et ne doivent pas être modifiées.
6. **État public séparé :** l'adresse du volume principal [MC-117 / CCCXLI](https://bobmythos.fr/chapitres/comparatif/volume-cccxli-mc-117-jumeaux-sacre-dioscures-asvins-romulus-remus-popol-wuj-ibeji/) doit être vérifiée au déploiement. Le présent fichier dans `docs/` et le manuscrit en retenue **ne constituent pas une publication d'un nouveau chapitre**.

**Portée du commit attendu : un nouveau fichier documentaire non numéroté, aucun autre chemin modifié.**
