# MYTHOS — MC-121 : réconciliation historique, préservation du manuscrit sur le sel et évaluation des compléments grecs et japonais

**Audit scientifique et éditorial du 7 novembre 2026.**  
**Statut :** rapport documentaire non numéroté ; ne vaut pas création d'une nouvelle étude historique, attribution de volume, fusion de manuscrits ni preuve de publication publique.  
**Périmètre :** collection \`comparatif\` et son articulation avec \`origines-du-sacre\`.  
**Décision conservatoire :** ne modifier **aucun** manuscrit original, fichier \`editorial/inbox\`, reçu \`editorial/numbering.json\`, retenue \`editorial/holds.json\`, planification ou média.

## 1. Diagnostic : trois objets sous une même cote et un sujet déjà traité

La cote historique **MC-121** a été revendiquée par plusieurs soumissions distinctes. La première en date parmi celles examinées, **« Le sel du sacré »** (\`7c121f0b-831e-48b1-a0a4-202611070121\`, commit \`cedf955206d557221954690812c8ea4a7c5f61b2\`), est scientifiquement largement redondante avec **MC-089**, *« Le sel des dieux : purification, offrande, alliance et conservation »*, volume **CCLXXXI (281)**. La demande « Le sel du sacré » compte **64 177 caractères Markdown** et demeure intégralement conservée en retenue, avec son empreinte **SHA-256 \`72913eea26cb43bb99f3b7b6dcd767c46d72a55dfc8a9e9939837e66fa1228d3\`**.

La cote historique **MC-121** a été régulièrement attribuée à l'étude distincte **« Les poissons du sacré : interdits, sages des eaux, métamorphoses et salut »**, UUID \`7b1a18d4-52ef-4d63-a80d-29c1256fd091\`, volume **CCCXLVI (346)**, chemin \`chapitres/comparatif/volume-cccxlvi-mc-121-poissons-sacre-egypte-syrie-apkallu-oannes-manu-apollon-ichtus.md\`. Il s'agit d'une attribution du registre, indépendante de l'état de publication HTTPS.

Une troisième soumission, **« Les cloches du sacré »**, UUID \`c0c121a0-57dc-4d42-8ed2-202611071150\`, est aussi retenue, car elle revendique une cote MC-121 déjà affectée aux poissons. Son objet est scientifiquement distinct ; cette notice ne l'évalue pas et ne lui attribue aucune cote de substitution.

**Conclusion :** il serait fautif de publier le sel comme deuxième MC-121 ou de lui assigner artificiellement MC-134. Les apports nouveaux doivent être explicités et, si nécessaire, publiés **en complément non numéroté** après relecture, sans cloner la monographie de 281. Le traitement historique des poissons reste intact.

## 2. Table de concordance : source de vérité

| Élément | Statut vérifié sur \`main\` | Destination et action |
| --- | --- | --- |
| MC-089 « Le sel des dieux » | Volume CCLXXXI (281), manuscrit de 87 214 caractères | [Texte canonique](../chapitres/comparatif/volume-cclxxxi-mc-089-sel-des-dieux-natron-mola-salsa-alliance-purification-conservation.md), à conserver |
| Demande sel MC-121 | 64 177 caractères ; SHA-256 verrouillé dans \`holds.json\` | [Texte intégral en attente](../editorial/inbox/7c121f0b-831e-48b1-a0a4-202611070121.json) ; ne pas attribuer |
| MC-121 « Les poissons du sacré » | Volume CCCXLVI (346), reçu dans \`numbering.json\` | [Texte canonique](../chapitres/comparatif/volume-cccxlvi-mc-121-poissons-sacre-egypte-syrie-apkallu-oannes-manu-apollon-ichtus.md) ; ne pas renuméroter |
| Demande cloches MC-121 | Retenue explicite, sujet autre que les poissons et le sel | [Fichier conservé](../editorial/inbox/c0c121a0-57dc-4d42-8ed2-202611071150.json) ; hors périmètre de la présente note |
| MC-133 | Soumission sur l'œuf cosmique, sans reçu observé au contrôle initial du 7 novembre à 17 h 30 UTC | Ne pas présumer une attribution ; relire \`main\` à chaque intervention |

Ne **pas** interpréter les chiffres MC comme une progression identique à celle des volumes romains : des études de comédie et autres recherches comparatives prennent également des volumes dans la série. L'allocation du volume appartient exclusivement à GitHub Actions et au registre transactionnel.

## 3. Ce qui constitue un recouvrement scientifique réel

La lecture directe des deux Markdown révèle cinq noyaux communs majeurs :

1. **Mésopotamie :** SAA 20 037 et les instructions de dépôt de sel dans le cadre des rites du temple d'Assur, avec le pain et la parole rituelle.
2. **Bible hébraïque :** Lévitique 2,13 ; Nombres 18,19 ; Ézéchiel 43,24, avec la fonction normative du sel et les formulations d'alliance.
3. **Rome :** *mola salsa*, préparation des Vestales, étymologies et procédures d'*immolatio*, sources de Pline et de la tradition de Festus.
4. **Égypte :** natron utilisé pour l'embaumement, dépôt funéraire KV54 et Metropolitan Museum **1988.437.2**, avec distinction physico-chimique entre natron et sel alimentaire.
5. **Méthode :** critique des universalismes, séparation de la substance, de l'action, de la norme cultuelle et de l'interprétation philosophique.

MC-089 traite ces questions de façon développée, notamment dans ses sections sur les comparaisons assyriennes, les dispositions bibliques, le natron et la *mola salsa*. La rédaction MC-121 sur le sel ne doit donc pas être décrite comme « nouvelle première monographie » du sujet.

Ces recouvrements ne signifient pas que les deux textes sont identiques ligne à ligne. Ils suffisent néanmoins à refuser une nouvelle livraison autonome qui répéterait les mêmes sources et la même question directrice.

## 4. Les apports du manuscrit retenu réellement absents ou peu développés dans MC-089

### 4.1. Grèce : ne pas transformer les grains en sel

Le volume MC-089 comporte un chapitre grec consacré notamment à **Porphyre, *De l'abstinence* II**, à la frugalité et à l'économie de l'offrande. Il **ne cite pas**, dans le texte contrôlé, les scènes de sacrifice nommées dans la soumission retenue : **Homère, *Iliade* I, 449–458 ; *Odyssée* III, 440–447 ; Euripide, *Électre* 799–812**.

Dans ces passages, les grains rituels, **οὐλοχύται** (*oulochýtai*) chez Homère, et les grains ou préparations projetés chez Euripide, font partie de la préparation du sacrifice. **[A]** Les références textuelles indiquent un geste céréaliaire. **[I]** On peut comparer sa fonction à la projection de *mola salsa* à Rome, mais **[N]** il n'est pas démontré que le passage homérique contienne explicitement du sel. Un commentaire byzantin, une approximation d'édition ou une coutume latine ne doit pas être incorporé dans le vers de l'épopée archaïque comme s'il s'agissait d'un mot réellement présent.

**Proposition de complément critique, non numéroté :** « Le grain grec et la farine salée romaine : quels gestes peut-on comparer ? ». La question doit être traitée avec le texte grec et l'apparat, pas par un simple collage de rites. Repères historiographiques : Marie-Claire Amouretti, *Le pain et l'huile dans la Grèce antique*, Annales littéraires de l'Université de Besançon 328, Besançon, 1986, [édition Persée](https://www.persee.fr/doc/ista_0000-0000_1986_mon_328_1) ; Jane Ellen Harrison, *Prolegomena to the Study of Greek Religion*, 1903, pour l'histoire critique des rapprochements. **La comparaison de commentaire** exige la prudence chronologique : les discussions tardives ne sont pas des attestations homériques du sel.

### 4.2. Japon : le cas spécifique de \`entō\` (塩湯)

La monographie canonique MC-089 n'aborde ni le Japon ni l'**entō** dans le corps consulté. Le manuscrit retenu propose un **second champ documentaire** : la préparation d'une eau salée pour certains rites de purification shintō, qui ne se réduit pas au dépôt de cristaux de sel sur des aliments.

L'[Encyclopedia of Shinto](https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9651) de **Kokugakuin University**, article **« Entō »** signé **Inoue Nobutaka**, précise que le terme peut également être lu **shioyu** et décrit une préparation obtenue en dissolvant du sel dans de l'eau. Elle indique son emploi dans la purification préparatoire (**shubatsu**) et dans certains rites de purification du terrain (**jichinsai**) ; une branche de **sakaki** trempée dans l'eau salée et agitée lors d'un acte codifié par la Jinja Honchō est décrite dans la notice. Le récipient spécialisé est appelé **entōki**.

La notice cite une expression du **Kōtai Jingū gishikichō**, document du début du IXe siècle, selon laquelle une purification à l'eau salée précède la présentation d'une offrande au magasin divin. C'est un **témoignage textuel historique** du recours à l'eau salée, mais il **ne prouve pas que la procédure moderne décrite soit restée inchangée durant tous les siècles intermédiaires**.

**[A]** La notice institutionnelle fournit des définitions et un témoin du IXe siècle. **[I]** L'eau salée peut être comprise comme un instrument de séparation et de qualification d'une action rituelle. **[H]** On ne peut, sans sources et mécanismes de contact, soutenir une diffusion du procédé depuis Assur ou Rome vers les sanctuaires japonais. **[P]** Le cas met à l'épreuve la tendance à réifier une « substance pure » en montrant le rôle de la recette, de l'officiant, de l'eau et du contexte.

**Complément critique possible :** « Shio, entō et shubatsu : l'eau salée, l'institution et le temps des sources ». Ne pas le publier comme un nouvel MC autonome sur le sel ; le présenter comme un dossier documentaire rattaché à MC-089 après revue.

### 4.3. Exode 30,35 : traduction technique et controverse

Le manuscrit retenu ajoute une discussion sur **Exode 30,34–38**, en particulier le participe du verset **30,35**, dont certaines traductions rendent la préparation de l'encens par « salé », « mêlé » ou « préparé ». MC-089 ne cite pas explicitement ce passage dans le Markdown consulté. **[A]** Il existe une controverse de traduction ; **[N]** il serait prématuré d'en faire une preuve matérielle certaine du dépôt de chlorure de sodium dans une recette d'encens. Vérifier le texte massorétique, les versions anciennes et le lexique avant d'exploiter cette occurrence.

### 4.4. 11Q19, Rouleau du Temple : témoin de réception

Le manuscrit retenu signale **11Q19 / 11QTa**, un témoin de la réception des prescriptions sacrificielles dans les manuscrits de la mer Morte. La référence précise à la colonne et aux lignes n'a **pas été collationnée** dans cette vérification et ne doit donc pas être annoncée comme définitivement établie. C'est une **piste** pour approfondir l'histoire de la transmission de la loi, non un élément qui autorise à réattribuer une cote historique.

### 4.5. Contre-épreuves supplémentaires et limites

Le manuscrit retenu donne une place plus importante à **2 Rois 2,19–22** (Élisée et la source), **Exode 30,35** et au lexique japonais. MC-089 connaît déjà les oppositions entre l'alliance et la destruction, notamment avec **Juges 9,45**, **Genèse 19,26** et la valeur non uniforme du sel dans la Bible. Il faut **éviter** de présenter comme inédit ce qui n'est que reformulé.

## 5. Correction méthodologique et contrôle des références de matériaux

L'[objet du Metropolitan Museum of Art](https://www.metmuseum.org/art/collection/search/587568) **1988.437.2** est un sac de natron provenant de la cache funéraire **KV54** de Toutankhamon, daté de la XVIIIe dynastie, env. **1328–1318 avant notre ère**, matériau indiqué comme **lin et natron**, dimensions **8,5 × 6,6 × 3,6 cm**. Le Met distingue cette cache des pièces du tombeau KV62 et présente les sacs comme des reliquats ou matériaux de l'embaumement. Ce point est déjà développé dans MC-089. Un nouveau commentaire peut comparer les modes de preuve, mais ne doit ni republier les mêmes objets comme « inédits » ni présenter le natron comme du NaCl alimentaire pur.

Le travail sur le sel en Assyrie repose sur **SAA 20 037 / VAT 08005** et la publication de Simo Parpola, *Assyrian Royal Rituals and Cultic Texts*, *State Archives of Assyria* 20 (2017), [édition de texte ORACC P336311](https://oracc.museum.upenn.edu/saao/saa20/P336311). Les indices de face/revers et les lignes ne doivent pas être cités comme collationnés tant que le cliché ou l'édition de référence n'a pas été examinée intégralement. En particulier, la formule abrégée « ligne 20 » dans le texte retenu doit être **recomparée** au découpage d'édition avant réemploi.

L'ensemble de ces corrections montre que le complément critique ne consiste **ni** à répéter la totalité de MC-089 **ni** à reproduire sans examen les 64 177 caractères du texte retenu.

## 6. Table de contrôle épistémique

| Proposition | Niveau | Action éditoriale |
| --- | --- | --- |
| MC-089 traite déjà le sel de l'offrande et du natron | **Confirmé dans le Markdown canonique** | Conserver MC-089 comme étude principale |
| Le manuscrit sel MC-121 est placé en retenue | **Confirmé par \`holds.json\`** | Conserver les octets et SHA-256 |
| MC-121 est attribué aux poissons | **Confirmé par \`numbering.json\`** | Ne pas renuméroter, ne pas créer de second MC-121 |
| Les vers grecs cités parlent de grains sacrificiels | **Attestation littéraire localisée, à collationner** | Dossier grec complémentaire possible |
| Les mêmes vers prouvent l'usage de sel homérique | **Non démontré** | Interdire la reformulation affirmative |
| Kokugakuin documente \`entō\` et cite un texte du IXe siècle | **Documenté par l'institution** | Complément japonais possible avec chronologie explicite |
| Le rituel \`entō\` a été importé de Mésopotamie | **Hypothèse sans preuve** | Ne pas publier comme filiation |
| Les références exactes à 11Q19 ont été collationnées | **Non vérifié** | Exiger une édition critique |
| Le rapport scientifique est un nouveau numéro de volume | **Faux** | Rester sous \`docs/\` sans allocation |

## 7. Deux pistes de compléments non numérotés, distinctes du thème canonique

**Complément A — L'absence du sel dans trois scènes grecques.** Mettre en parallèle le vocabulaire des grains chez Homère et Euripide et la farine rituelle salée de Rome. Le résultat pourrait être un contre-exemple rigoureusement formulé à l'universalisation des pratiques. Ce dossier serait court et ancré à MC-089 ; ne pas reproduire intégralement les sections communes à Assur et à l'Égypte.

**Complément B — Purifications japonaises et chronologie des gestes.** Élaborer une petite édition commentée des occurrences de \`shioyu / entō\` dans les textes historiques, décrire le cadre institutionnel contemporain et distinguer les usages locaux, les traductions et les limites de comparaison. Le dossier ne deviendrait autonome que si une question scientifique **nouvelle et non redondante**, une cote historiquement libre et une revue explicite le justifiaient. Ce rapport n'attribue aucune cote nouvelle.

**Les deux projets ne doivent pas être déposés directement en \`editorial/inbox\`** comme des manuscrits canoniques tant que leur périmètre n'a pas fait l'objet d'une réconciliation. L'original retenu suffit à préserver leur matériau documentaire.

## 8. Bibliographie de contrôle

### Sources anciennes
- Homère, *Iliade* I, 449–458 ; *Odyssée* III, 440–447, texte grec et apparat à comparer pour **οὐλοχύται**.
- Euripide, *Électre* 799–812, scène sacrificielle et vocabulaire des grains.
- Lévitique 2,13 ; Nombres 18,19 ; Ézéchiel 43,24 ; Exode 30,34–38 ; 2 Rois 2,19–22 ; 11Q19 / Rouleau du Temple (référence fine à vérifier).
- Festus, *De verborum significatione* (éd. Lindsay, rubrique \`immolare\`) ; Pline, *Histoire naturelle* XXXI, 89.
- Documentation \`Kōtai Jingū gishikichō\`, témoin du début du IXe siècle signalé dans l'*Encyclopedia of Shinto* ; consulter le texte japonais original avant édition définitive.

### Études et institutions
- Simo Parpola, *Assyrian Royal Rituals and Cultic Texts*, SAA 20 (2017), texte SAA 20 037.
- Marie-Claire Amouretti, *Le pain et l'huile dans la Grèce antique*, Besançon, 1986, [Persée](https://www.persee.fr/doc/ista_0000-0000_1986_mon_328_1).
- Jane Ellen Harrison, *Prolegomena to the Study of Greek Religion*, 1903 ; histoire de la comparaison des matières de sacrifice.
- Meghan J. DiLuzio, *A Place at the Altar*, Princeton University Press, 2016 ; Vestales et travail sacerdotal.
- Metropolitan Museum of Art, [« Bag of Natron from Tutankhamun's Embalming Cache »](https://www.metmuseum.org/art/collection/search/587568), 1988.437.2.
- Kokugakuin University, *Encyclopedia of Shinto*, [« Entō »](https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9651), notice institutionnelle signée Inoue Nobutaka.
- Marcel Detienne, *Comparer l'incomparable*, 2000 : méthode de fabrication des comparables, sans statut de source antique.
- Jean-Pierre Vernant et John Scheid : histoire des sacrifices dans leurs institutions historiques, sans fusion du rite grec et du rite romain.

## 9. Conclusion et procédure de suivi

Le contrôle des sources conclut à **un recouvrement scientifique substantiel** entre MC-089 et le manuscrit sur le sel anciennement proposé sous MC-121. La bonne réponse n'est ni la suppression du second texte ni la réédition artificielle de tout son contenu sous une nouvelle cote. Les trois objectifs simultanés sont : **conserver l'intégralité des matériaux historiques**, **éviter un faux volume supplémentaire** et **rendre visibles les questions réellement nouvelles**, notamment Grèce / Japon.

Ce document est un **rapport de rapprochement**, non le lecteur public du supplément. À chaque étape de révision, consulter les fichiers de référence de \`main\`, les reçus, les retenues, les validations de GitHub Actions et les pages HTTPS ; **ne déclarer la publication publique d'un nouveau dossier qu'après vérification effective**.

**Périmètre du commit de cette note : un seul fichier documentaire ajouté sous \`docs/\` ; aucun autre fichier modifié.**
