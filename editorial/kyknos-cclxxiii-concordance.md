# Achéos d’Érétrie — *Kyknos* / *Cycnos* (Κύκνος)

## Concordance philologique, bibliographique et éditoriale — MYTHOS, 6 novembre 2026

**Décision : une seule œuvre antique, une monographie canonique publiée (volume CCLXXIII, 273), deux manuscrits critiques intégraux conservés en retenue SHA-256.** Cette concordance n’attribue aucun autre volume, ne modifie aucun reçu, ne réécrit aucun original et ne prétend pas restituer l'intrigue du drame perdu. Voir [l'issue 109](https://github.com/Bobcribb/Bobcribb.github.io/issues/109).

### 1. Identité, provenance et intégrité

| Statut | UUID immuable | Fichier source | SHA-256 du JSON brut |
| --- | --- | --- | --- |
| **Édition canonique CCLXXIII (273)** | 276c0f58-3e65-46b3-b275-f9319343b82d | editorial/inbox/276c0f58-3e65-46b3-b275-f9319343b82d.json | ee84e0e0f7cf0614502ac3145cc0de711c67ba66a83d8191a59e38e3f4c00ca9 |
| **Retenue A — tradition du fils d'Arès** | 9ba73d62-cc3a-4db9-8d67-10f2afc7e581 | editorial/inbox/9ba73d62-cc3a-4db9-8d67-10f2afc7e581.json | c769caacbf80f156667fedcc4fd464d53d6015a99c2b22a71c9e5bcf383c3f2a |
| **Retenue B — critique de la transmission et de la valeur** | e4c7b801-1ab2-4e0a-9012-729b3d60c657 | editorial/inbox/e4c7b801-1ab2-4e0a-9012-729b3d60c657.json | ccd20a249cf3080336d0ae2812a8bc5ce06d2a3d4cee636c693db4c592dce110 |

Les trois empreintes ont été **recalculées indépendamment sur les octets UTF-8 intégraux de chacun des trois JSON**, puis confrontées au reçu de editorial/numbering.json et aux deux entrées de editorial/holds.json : **trois correspondances exactes**. Les longueurs constatées des trois textes Markdown sont respectivement **61 968, 64 781 et 49 967 caractères**. Sur les paragraphes longs normalisés de plus de 120 caractères, **aucun paragraphe identique** entre les manuscrits (critère de répétition littérale, non mesure d'indépendance intellectuelle). Les slugs demeurent distincts.

Le reçu de la collection tragedies pour l'UUID 276c0f58… porte **number = 273**, **request_sha256 = ee84e0e0…** et le chemin canonique ci-dessous. Les UUID 9ba73d62… et e4c7b801… ne possèdent pas de reçu et demeurent en retenue. Il ne faut ni modifier les empreintes, ni déplacer les manuscrits, ni les réinjecter dans la file de numérotation.

**Étude de référence :** [Volume CCLXXIII — *Kyknos*](https://bobmythos.fr/chapitres/tragedies/volume-cclxxiii-acheos-eretrie-kyknos-cycnos-orge-or-ivoire-heracles-ares-athenee-270e/).

**Source Markdown canonique :** chapitres/tragedies/volume-cclxxiii-acheos-eretrie-kyknos-cycnos-orge-or-ivoire-heracles-ares-athenee-270e.md.

### 2. Noyau philologique commun — établir le certain avant le possible

1. **Œuvre et titre :** Achéos d'Érétrie, Κύκνος (*Kyknos*, *Cycnos*), **titre 12** dans la [concordance FragTrag1, Achaeus I](https://fragtrag1.upatras.gr/exist/apps/fragtrag/indexc.html), entre Κατάπειρα et Λίνος Σατυρικός. Le classement de MYTHOS dans les tragédies n'établit pas à lui seul le sous-genre : l'hypothèse satyrique doit rester distinguée d'une attestation.
2. **Correspondances de fragments :** FragTrag1 **fr. 25 et 26** ↔ **TrGF I, 20 F 24 + F 43** (ensemble éditorial) ; FragTrag1 **fr. 27** ↔ **TrGF I, 20 F 25**. Le signe « + » ne prouve ni une continuité de répliques ni deux scènes.
3. **Témoin situé :** Athénée, *Deipnosophistes* **VI, 270e** transmet la comparaison de la nourriture d'orge avec l'or et l'ivoire libyen, selon l'état de faim du sujet ; [index de S. Douglas Olson](https://www.digitalathenaeus.org/tools/OlsonIndex/digger.php?onoffswitch=on&what%5B%5D=Name%7CAchaeus+of+Eretria), **TrGF 20 F 25**. La traduction du sens est assurée, mais **aucune collation exhaustive des variantes grecques de VI, 270e, F 24 et F 43 n'est réalisée dans les trois manuscrits** : ne pas certifier mètre, leçon ou locuteur.
4. **Identité du protagoniste et intrigue :** non déterminables. Le Kyknos fils d'Arès affronté par Héraclès, le Kyknos de la tradition troyenne affronté par Achille, le père de Ténès et les personnages associés à des métamorphoses doivent rester séparés selon les sources, sans fusion des généalogies.
5. **Témoignages parallèles, non fragments du drame :** *Bouclier d'Héraclès* pseudo-hésiodique, Pindare, Pseudo-Apollodore, Aristote (*Rhétorique* II, 22, 1396b), Ovide et mythographes. Les vers épiques, descriptions de vases, allusions lyriques et épisodes tardifs ne sont pas des descriptions certifiées de la représentation d'Achéos.

### 3. Concordance intégrale des axes de recherche (repères de sections)

| Axe | Volume 273 (source canonique) | Retenue A : 9ba73d62… | Retenue B : e4c7b801… | Décision |
| --- | --- | --- | --- | --- |
| Auteur, titre, genre et méthode | II–IV, XXXVIII–XL | I–V, XVII, XXXVII | I §§1–8, V §§34–38 | Noyau déjà publié ; expliciter l'incertitude du genre |
| Concordance FragTrag/TrGF | IV, XI, annexes I–III | IV–V, annexe A | I §6, V §§35–37, VIII §60 | Même chaîne éditoriale, non trois témoins indépendants |
| Athénée VI, 270e et économie de la faim | V–X, XXVIII, XXXIII | IV–V, XXIV et XXXVII | II §§9–18, IV §§27–33, VI §§39–47 | Conserver 273 ; retenir la grille de provenance et les parallèles supplémentaires de B |
| Homonymes et généalogies | XII–XIX, XXXVI–XXXVII | VI–IX, XVI, annexe A | III §§19–26 | Complément A pour Colonai/Ténès et l'examen plus détaillé des contre-exemples |
| Héraclès, Arès, Athéna, espace sacré | XIII–XV, XX, XXV, XXXIV | X–XV, XXII–XXIV, XXIX–XXXI | III §§20,25 ; IV §32 | Complément A : témoin pseudo-hésiodique segmenté et analyse de la tombe |
| Scénarios dramaturgiques et degrés de preuve | I, XXV–XXIX, XXXVIII–XLI | XXXII–XXXVI, XL, annexe E | V §§34–38, VIII §§55–60 | Aucune reconstruction présentée comme pièce attestée |
| Philosophie et anthropologie | VII–X, XXX–XXXV | XXIV–XXVIII, XXXVIII | IV §§27–33, VI §§39–47 | B ajoute Aristote (χρεία), Solon, Hésiode et Marx comme comparaisons **modernes ou externes**, pas comme sources dramatiques |
| Iconographie et archéologie | XXI–XXIV, annexe IV | XVIII–XXI, XXXIX, annexe D | VII §§48–54 | Louvre / Hambourg / British Museum communs ; Met / Petit Palais propres à B |
| Références bibliographiques | annexes II–III | annexes B–D | IX §§61–62 | Consolider la bibliographie, distinguer édition critique, synthèse et simple notice de catalogue |

Cette concordance est une **cartographie de textes complets**, non une comparaison de leurs seuls intitulés. L'absence de répétition littérale de paragraphes longs ne supprime pas le fort **recouvrement documentaire et interprétatif**. Une bibliographie présente dans les trois fichiers n'est pas trois attestations.

### 4. Complément scientifique A — mythographie du fils d'Arès et politique de la violence

**Apports justifiant un dossier documentaire distinct lié au volume 273, mais non un nouveau volume à ce stade :**

- Une segmentation suivie du *Bouclier d'Héraclès* : **vv. 57–76, 325–399 et 400–480**, avec la place d'Iolaos, l'intervention d'Athéna, la mort de Kyknos, la blessure d'Arès et la disparition du tombeau sous l'action de l'Anaure. Cette dernière tradition ouvre une étude spécifique des rites, de la mémoire et de l'effacement du vaincu ; elle n'est pas une scène attestée d'Achéos.
- Un inventaire critique plus dense des **Cycnoi homonymes**, notamment le dossier Colonai/Ténès/Hémithéa, les récits troyens et leurs contradictions, l'*Épitomé* pseudo-apollodorienne et Aristote, *Rhétorique* 1396b. L'identification indexée par MANTO au fils d'Arès est un argument documentaire, non une preuve de distribution dramatique.
- La comparaison de **Pindare, *Olympique* X**, avec le pseudo-Hésiode, la question du sanctuaire d'Apollon, la différence entre violence légitime et filiation divine, et des scénarios explicitement réfutables (duel, conséquences funéraires, éventuel cadre satyrique).
- L'appareil spécialisé : **Richard Janko**, « The Shield of Heracles and the Legend of Cycnus », *Classical Quarterly* 36/1 (1986), 38–59, DOI 10.1017/S0009838800010521 ; **H. A. Shapiro**, « Herakles and Kyknos », *American Journal of Archaeology* 88/4 (1984), 523–529, DOI 10.2307/504740 ; **Krumeich, Pechstein, Seidensticker** (1999), et **O'Sullivan, Collard** (2013).

**Arbitrage :** préserver intégralement le manuscrit A en retenue. Il mérite un **complément analytique thématique** (« Mythographie, sanctuaire et mémoire du combat »), associé par renvoi à 273, sans fichier numéroté et sans altération de ses citations.

### 5. Complément scientifique B — philologie du fragment, économie de la valeur et histoire des images

**Apports justifiant un second dossier documentaire distinct lié au volume 273, sans duplication canonique :**

- Distinction méthodique entre **sens de la citation** et **situation scénique inconnue**, et entre indexation multiple et pluralité de témoins : Athénée VI, 270e, traduction Yonge, traduction Gulick, index Olson et Meineke. Les traductions permettent de comparer le sens ; elles ne remplacent pas la collation grecque ni ne fixent la métrique.
- Une problématique conceptuelle plus étendue : Hésiode (*Travaux et les Jours*), Solon, l'**Éthique à Nicomaque V, 5, 1133a**, où Aristote traite de la **χρεία** (besoin) dans les échanges, et **Marx** sur la valeur d'usage en tant qu'analogie moderne explicitement non rétroprojetée. Éviter de présenter Achéos comme théoricien de l'économie marginaliste ou marxiste.
- Une enquête iconographique **non redondante** avec les trois musées principaux : Metropolitan Museum of Art, cratère à colonnettes **91.1.462**, vers 500 av. J.-C., Héraclès et Kyknos ; lécythe **98.8.3**, vers 500 av. J.-C., même sujet ; **Petit Palais**, kyathos « Lutte d'Héraclès et de Kyknos **(?)** », dont l'attribution reste explicitement interrogative. Les terres cuites d'acteurs et la céramique satyrique citées dans B sont seulement des comparaisons de genre.
- Une matrice de preuve à utiliser lors des corrections : **transmetteur — locus — mots grecs collationnés/non collationnés — édition — traduction — hypothèse — certitude**.

**Arbitrage :** préserver intégralement le manuscrit B en retenue. Il mérite un **complément philologique et iconographique** (« Transmission indirecte, besoin et comparaisons iconographiques »), lié à 273 ; ne pas le transformer en seconde édition de la même œuvre.

### 6. Appareil archéologique — inventaires et statut des rapprochements

| Institution | Inventaire | Identification et date | Fonction documentaire |
| --- | --- | --- | --- |
| Musée du Louvre | **F 36 / cl010269771** | Amphore à figures noires attribuée au Peintre d'Amasis, vers **540 av. J.-C.** ; Héraclès et Kyknos, Athéna (?) et Arès | Tradition figurée antérieure à la pièce ; [notice](https://collections.louvre.fr/ark:/53355/cl010269771) |
| Museum für Kunst und Gewerbe, Hambourg | **1917.471** | Amphore à col, groupe de Léagros/Peintre d'Oxford 569, vers **510–500 av. J.-C.** ; Héraclès, Iolaos, Kyknos | Image archaïque ; [notice](https://www.mkg-hamburg.de/sammlung/objekt/halsamphora-kampf-zwischen-herakles-und-kyknos/1917.471/dc00124099) |
| British Museum | **1837,0609.47 / B158** | Amphore à figures noires, Héraclès et Kyknos selon les notices citées par les monographies | Notice à contrôler avant intégration d'image ; [fiche](https://www.britishmuseum.org/collection/object/G_1837-0609-47) |
| Metropolitan Museum | **91.1.462** | Cratère à colonnettes, manière du peintre de Göttingen, env. **500 av. J.-C.** | Complément B ; [notice](https://www.metmuseum.org/art/collection/search/245619) |
| Metropolitan Museum | **98.8.3** | Lécythe à figures noires, env. **500 av. J.-C.** | Complément B ; [notice](https://www.metmuseum.org/art/collection/search/246715) |
| Petit Palais / Paris Musées | Kyathos à fond blanc, notice « Héraclès et Kyknos (?) » | Identification **incertaine** | Complément B ; [notice](https://parismuseescollections.paris.fr/fr/petit-palais/oeuvres/kyathos-a-fond-blanc-lutte-d-heracles-et-de-kyknos) |

**Règle commune :** aucune céramique n'est un témoignage de la scénographie de la pièce d'Achéos ; aucune nouvelle image, aucune attribution à une représentation réelle, aucun fichier WebP et aucune reconstitution 2,5D ne sont créés par cette concordance. Crédit, droits, date et cote obligatoires avant publication de média.

### 7. Bibliographie de référence et lacunes à ne pas dissimuler

- **Fragments et éditions :** Bruno Snell, Richard Kannicht, *Tragicorum Graecorum Fragmenta* I, auteur 20, F 24, F 25, F 43 ; August Nauck, *Tragicorum Graecorum Fragmenta*, 2e éd., 1889, p. 752 ; [FragTrag1](https://fragtrag1.upatras.gr/exist/apps/fragtrag/indexc.html).
- **Transmission :** Athénée, *Deipnosophistes* VI, 270e ; [Digital Athenaeus / Olson](https://www.digitalathenaeus.org/tools/OlsonIndex/digger.php?onoffswitch=on&what%5B%5D=Name%7CAchaeus+of+Eretria) ; traductions de C. D. Yonge et de C. B. Gulick (vérification de sens, non établissement du grec).
- **Mythographie :** *Bouclier d'Héraclès* pseudo-hésiodique ; Pindare, *Olympiques* II et X, *Isthmique* V ; Pseudo-Apollodore, *Bibliothèque* II, 7, 7 et *Épitomé* III, 23–31 ; Aristote, *Rhétorique* II, 22.
- **Interprétation du duel et des images :** Janko (1986), Shapiro (1984), références intégrales en §4 ; catalogues institutionnels en §6.
- **Philosophie comparative (non preuves sur le texte perdu) :** Platon, Aristote, Hegel, Nietzsche ; Hésiode, Solon et Marx sont à distinguer par époque, genre et objet théorique.
- **Contrôle restant :** texte grec et apparats intégraux du *TrGF* et de FragTrag1, variantes manuscrites d'Athénée, établissement métrique des unités fragmentaires, vérification de détail des scolies et des éventuelles identifications mythographiques. Ne pas annoncer de collation réalisée sans accès effectif aux témoins.

### 8. Publication et indexation contrôlées le 6 novembre 2026

- **Publication effective :** l'URL HTTPS du volume 273 est accessible et restitue le titre et ses **47 entrées de sommaire**.
- **Navigation :** le portail public [Théâtre grec](https://bobmythos.fr/theatre/) contient le lien vers le volume 273 ; il apparaît dans le sommaire de la collection dans le HTML de la branche main.
- **Sitemap :** l'URL canonique 273 figure dans [sitemap.xml](https://bobmythos.fr/sitemap.xml), dont le site présente **1 694 URL** au contrôle. La présence dans le fichier de recherche volumineux search.json n'a **pas pu être confirmée par une lecture complète du fichier** ; ne pas assimiler ce point à une erreur démontrée.
- **Réserve de rédaction publique :** le préambule/colophon du volume publié contient encore des formulations héritées du manuscrit en file (« sans numéro réservé », numéro « futur »). Elles sont **obsolètes depuis l'attribution officielle 273** ; un correctif ultérieur doit synchroniser source Markdown et rendu HTML, sans toucher au reçu ni au JSON d'origine.

### 9. Décision de conservation et critères de levée des retenues

1. **Conserver CCLXXIII (273)** comme unique référence canonique de *Kyknos* dans MYTHOS.
2. **Garder les deux retenues actives** tant qu'aucune décision éditoriale distincte et documentée n'a été prise. L'existence d'un apport original justifie un **dossier complémentaire**, non automatiquement un volume indépendant.
3. Utiliser les deux manuscrits comme **archives scientifiques intégrales** : A pour le duel, le sanctuaire, les traditions héroïques et l'effacement mémoriel ; B pour la transmission, la valeur conditionnelle, la philosophie du besoin et les céramiques supplémentaires. Renvois vers 273, non duplication du titre dans la numérotation.
4. Ne pas modifier les UUID, les sources, les empreintes, les reçus, les autres études d'Achéos (*Iris*, *Katápeira*, *Linos* et autres), les collections non concernées, les images, les horaires ou les workflows de publication.
5. Si un complément public est ultérieurement envisagé, préparer une **révision scientifique contrôlée** : appariement passage par passage avec 273, vérification des références antiques, des traductions et des droits iconographiques ; décision explicite distincte d'une allocation automatique.

**Conclusion :** les trois textes constituent trois monographies intellectuellement distinctes sur **une seule œuvre antique perdue**. Les deux textes retenus comportent des approfondissements réutilisables et identifiables ; la conservation intégrale et la concordance sont préférables tant à leur destruction qu'à la multiplication non arbitrée des numéros canoniques.
