# MYTHOS — MC-134 : arbitrage historique de trois monographies distinctes et sauvegarde de leur identité

**Contrôle éditorial : 7 novembre 2026.**  
**Collection :** mythologie comparée, dépôt Bobcribb/Bobcribb.github.io.  
**Nature :** rapport scientifique et protocole de réconciliation, **non numéroté**.  
**Statut :** document proposé en pull request de relecture, **non fusionné et non publié automatiquement**.  
**Règle :** aucun manuscrit, reçu, numéro, image, workflow, horaire ou registre existant ne doit être modifié pour cette opération. Les propositions ci-dessous ne sont pas des réattributions.

## I. Diagnostic vérifié sur la branche principale

Trois soumissions autonomes utilisent dans leurs titres la même cote historique MC-134. Cette anomalie n'est **pas** un doublon scientifique démontré, mais une collision d'identité éditoriale : leurs objets principaux, leurs sources et leurs problématiques sont distincts.

| Ordre | Manuscrit et date de commit UTC | UUID et état | Étendue et singularité |
| --- | --- | --- | --- |
| 1 | **Les mains du sacré** ; 17:45:34, commit [4d21cf61520e](https://github.com/Bobcribb/Bobcribb.github.io/commit/4d21cf61520e8ec23d740bed6ec1f2f312012687) | [a0ce1340-74b1-4a3d-8e05-202611071829](../editorial/inbox/a0ce1340-74b1-4a3d-8e05-202611071829.json) ; demande sans reçu et sans retenue au contrôle | **69 863 caractères Markdown**, 80 sections : mains de prière, d'offrande, d'investiture et de reconnaissance, avec l'Égypte, Sumer, la Grèce, Rome, l'Iran, l'Inde bouddhique et les Andes |
| 2 | **Les nuées du sacré** ; 17:46:19, commit [4b3262c75f7b](https://github.com/Bobcribb/Bobcribb.github.io/commit/4b3262c75f7ba01d444029998ba003a278b3340b) | [f18c9d47-2e5b-4b61-9ac4-202611071830](../editorial/inbox/f18c9d47-2e5b-4b61-9ac4-202611071830.json) ; **retenue explicite** | **69 364 caractères**, 98 sections : pluies, orages et souveraineté divine, Baal, Zeus, Indra, Parjanya, Tištrya, YHWH, inscriptions Shang, Chahk maya |
| 3 | **Quand le corps devient présage : l'éternuement** ; 17:48:55, commit [8203adfde49b](https://github.com/Bobcribb/Bobcribb.github.io/commit/8203adfde49b922a149c305709b15c3f2bd35e60) | [641d3c82-4f8b-4e21-9d34-202611070134](../editorial/inbox/641d3c82-4f8b-4e21-9d34-202611070134.json) ; **retenue explicite** | **52 808 caractères**, 56 sections : éternuement et interprétation de signes chez Homère, Xénophon, Aristophane, Platon, Pline, Varāhamihira |

L'ordre provient des commits et des motifs inscrits dans editorial/holds.json, **et non de la terminaison numérique des UUID**, qui ne constitue pas une horloge fiable. En particulier, le nom du dernier UUID contient « 202611070134 », mais sa création a eu lieu **après** les deux autres soumissions. Toute décision qui privilégierait l'ordre numérique des UUID serait donc erronée.

**Fait A :** la collection comparative de editorial/numbering.json atteint le volume CCCLIX (359) au contrôle initial de cette opération ; aucun des trois UUID ci-dessus n'y possède de reçu canonique. Cette photographie **n'est pas une réservation d'un volume futur**. Les publications et entrées horaires concurrentes peuvent changer le maximum.

**Fait B :** la première demande reste, à cet état, sans retenue ; les deux suivantes sont verrouillées dans editorial/holds.json. Les empreintes de demande reconnues par le registre sont :

- « Nuées » : SHA-256 **e29050c43609d86b5b199149851f61df9a0742c37cbb1577d052af2b60663e80**.
- « Éternuement » : SHA-256 **23957c9860300eb9fae5b5ed5547c36d8baf249a3aa2d78df80c8ae7e7449d34**.

Ces empreintes se rapportent aux **demandes JSON**, non aux seuls corps Markdown. Les SHA de blobs GitHub sont différents et ne doivent pas être présentés comme des SHA-256. La demande première est conservée sous le même UUID : sa date plus ancienne ne dispense pas de validation du contenu.

## II. Les niveaux de responsabilité : historique, scientifique, transactionnel et public

1. **Identité historique MC :** attribuer une seule cote historique à une étude principale, et ne pas créer deux textes portant la même cote hors d'un complément explicitement documenté. Le contrôle est assuré par scripts/comparative_history.py et les registres existants.
2. **Numéro canonique romain :** attribué par le mécanisme éditorial transactionnel depuis un instantané frais de main et enregistré dans editorial/numbering.json. La présence d'une cote MC ne réserve aucun numéro de volume. Les variables {{volume}} et {{numero}} doivent rester dans les demandes non attribuées.
3. **Intégrité des manuscrits :** les fichiers JSON d'inbox, les demandes déjà attribuées, les retenues et leur SHA-256 restent immuables. Ne pas effacer, renommer, réémettre sous un autre UUID ou injecter un correctif dans l'original pour contourner le refus.
4. **Publication publique :** le commit qui ajoute une demande ne prouve pas sa conversion en chapitre. Il faut ensuite un reçu, un rendu, une validation complète de GitHub Actions et un contrôle HTTPS de la page de bobmythos.fr.
5. **Concurrence :** la succession de commits sur main peut annuler des exécutions de publication. Une note documentaire en branche de travail séparée est préférable à un commit inutile sur main qui déplacerait sa tête pendant le traitement des manuscrits.

La présente note documente **un arbitrage et des possibilités** : elle ne lève aucune retenue, ne permet aucune réattribution silencieuse et ne soumet aucune nouvelle demande en remplacement. Les autres études, images et planifications de MYTHOS n'entrent pas dans le périmètre.

## III. Première monographie : les mains — objet et corpus propre

**[A : contenu réellement présent dans le manuscrit]** Le premier dossier possède 80 sections, réparties sur la philologie du geste, les statues de fidèles sumériennes, le langage visuel d'Akhétaton, les mains levées et lavées dans les récits grecs, la dexiosis funéraire, le droit ou l'iconographie de la main droite romaine, les reliefs royaux sassanides, les gestes des images bouddhiques et le matériel andin.

**Question propre :** comment un organe représenté et manipulé devient-il une action reconnue — prière, offrande, présence substituée, investiture, reconnaissance ou droit ? Le point commun n'est **pas** une « main universellement sacrée » ; le dossier distingue les gestes entre eux.

**[I]** Une statue montrant des mains réunies ne prouve pas que tous les fidèles ont eu les mêmes gestes à toutes les époques. De même, une poignée de mains figurée sur une stèle attique est un document d'image et d'interprétation funéraire, pas une photographie d'un échange physique réellement accompli après la mort.

**Contre-exemples et nécessité de contexte :** des rayons terminés par des mains dans l'iconographie d'Aton, une dexiosis grecque et un geste bouddhique de main ont des histoires visuelles et théologiques distinctes. Leur morphologie commune ne produit pas une filiation.

**Conclusion scientifique [I] :** la monographie « mains » forme un objet autonome par rapport aux nuées et aux éternuements ; la priorité temporelle de sa demande est un critère éditorial **séparé** de cette autonomie. Elle demeure candidate à l'examen transactionnel, sans garantie automatique de succès.

## IV. Deuxième monographie : les nuées — météorologie, royauté et sources

**[A : contenu réellement présent dans le manuscrit]** La seconde étude comporte 98 sections, dont des dossiers sur **Baal, « chevaucheur des nuées »**, le titre grec **Νεφεληγερέτα** attribué à Zeus, l'orage en poésie grecque, les eaux du Veda, l'intercession pour la pluie, **Tištrya** dans l'Avesta, les images de tempête bibliques, les attestations divinatoires de Chine Shang et les figures de **Chahk** dans l'iconographie maya. Son index iconographique cite notamment la stèle du Baal au foudre **AO 15775** et des pièces muséales de Chahk.

**Question propre :** quelles institutions et images rendent la pluie compatible avec une souveraineté divine, et comment les sécheresses ou orages introduisent-ils la possibilité de contestation de cette souveraineté ? Il ne s'agit ni de la gestuelle d'une main ni d'un réflexe nasal interprété comme un présage.

**Précautions [A/I/H] :** un titre divin ou un poème ne livre pas une série de mesures pluviométriques. Une inscription Shang demandant la pluie ne prouve pas que toutes les traditions chinoises possédaient un « Baal local ». L'emploi de catégories comme « dieu de l'orage » peut être descriptif, mais sa généralisation efface langues, genres et périodes. L'hypothèse d'une transmission directe entre Ougarit et le monde maya ne découle d'aucun témoin invoqué.

**Conclusion scientifique [I] :** ce manuscrit est substantiellement distinct de la première demande. Son statut de retenue provient de la collision de cote MC-134, pas d'un diagnostic de redondance de sujet. Une cote nouvelle ne peut être obtenue sans décision documentaire explicite et sans préserver l'UUID original ; le présent rapport ne fait pas cette opération.

## V. Troisième monographie : l'éternuement — signe fortuit, voix collective et médecine du corps

**[A : contenu réellement présent dans le manuscrit]** Le troisième dossier traite en 56 sections de l'**éternuement involontaire** et de sa transformation en présage, salutation, ressort comique ou objet d'explication corporelle. Sa source grecque centrale est *Odyssée* **XVII, 541–550** : Télémaque éternue au moment où Pénélope exprime l'espoir d'un châtiment des prétendants. Pénélope **rit** et interprète le bruit comme confirmation. Dans Xénophon, *Anabase* **III, 2, 9**, un homme éternue pendant un discours sur le salut ; les soldats marquent une réaction religieuse, puis Xénophon propose un vœu à **Zeus Sōtēr**. Le récit distingue ensuite un vote à mains levées.

Ce dernier point est aussi la raison pour laquelle les deux dossiers « mains » et « éternuement » **ne sont pas des doublons** : l'assemblée lève effectivement les mains chez Xénophon, mais l'étude de l'éternuement explique d'abord **comment un événement fortuit reçoit une autorité dans un discours** ; la monographie sur les mains explique **comment un geste produit ou représente une relation rituelle**. La ressemblance locale n'unifie pas leur question directrice.

Dans Aristophane, *Oiseaux* **719–722**, le chœur élargit la catégorie d'**ὄρνις** en évoquant la voix, une rencontre et un éternuement parmi des signes : l'effet comique interdit d'en faire une loi divinatoire universellement acceptée. Dans Platon, *Banquet* **185d–e et 189a–c**, il s'agit de traiter un hoquet par des procédés corporels et de jouer avec la conversation médicale, non de transmettre un oracle. La salutation de ceux qui éternuent est documentée chez Pline, *Histoire naturelle* **XXVIII, 23** ; une section supplémentaire traite les classifications sanskrites chez **Varāhamihira**, *Bṛhatsaṃhitā*, en gardant leurs problèmes de numérotation et de traduction.

**[A : vérifications externes complémentaires]**

- [Homère, *Odyssée* XVII](https://beta.perseus.tufts.edu/urn:cts:greekLit:tlg0012.tlg002.butlernagy2020-eng2/book:17/) : l'éternuement de Télémaque et le rire de Pénélope se trouvent bien à cet endroit ; ne pas inventer une scène de consultation sacerdotale.
- [Xénophon, *Anabase* III, 2, 9](https://adfonteslibrary.org/work-xenophon-anabasis) : la séquence éternuement — réaction religieuse — vœu — vote est attestée dans la traduction en ligne ; lire aussi le texte grec avant toute nouvelle traduction scientifique.
- [Aristophane, *Oiseaux*, v. 719–722](https://adfonteslibrary.org/work-aristophanes-birds) : la plaisanterie sur la classe des présages comprend explicitement l'éternuement.
- [Pieter W. van der Horst, « The Omen of Sneezing », *Ancient Society* 43 (2013), 213–221](https://poj.peeters-leuven.be/content.php?id=2992610&journal_code=AS&url=article), DOI **10.2143/AS.43.0.2992610** : la notice et le résumé éditorial vérifiés soulignent le rôle du moment, du côté, de la personne et de la critique antique. **La totalité de l'article n'a pas été collationnée pour cette note.**
- [J. B. Kennedy, « New Sexual Puns in Plato’s Symposium: Hiccups, Sneezes and Pausanias », *The Classical Quarterly*](https://www.cambridge.org/core/journals/classical-quarterly/article/abs/new-sexual-puns-in-platos-symposium-hiccups-sneezes-and-pausanias/460585A374635D1A3B1C8CD60A2F6207) : publication en ligne **12 octobre 2026**, DOI **10.1017/S0009838826101797** ; le résumé fait état de jeux de mots médicaux et sexuels. **Ne pas présenter comme collationné le développement intégral sous abonnement.**

**Point non vérifié :** une ligne ou une tablette mésopotamienne spécifique établissant le même type d'éternuement présage. La série *Šumma ālu* peut servir de contrepoint sur la construction savante de signes, mais aucune « tablette de l'éternuement » inventée ne doit être ajoutée. Les passages de Varāhamihira réclament une collation sanskrite et une vérification de la division en chapitres selon les éditions utilisées.

**Conclusion scientifique [I] :** les outils de la sémiotique et de la philosophie peuvent éclairer le passage du bruit corporel au signe accepté. Ils ne justifient ni une efficacité physiologique prédictive ni une filiation uniforme entre traditions grecques et indiennes.

## VI. Tableau d'intersections réelles : empêcher les faux doublons

| Critère | Les mains | Les nuées | L'éternuement |
| --- | --- | --- | --- |
| Objet physique privilégié | Main ou mains représentées et agissantes | Nuage, pluie, orage, ciel | Réflexe nasal et bruit corporel |
| Corpus privilégié | Statues, reliefs, inscriptions, gestes textuels | Hymnes et épopées, textes religieux, inscriptions météorologiques, iconographie | Épopée, récit historique, comédie, philosophie, encyclopédie et astronomie-astrologie sanskrite |
| Question comparatiste | Qui montre, touche, investit, bénit, contracte ? | Qui dispense les eaux et comment en répondre ? | Qui interprète une coïncidence sonore comme message ? |
| Point grec | Homère, dexiosis, gestes de prière et d'offrande | Zeus et la poésie de l'orage | Homère XVII, Xénophon III, 2, Aristophane *Oiseaux* |
| Risque majeur | Confondre iconographie et acte rituel | Confondre mythe et mesure météorologique | Confondre hasard, médecine et divination |
| Statut éditorial au contrôle | Première demande, sans reçu ni retenue | Seconde demande, en retenue | Troisième demande, en retenue |

**[I]** Le contact entre les trois thèmes est réel : une main levée peut accompagner une prière pour la pluie ou un vœu formulé après un éternuement ; un orage peut être reçu comme un signe. Cette intersection ne transforme pas des problématiques disjointes en trois versions du même manuscrit. La méthode doit distinguer les liens conceptuels des collisions de cote.

## VII. Contrôles des références matérielles et iconographiques

**Les mains.** Tout objet comme une statuette votive de Tell Asmar, un relief d'Akhétaton, une dexiosis funéraire attique ou un relief de *dēxiosis* royale sassanide doit conserver **sa cote, sa datation, son lieu de conservation, sa fonction dans le catalogue et le degré de certitude de l'identification**. L'objet matériel n'est pas un portrait photographique d'un rite. Aucun fichier 2,5D ni photographie non autorisée n'est ajouté ici.

**Les nuées.** Le texte propose la **stèle du Baal au foudre AO 15775** parmi d'autres témoins ; vérifier la notice de collection, les droits de la photographie et la différence entre **attribution iconographique** et **reconstitution d'une cérémonie météorologique** avant de proposer un rendu. Les pièces mayas de Chahk ne démontrent pas une filiation ougaritique.

**L'éternuement.** Le skyphos attique du **Peintre de Pénélope**, ancien inventaire **Chiusi 1831**, est documenté par [Françoise Touchefeu-Meynier, *Thèmes odysséens dans l'art antique*](https://www.persee.fr/doc/ista_0000-0000_1975_mon_175_1?pageId=T1_110) ; la scène montre **Pénélope et Télémaque devant un métier à tisser**, **pas** l'éternuement du chant XVII. Cette limite doit figurer dans toute légende. La notice bibliographique situe le vase vers 440–435 avant notre ère ; une indication contradictoire sur sa localisation muséale actuelle doit être résolue auprès de l'institution avant publication d'un crédit photographique.

**Règle générale :** les illustrations seront accompagnées d'une légende savante et d'une source primaire ou d'un catalogue officiel ; aucun droit ne doit être déduit du simple fait qu'une image se trouve sur Internet. La charte anthracite, noir, ivoire et or concerne les pages du site, non les photographies d'objets antiques qui doivent rester fidèles à leur contenu.

## VIII. Décision opérationnelle proposée — sans toucher aux textes

1. **Conserver la première candidature MC-134 (« Les mains ») à son UUID et à son slug actuel.** Laisser le workflow transactionnel déterminer si elle satisfait également les règles scientifiques et éditoriales ; sa priorité chronologique ne garantit pas son allocation.
2. **Conserver intégralement « Les nuées » et « L'éternuement » sous leurs UUID en retenue**, avec les deux SHA-256 explicitement enregistrés. Ne lever aucun hold et ne supprimer aucune entrée d'inbox.
3. **Ne pas réémettre une seconde demande pour ces mêmes textes** ni attribuer arbitrairement MC-135 ou MC-136 ; il faut une décision éditoriale de requalification fondée sur une lecture actualisée des cotes historiques, des sujets, de la file et de leurs reçus, avec conservation de l'archive originale. Le présent rapport n'effectue pas cette requalification.
4. **Ne pas réserver un numéro canonique** à partir du volume CCCLIX (359). Toute allocation doit être faite par GitHub Actions sur un état courant de main, selon docs/PUBLICATION_CONCURRENTE.md.
5. **Contrôler la publication publique séparément.** Au dernier contrôle de cette rédaction, le manifeste de bobmythos.fr renvoyait au commit **431efebb2e2e59e91a6d9b2c278bea7a1a395396** ; il ne prouvait pas la publication de MC-133 ni de MC-134. Vérifier à nouveau /catalog/publication-verification.json et la page HTTPS exacte après un workflow abouti.
6. **Faire la relecture scientifique des trois textes avant décision de publication** : langues et graphies, témoins, éditions, iconographie et droit d'usage. Le contrôle d'une source numérique consultable n'est pas une collation exhaustive d'un appareil critique.
7. **Conserver les autres séries** — Origines du sacré, Encyclopédie grecque, Tragédies, Comédies, Philosophie et Reconstitutions 3D — et leurs planifications. Aucun fichier de ces séries n'entre dans la présente modification.

## IX. Validation et statut du présent document

- **Ce qui est vérifié :** existence des trois JSON et de leurs Markdown complets sur main ; ordre des commits ; deux retenues ; absence de reçu attribué aux trois UUID lors du contrôle ; présence des textes et notices primaires et secondaires cités dans la section V.
- **Ce qui est partiel :** collation mot à mot des originaux grecs, des tablettes et des éditions modernes ; vérification des licences des photos et du dossier sanskrit.
- **Ce qui est non vérifié :** attribution ultérieure d'une nouvelle cote historique aux deux manuscrits en retenue et déploiement public de la première candidature.
- **Ce qui est hypothétique :** toute filiation historique directe entre les cultures rapprochées dans les trois études.
- **Ce qui n'est pas autorisé par le document :** fusion, suppression, levée des retenues, affectation manuelle des volumes, création d'un troisième texte copié ou changement de planification.

Cette note doit être soumise à relecture dans une **pull request documentaire distincte**, sans fusion automatique. Elle ne produit aucun volume nouveau et ne prend aucune place dans la numérotation canonique.

**Contrôle attendu du commit de la PR :** le seul chemin ajouté doit être docs/MYTHOS_MC134_RECONCILIATION_TROIS_MANUSCRITS_2026-11-07.md.
