# MYTHOS — Registre des intégrations contrôlées

Ce registre sert à éviter les doublons et à distinguer les contenus effectivement présents sur GitHub des manuscrits uniquement signalés en conversation ou en Bibliothèque. Une intégration est validée ici uniquement lorsque le texte de la source a été lu intégralement, que la comparaison du texte nettoyé est concluante et que les pages et sommaires ont été reliés.

## 3 novembre 2026 — Migration des monographies

| Cote | Titre | Manuscrit d'origine | Page publiée | Contrôle de reprise |
|---|---|---|---|---|
| MG-02.A | Aphrodite — monographie universitaire intégrale | `MYTHOS-aphrodite-2026-10-28.md` (Bibliothèque) | [Dossier Aphrodite](mythologie-grecque/02-dieux-et-divinites/aphrodite-etude-integrale.html) | Correspondance exacte du texte lisible : 19 755 caractères après suppression des commentaires de blocs WordPress et ajout des ancres de navigation. Bibliographie et exercices conservés. |
| CIV-01 | Perse et Iran ancien — étude de Behistun | `MYTHOS-perse-iran-ancien-2026-10-28.md` (Bibliothèque) | [Dossier Perse et Iran](civilisations/perse-iran-ancien-behistun.html) | Correspondance exacte du texte lisible : 16 929 caractères ; seuls les commentaires Gutenberg et deux chemins internes obsolètes ont été adaptés. Bibliographie et exercices conservés. |

Ces deux pages sont aussi reliées depuis les sommaires thématiques et le sommaire général ; Aphrodite est indexée dans la rubrique Philosophie par une **ancre vers sa propre étude**, sans copie supplémentaire du texte. Les métadonnées de provenance sont conservées dans les pages publiées.

### Portée du contrôle

Le contrôle porte sur **l'intégrité textuelle et la navigation**, non sur la vérification scientifique exhaustive. Les citations anciennes, références, attributions et droits d'illustration exigent une révision savante distincte. Aucune autre section annoncée dans les conversations n'est considérée comme transférée par le présent registre.

### Règles pour les prochaines intégrations

1. Chercher d'abord si la source figure dans ce registre, puis si elle existe déjà dans l'arborescence GitHub.
2. Lire le manuscrit intégral et vérifier le début, la fin, les sources et la bibliographie avant de créer une page.
3. Conserver le texte et son schéma de numérotation d'origine ; créer une cote éditoriale explicite plutôt qu'une renumérotation arbitraire.
4. Ajouter sommaire, références croisées et lien de retour, sans recopier le même contenu sur plusieurs pages.
5. Comparer la version publiée au manuscrit, contrôler l'absence de liens locaux manquants et compléter ce registre uniquement en cas de succès.


## Contrôle du 3 novembre 2026 — exécution suivante

**Inventaire réellement inspecté :** racine du dépôt, `contenus/philosophie/`, `corpus/`, `corpus/mythologie-grecque/`, le registre des récupérations et le sommaire général.

- **Aucun nouveau manuscrit intégral publié lors de cette exécution.** Le document [Homère et Hésiode](../contenus/philosophie/homere-hesiode-dossier-preparatoire.md) est explicitement un *dossier éditorial de préparation*, composé de pistes de développement, d'une bibliographie à compléter et d'une iconographie non vérifiée. Il ne peut pas remplacer les trois études intégrales attendues.
- **Chiron et chapitres 118–133 :** signalés dans [le registre de récupération](mythologie-grecque/REGISTRE-RECUPERATION.md), mais non disponibles sous forme de manuscrits complets dans les sources inspectées ; aucun texte n'a été reconstitué à partir d'un résumé.
- **Aphrodite (MG-02.A) et Perse (CIV-01) :** déjà inscrits et publiés dans ce registre, donc exclus d'une nouvelle migration pour éviter les doublons.
- **Travail technique effectué :** mise à jour de `assets/mythos-reference.css` (grilles mobiles, retour à la ligne, repères de focus et préférence de mouvement réduit). Les fichiers historiques n'ont pas été supprimés, déplacés ou écrasés.
- **Limite de vérification :** le commit CSS peut être confirmé dans GitHub ; aucune capture navigateur réelle ni validation visuelle du déploiement public n'a été réalisée dans cette exécution.

**Action éditoriale suivante :** retrouver le fichier source intégral d'un volume non publié, puis vérifier titres, début, fin, notes, bibliographie et correspondance textuelle avant toute mise en ligne.


## Iconographie philosophique — contrôle de l'exécution du 3 novembre 2026

**Pages réellement identifiées dans `main` :** `/philosophie-iliade.html` (12 sections d'étude), `/philosophie-odyssee.html` (12 sections) et `/philosophie-theogonie.html` (13 sections). Chacune contenait trois figures documentaires avant cette opération. Le document `contenus/philosophie/homere-hesiode-dossier-preparatoire.md` reste séparé, sans duplication de ses paragraphes.

**Ajouts vérifiés après écriture GitHub :**
- `/assets/philosophie/iliade-parcours-ethique.svg` inséré dans `/philosophie-iliade.html` — mênis, choix de la destinée, violence contre Hector, reconnaissance avec Priam.
- `/assets/philosophie/odyssee-identite-reconnaissance.svg` inséré dans `/philosophie-odyssee.html` — Calypso, mêtis, cicatrice, lit conjugal.
- `/assets/philosophie/theogonie-succession-pouvoir.svg` inséré dans `/philosophie-theogonie.html` — puissance primordiale, Ouranos, Cronos et Zeus.
- `/assets/mythos-iconographie.css` enrichi d'un affichage adapté au format des schémas et d'un lien de zoom accessible.

**Statut documentaire :** trois schémas vectoriels originaux édités en 2026 ; ni photographies antiques ni rendus produits par intelligence artificielle. Chaque page contient désormais quatre figures balisées en HTML (trois iconographies documentaires préexistantes + un schéma nouveau). Les SVG portent leurs références aux passages homériques ou hésiodiques ; les textes des études, titres et ancres ont été préservés. Les nombres 12, 12 et 13 désignent des sections, **pas** un nombre de pages A4 certifié : l'exigence de dix pages imprimées par étude reste à vérifier par un contrôle de pagination.

**Vérification :** fichiers et insertions relus depuis l'API GitHub après les commits ; exécution GitHub Pages `41644417144` terminée avec conclusion `success` sur `e7718f2dd656d3cdf1fc4bafb3aa168286638748`. L'accès public au domaine `bobmythos.fr` et le rendu sur navigateur n'ont pas pu être vérifiés via le réseau de cette exécution. Ne pas assimiler le build réussi à une inspection visuelle. L'enrichissement des autres pages se poursuit à partir du catalogue existant `assets/mythos-iconographie.js` ; éviter les doublons de visuels déjà déclarés.


## 3 novembre 2026 — Intégration ODS-S28 : tome XXVIII

| Cote | Document source | Fichiers sur GitHub | Contrôle d'intégrité |
|---|---|---|---|
| **ODS-S28** | `MYTHOS_Origines_du_sacre_Tome_XXVIII_Ch363-370_2026-11-01.md` (Bibliothèque, dossier `MYTHOS-suivi-editorial`, 1er novembre 2026) | [Page de lecture](origines-du-sacre/tome-XXVIII-chapitres-363-370.html) ; [copie Markdown exacte](origines-du-sacre/tome-XXVIII-chapitres-363-370.md) | Source complète lue : **54 221 caractères**, 379 lignes, huit chapitres **363–370**, bibliographie **[S1]–[S19]** et état éditorial terminal conservés. La copie Markdown a été relue depuis GitHub et comparée caractère par caractère à la source : identité exacte. La version HTML est une conversion de lecture avec sommaire, sans suppression volontaire de texte, plus avertissement éditorial ajouté. |

Cette livraison appartient à la **série de suivi** des *Origines du sacré*. Les cotes `ODS-Sxx` distinguent cette série de l'édition cumulative I–XXVII, dont la numérotation ne doit pas être recalculée sans concordance critique. Le manuscrit source était signalé comme non publié sur WordPress au 1er novembre ; il est désormais transféré sur la branche par défaut GitHub au 3 novembre. Son avertissement originel est reproduit tel quel, avec cette clarification en tête de l'HTML.

**Vérifications effectuées :** URL du document source GitHub accessible dans le dépôt ; HTML récupéré de GitHub après création et comparé exactement à la chaîne écrite ; dix liens de sommaire pointent vers des en-têtes générés, dont huit chapitres. Index ODS, sommaire général et page d'accueil mis à jour. **Contrôles restant nécessaires :** bibliographie et identifications scientifiques, apparence navigateur, liens externes, déploiement sur `bobmythos.fr`.

**Aucun doublon des tomes existants n'a été créé.** Les archives historiques I–XXVII restent inchangées.


## 3 novembre 2026 — Iconographie des monographies, contrôle complémentaire

**Base inspectée avant modification :** `philosophie-iliade.html`, `philosophie-odyssee.html`, `philosophie-theogonie.html`, tous présents sur la branche par défaut avec respectivement 12, 12 et 13 sections et **7 figures HTML chacun**. Les images et schémas déjà présents ont été identifiés avant tout ajout ; aucune ancienne figure n'a été remplacée.

**Trois nouvelles figures vectorielles intégrées et relues après commit :**

| Page et chapitre | Fichier SVG ajouté | Source primaire vérifiée | Nature documentaire |
| --- | --- | --- | --- |
| *Iliade*, étude 09 (bouclier d'Achille) | `assets/philosophie/iliade-bouclier-monde.svg` | Homère, *Iliade* XVIII, 478–608 ; [texte de référence](https://www.theoi.com/Text/HomerIliad18.html) | Schéma conceptuel des motifs poétiques, **non** restitution archéologique ; assistance IA déclarée. |
| *Odyssée*, analyse 02 (Télémachie) | `assets/philosophie/odyssee-telemachie-memoire.svg` | Homère, *Odyssée* I–IV, surtout III et IV ; [texte du chant III](https://www.theoi.com/Text/HomerOdyssey3.html), [chant IV](https://www.theoi.com/Text/HomerOdyssey4.html) | Schéma interprétatif de la mémoire et de l'action de Télémaque, **non** carte historique ; assistance IA déclarée. |
| *Théogonie*, étude 11 (Zeus et Métis) | `assets/philosophie/theogonie-zeus-metis.svg` | Hésiode, *Théogonie* 886–900 ; [texte de référence](https://adfonteslibrary.org/work-hesiod-theogony) | Schéma analytique de la souveraineté et de la contrainte, **non** objet antique ; assistance IA déclarée. |

**Contrôle d'intégrité :** l'HTML précédent a été conservé **à l'identique** hors insertion d'une figure `<figure>` avec lien SVG, `<img>` doté de texte alternatif et dimensions, sources, datation de création (2026), légende et déclaration d'assistance IA. Chacune des trois pages comporte maintenant **8 figures**, soit **24 figures au total pour ces trois monographies**. Les six fichiers (trois HTML et trois SVG) ont été relus depuis GitHub après écriture. Aucun titre, texte préexistant, identifiant de section, sommaire, numérotation ni automatisation n'a été modifié.

**Limites de ce contrôle :** sections ≠ pages imprimées ; le minimum de dix pages A4 doit être vérifié en sortie PDF/navigateur. L'API GitHub atteste les fichiers et commits, non l'affichage public. Les tentatives de consultation de `bobmythos.fr` n'ont pas permis d'inspecter la page ou le SVG sur le domaine ; aucun état de déploiement public n'est certifié ici. Pour les prochaines exécutions, reprendre l'inventaire de chaque rubrique avant insertion et ne jamais dupliquer les figures existantes.


## 3 novembre 2026 — Intégration contrôlée : tome XXX de la série MYTHOS-OS-CONV

| Cote | Titre | Provenance | Page de lecture | Manuscrit conservé |
|---|---|---|---|---|
| ODS-CONV-XXX | Pierres sacrées, bétyles, météorites et images aniconiques, chapitres 379–386 | Bibliothèque : `MYTHOS_Origines_du_sacre_Tome_XXX_Ch379-386_2026-11-01.md`, version 1, manuscrit daté du 1er novembre 2026 | [Édition HTML](origines-du-sacre/conv-tome-XXX-chapitres-379-386.html) | [Markdown source exact](origines-du-sacre/conv-tome-XXX-chapitres-379-386.md) |

**Vérification de la source :** lecture complète du fichier, 369 lignes, début et fin présents, huit en-têtes de chapitre (379 à 386), conclusion et section « SOURCES PRIMAIRES ET BIBLIOGRAPHIE CRITIQUE » identifiées ; 56 903 caractères de contenu textuel récupérés puis conservés en Markdown, sans réécriture. Le fichier HTML présente le contenu en blocs de lecture et renvoie au Markdown original pour une confrontation mot à mot. Les chapitres 379–386 appartiennent exclusivement à la série **MYTHOS-OS-CONV** et ne sont pas des subdivisions de MYTHOS-OS-LIB.

**Navigation :** liens ajoutés dans `origines-du-sacre.html`, `sommaire-general.html` et `corpus/sommaire-general.md`. Sommaire de huit chapitres, ancres de conclusion et bibliographie, retour à la collection, lien au manuscrit source. Ni les archives ni les autres automatisations MYTHOS n'ont été modifiées.

**Périmètre du contrôle :** intégrité de la copie source et présence des repères documentaires ; les références scientifiques individuelles ne sont pas toutes revérifiées ici. La disponibilité publique après déploiement reste à confirmer séparément. Le tome XXIX, chapitre 378, est seulement mentionné par la source : aucun faux lien de continuité n'a été créé.


## 3 novembre 2026 — Deux volumes intégraux supplémentaires, série MYTHOS-OS-CONV

| Cote | Tome et chapitres | Source en Bibliothèque, version 1 | Archive exacte dans GitHub | Page HTML |
|---|---|---|---|---|
| ODS-CONV-XXIX | XXIX, chapitres 371–378, arbres sacrés et jardins de l'immortalité | `MYTHOS_Origines_du_sacre_Tome_XXIX_Ch371-378_2026-11-01.md` | [Markdown source](origines-du-sacre/conv-tome-XXIX-chapitres-371-378.md) | [Édition lisible](origines-du-sacre/conv-tome-XXIX-chapitres-371-378.html) |
| ODS-CONV-XXXI | XXXI, chapitres 387–394, images divines et rituels d'animation | `MYTHOS_Origines_du_sacre_Tome_XXXI_Ch387-394_2026-11-01.md` | [Markdown source](origines-du-sacre/conv-tome-XXXI-chapitres-387-394.md) | [Édition lisible](origines-du-sacre/conv-tome-XXXI-chapitres-387-394.html) |

**Contrôle des sources :** lecture du tome XXIX sur 306 lignes sans pagination ; 41 064 caractères textuels, huit chapitres 371–378, bibliographie et fin du fichier. Lecture du tome XXXI sur 1 170 lignes, en deux tranches jointives (1–1000 puis 1001–1170), sans omission ni recouvrement ; 64 741 caractères textuels, huit chapitres 387–394, bibliographie et registre final. Les marques Markdown d'origine sont conservées dans les pages HTML, sans résumé ni condensation. Les archives Markdown rendent possible la confrontation avec les fichiers de Bibliothèque.

**Liens :** `origines-du-sacre.html`, `sommaire-general.html`, `corpus/sommaire-general.md` renvoient aux deux éditions HTML. Chaque nouvelle page contient huit ancres de chapitres, des liens vers sa source Markdown et le retour à la collection ; les tomes se relient au tome XXX déjà présent. Ne pas confondre ces cotes avec les tomes homonymes de MYTHOS-OS-LIB.

**Limites :** l'intégrité documentaire et les liens sont vérifiables dans GitHub, mais l'audit scientifique de chaque citation, la fidélité du rendu visuel sur appareil et le déploiement du domaine public ne sont pas certifiés par cette intervention. Aucun texte précédent ni aucune automatisation n'ont été modifiés.


## 3 novembre 2026 — ODS-CONV-XXVII, feu sacré

**Source retrouvée :** Bibliothèque, `MYTHOS_Origines_du_sacre_Tome_XXVII_Ch355-362_2026-11-01.md`, 338 lignes / 51 508 caractères textuels. Manuscrit intégral lu, contrôle des huit chapitres 355–362, de la bibliographie, des réserves scientifiques et de la fin du document.

- [Archive Markdown sans réécriture](origines-du-sacre/conv-tome-XXVII-chapitres-355-362.md).
- [Page de lecture HTML](origines-du-sacre/conv-tome-XXVII-chapitres-355-362.html), avec huit ancres de chapitre, sommaire, styles responsives et lien vers le tome XXVIII.
- Liens ajoutés dans les pages `origines-du-sacre.html`, `sommaire-general.html` et `corpus/sommaire-general.md`.
- Cote **ODS-CONV-XXVII**. Ne pas confondre le tome XXVII de cette série, consacré au feu, avec celui de **MYTHOS-OS-LIB**, dont le contenu et la numérotation sont différents.
- Les tomes XXV et XXVI de la série conversationnelle ont été localisés dans la Bibliothèque mais ne sont pas intégrés par cette entrée de registre. Ne pas leur attribuer de statut de publication avant contrôle et transfert.
- Contrôle scientifique détaillé des références et déploiement public à vérifier séparément ; aucun fichier d'archive précédent ni aucune automatisation n'a été modifié.


## 3 novembre 2026 — Tomes XXXII et XXXIII, édition MYTHOS-OS-CONV

| Cote | Chapitres / contenu | Source originale (Bibliothèque, 1er novembre 2026) | Archive fidèle | Page HTML |
| --- | --- | --- | --- | --- |
| **ODS-CONV-XXXII** | 395–402 — Corps humains, possession, masques et incarnations rituelles | `MYTHOS_Origines_du_sacre_Tome_XXXII_Ch395-402_2026-11-01.md` | [Markdown](origines-du-sacre/conv-tome-XXXII-chapitres-395-402.md) | [Lecture avec sommaire](origines-du-sacre/conv-tome-XXXII-chapitres-395-402.html) |
| **ODS-CONV-XXXIII** | 403–410 — Voix du sacré : hymnes, chants, musique et silence | `MYTHOS_Origines_du_sacre_Tome_XXXIII_Ch403-410_2026-11-01.md` | [Markdown](origines-du-sacre/conv-tome-XXXIII-chapitres-403-410.md) | [Lecture avec sommaire](origines-du-sacre/conv-tome-XXXIII-chapitres-403-410.html) |

**Contrôle d'intégralité :** tome XXXII, 392 lignes et **60 944 caractères textuels** ; tome XXXIII, 366 lignes et **54 867 caractères textuels**. Chaque fichier de Bibliothèque a été lu du début à la dernière ligne. Les copies Markdown récupérées depuis GitHub sont **strictement identiques caractère par caractère** aux manuscrits accessibles : aucun chapitre, source, bibliographie ou registre final tronqué, renommé ou résumé dans ces archives. Huit en-têtes de chapitre contrôlés par tome ; les seize ancres de chapitre et les seize liens du sommaire sont présents dans les deux lecteurs HTML. Les pages proposent un lien vers la source vérifiée et une mise en page responsive noir et or ; leur transcription en HTML préserve les marques Markdown pour assurer la traçabilité. Ces documents sont de statut **manuscrit universitaire de travail**, non des éditions scientifiques revues ligne à ligne.

**Navigation et graphisme :** lecteur responsive commun `assets/mythos-volume-lecture.css`, avec bandeau vectoriel local « statue à gauche, temple à droite » (déjà présent : `assets/mythos-hero.svg`), sommaires internes, pages sources, tomes précédent/suivant ; ajout de deux **cartes illustrées responsives** dans `origines-du-sacre.html`, à partir des motifs graphiques locaux `assets/mythos-archaeology-tiles.svg` explicitement présentés comme décoratifs. Liens ajoutés dans `sommaire-general.html`, `corpus/sommaire-general.md` et sur l'accueil `index.html`. Liens de progression intégrés aux lecteurs XXX et XXXI sans modifier leurs transcriptions d'origine. La collection de référence **MYTHOS-OS-LIB** reste distincte.

**Correction de catalogue :** remplacement de trois séquences littérales `\\n` erronées par de véritables retours à la ligne dans le sommaire Markdown ; correction d'un chemin relatif erroné vers le recueil I–XXVII.

**Limites :** la disponibilité sur GitHub et la reprise documentaire sont vérifiées. Aucune vérification bibliographique exhaustive, aucun test visuel dans tous les navigateurs et aucune garantie de déploiement de bobmythos.fr ne sont revendiqués. Aucune automatisation MYTHOS n'a été modifiée.

**Contrôle pré-déploiement GitHub Pages :** le workflow `.github/workflows/pages.yml` vérifie désormais la présence des deux lecteurs et des deux sources Markdown, un seuil de taille de 50 000 octets par manuscrit, les ancres des premiers/derniers chapitres et celles des bibliographies, ainsi que le lien de la collection vers le tome XXXIII. Ce garde-fou n'atteste pas à lui seul que le déploiement public a réussi.


## 3 novembre 2026 — ODS-CONV-XXV et XXVI : récupération de deux manuscrits intégraux

**Audit préalable :** inspection de l'arborescence GitHub et recherche dans la Bibliothèque. Les tomes XXV (339–346) et XXVI (347–354) de **MYTHOS-OS-CONV** étaient absents de `corpus/origines-du-sacre/`. Le tome XXVII (355–362) était déjà présent. La collection **MYTHOS-OS-LIB** utilise une autre numérotation et n'a pas été fusionnée.

- **ODS-CONV-XXV — Sanctuaires, espaces sacrés et géographie religieuse.** Source `MYTHOS_Origines_du_sacre_Tome_XXV_Ch339-346_2026-11-01.md`, 316 lignes, **47 280 caractères**, chapitres 339–346 (8/8), introduction, conclusion, bibliographie critique et registre. [Source Markdown sans réécriture](origines-du-sacre/conv-tome-XXV-chapitres-339-346.md) ; [page de lecture](origines-du-sacre/conv-tome-XXV-chapitres-339-346.html).
- **ODS-CONV-XXVI — Les eaux sacrées et les cosmologies de la régénération.** Source `MYTHOS_Origines_du_sacre_Tome_XXVI_Ch347-354_2026-11-01.md`, 260 lignes, **35 509 caractères**, chapitres 347–354 (8/8), conclusion, sources primaires, bibliographie et registre. [Source Markdown sans réécriture](origines-du-sacre/conv-tome-XXVI-chapitres-347-354.md) ; [page de lecture](origines-du-sacre/conv-tome-XXVI-chapitres-347-354.html).

**Vérifications après écriture :** les deux fichiers Markdown ont été relus depuis GitHub. Comparaison directe de la transcription HTML avec le texte source après extraction de la seule ligne de titre des chapitres (affichée dans les titres `h2` des lecteurs) : **46 636/46 636 caractères strictement identiques** pour XXV et **34 795/34 795** pour XXVI. Les 16 ancres internes, leurs liens de sommaire, deux conclusions et deux bibliographies sont présents. Le script `scripts/check-origines-conv-xxv-xxvi.py` vérifie ces propriétés et les liens locaux dans le workflow GitHub Pages.

**Navigation et graphisme :** deux nouvelles cartes illustrées responsives dans `origines-du-sacre.html` ; liens dans `sommaire-general.html`, `corpus/sommaire-general.md` et `index.html` ; retour XXVII → XXVI et enchaînement XXV → XXVI → XXVII. Lecteur noir et or partagé, bandeau `assets/mythos-hero.svg` (statue à gauche, temple à droite), cibles de navigation plus visibles et focus clavier renforcé dans `assets/mythos-volume-lecture.css`. Les illustrations des cartes sont **décoratives**, non des reconstitutions historiques.

**Limites :** l'intégrité documentaire est contrôlée dans le dépôt, mais cela ne vaut ni audit philologique exhaustif ni garantie d'affichage sur le domaine public. Le tome XXIV ODS-CONV n'est pas déclaré intégré. Aucun changement aux autres archives ni aux automatisations MYTHOS.


## 3 novembre 2026 — ODS-H-487 transféré vers le dépôt actif

**Détection et correction du dépôt cible :** `Bobcribb/Mythos` est une archive historique ; la publication du domaine `bobmythos.fr` utilise `Bobcribb/Bobcribb.github.io` (branche `main`). Les commits réalisés uniquement dans l'archive ne valent pas publication.

**Intégration documentaire :** `corpus/origines-du-sacre/chapitre-487-iran-inde-mithra-rta-satya.md` est la copie intégrale du manuscrit historique `chapitres/origines-du-sacre/487-iran-inde-mithra-rta-satya.md` (blob Git `70d6aef3fcdecb993f6c2d3bbd7d52969821d9a3`, 4 391 caractères). Lecteur associé `corpus/origines-du-sacre/chapitre-487-iran-inde-mithra-rta-satya.html`, six sections 487.1–487.6, appareil de sources et bibliographie, thème sombre et or, navigation vers source et sommaires. Liens ajoutés à `origines-du-sacre.html`, `sommaire-general.html`, `corpus/sommaire-general.md` sur le **dépôt actif**, sans suppression d'archives ni renumérotation ODS-CONV/ODS-LIB.

**Statut :** fichiers et entrées de sommaire enregistrés dans GitHub. Une réussite du build GitHub Pages et un contrôle HTTP du domaine public sont nécessaires pour déclarer la page effectivement publiée. Les références scientifiques n'ont pas fait l'objet d'une collation indépendante.


## 3 novembre 2026 — Portail unifié de l'Encyclopédie mythologique grecque

**Dépôt actif :** `Bobcribb/Bobcribb.github.io`, branche `main`. **Entrée canonique :** [`/mythologie-grecque/`](https://bobmythos.fr/mythologie-grecque/). Un lien prioritaire noir et or avec bannière statue grecque à gauche et temple à droite a été ajouté à l'accueil, et des renvois ont été ajoutés au sommaire général HTML, au sommaire fusionné Markdown, à l'index MG et à l'ancien portail `mythologie-grecque.html`.

**Inventaire issu du générateur automatique** `scripts/build_greek_corpus.py` : **55 chapitres** de `chapitres/encyclopedie/` dont les textes complets ont déjà leur lecteur HTML ; **14 archives HTML** dans `corpus/mythologie-grecque/archives/` ; **15 notices de dieux** ; **16 notices de héros** ; **1 monographie MG**, plus des renvois savants vers les analyses et collections conservées à leur emplacement d'origine. Au total, **107 liens distincts** dans le catalogue nouveau, sans duplication du texte des sources. L'inventaire est recalculé depuis les fichiers présents à chaque publication. Les études de la Grande Encyclopédie sont reliées, mais **non déplacées ni reclassées** dans la collection MG ; la numérotation historique reste intacte, y compris les chapitres homonymes.

**Contrôle automatique GitHub Actions :** le premier audit du portail a validé la reconstruction de cet inventaire, avec `HARD ERRORS: 0` et `WARNINGS: 0`, contrôle des liens internes, des fichiers médias et des dossiers indexés. Cela atteste le site généré, et non l'existence de tous les manuscrits jamais évoqués.

**Archives et lacunes :** aucun texte intégral n'a été supprimé ou remplacé par un résumé. Chiron et chapitres 118–133, ainsi que les chapitres historiques 218–224, restent signalés dans `corpus/mythologie-grecque/REGISTRE-RECUPERATION.md` tant que leur texte intégral n'est pas recollationné. Cette entrée ne doit pas faire croire à leur publication. Le rendu mobile et l'URL publique sont à tester après le déploiement correspondant ; la révision scientifique exhaustive des références ne découle pas du contrôle d'intégrité.


## 3 novembre 2026 — Portail complet MG : encyclopédie mythologique grecque

**Portail unique de consultation :** [Encyclopédie mythologique grecque](../mythologie-grecque.html), désormais séparée de la Grande Encyclopédie transversale, de la Mythologie comparée et des collections théâtre/Origines du sacré. L'entrée est reliée à l'accueil `index.html`, au menu commun `scripts/build_navigation.py`, au sommaire HTML et Markdown, et au portail historique `mythologie-grecque/index.html`. La recherche et le plan du site sont configurés pour indexer son URL exacte `/mythologie-grecque.html` dans `scripts/build_native.py`.

**Inventaire effectué sur `main` :** 55 manuscrits `chapitres/encyclopedie/chapitre-*.md` associés aux pages de lecture, 14 archives HTML dans `corpus/mythologie-grecque/archives/` (dont une bibliothèque historique multithématique), 15 entrées individuelles de divinités `dieu-*/`, 17 entrées du domaine des héros (y compris ses pages transversales), les quatre grands cycles archivés, les études philosophiques des épopées et 19 autres dossiers grecs complémentaires publiés. Le portail conserve les chapitres distincts qui portent les mêmes numéros historiques 314, 315 et 353 et donne un lien vers les sources Markdown dans GitHub. Aucune copie condensée ni suppression de source.

**Contrôle de cohérence :** 55 liens distincts vers les chapitres de la série encyclopédique ; 145 chemins locaux uniques du portail ont été confrontés aux fichiers de la branche principale, sans cible absente ; huit rubriques d'ancrage, aucun identifiant HTML dupliqué. Le visuel de bannière statue à gauche / temple à droite est un SVG éditorial, distinct des objets archéologiques. Page responsive et recherche locale des chapitres. L'intégration dans l'HTML public après déploiement GitHub Pages reste à vérifier indépendamment du commit.

**État documentaire :** cette entrée couvre le corpus actuellement identifié dans le dépôt, et non tous les textes signalés dans des conversations antérieures. Les chapitres Chiron 118–133 et 218–224 restent soumis au [registre de récupération](mythologie-grecque/REGISTRE-RECUPERATION.md). La présence d'un chapitre sur une page de consultation n'atteste pas une collation philologique indépendante de toutes les sources et éditions anciennes. Aucun autre automate MYTHOS n'a été modifié.



## 4 novembre 2026 — Pagination A4 et enrichissement des trois études philosophiques

**Dépôt actif :** `Bobcribb/Bobcribb.github.io`. Contrôle des textes initiaux, de leur mise en page et de leurs liens. Les anciennes règles `min-height:250mm` et les sauts de page systématiques par section gonflaient artificiellement la pagination ; elles sont retirées au profit d’un flux continu.

| Étude | Analyse seule initiale | Analyse seule enrichie | PDF complet illustré | Mots d’analyse | Figures conservées |
|---|---:|---:|---:|---:|---:|
| Iliade | 7 pages | 10 pages | 18 pages | 4 279 | 13 |
| Odyssée | 7 pages | 10 pages | 17 pages | 3 964 | 12 |
| Théogonie | 7 pages | 10 pages | 19 pages | 4 001 | 15 |

**Protocole :** A4 210 × 297 mm, marges de 25 mm, Nimbus Roman 12 points, interligne 1,5, titres 15 points ; WeasyPrint 70.0. Les deux états sont mesurés avec la même mise en page. La mesure d’analyse seule exclut titre de dossier, notice, sommaire, images, légendes, références et bibliographie ; titres de section conservés, dernière page éventuellement partielle. Un essai typographique préliminaire avait donné 9/8/9 pages : il ne constitue pas la mesure comparative définitive. Les six PDF fixent le résultat ; l’impression navigateur peut différer selon les polices disponibles.

**Enrichissement :** trois compléments A–C par étude, sans renumérotation du noyau initial. Iliade : responsabilité d’Agamemnon, justice des jeux funèbres, voix de Briséis. Odyssée : commandement sous contrainte, discrimination des responsabilités et servantes, reconnaissance réciproque avec Pénélope. Théogonie : parole des rois et des Muses, Hécate/Styx et les honneurs, serment et exclusion. Références localisées aux passages antiques, bibliographies universitaires identifiables ; deux précisions distinguent la paraphrase de la vie chez Achille et le nom de Pandore absent de la Théogonie. Aucune revendication de collation philologique exhaustive ou d’évaluation par les pairs.

**Intégrité :** comparaison de chaque section initiale par identifiant et texte lisible : 12/12, 12/12, 13/13 conservées, y compris toutes les légendes et bibliographies. Les neuf photographies/reproductions externes sont copiées à l’identique dans `assets/philosophie/documents/`, URLs d’origine dans `data-original-src`, provenance et droits inchangés. Les 31 SVG existants sont conservés. Toutes les ancres locales des études sont valides, aucun identifiant dupliqué, 40 fichiers d’images présents.

**Navigation :** trois études et audit reliés depuis `philosophie.html` et `philosophie/index.html`. Modification de `scripts/build_navigation.py` afin que le portail `/philosophie/` conserve les liens aux reconstructions ; génération isolée testée. La dernière version du portail récupérée pendant l’intervention est préservée par insertion du bloc supplémentaire.

**Affichage :** contrôle visuel en navigateur de prévisualisation, à 360 et 768 pixels pour les trois études ; largeurs de contenu 345/753 pixels après barre verticale, sans débordement horizontal de la page. Navigation sur plusieurs lignes, accès aux compléments et lecture vérifiés. Contrôle des pages PDF rendues : images, légendes, marges et pagination. Il ne s’agit pas d’un essai physique sur tous les appareils.

**Pièces de contrôle :** [rapport public et six PDF](../philosophie-audit-pagination-2026-11-04.html), [mesures et empreintes](../assets/philosophie/pagination-2026-11-04.json), [manifeste des images](../assets/philosophie/documents/manifest.json), script `scripts/render_philosophie_a4.py`. Les états de publication GitHub Pages doivent être contrôlés après le commit ; ce registre de préparation ne confond pas validation locale et déploiement public.


## 4 novembre 2026 — Études longues : cent pages d’analyse par œuvre

L’objectif éditorial est porté à **au moins 100 pages A4 d’analyse pour chacune des trois œuvres**, hors images, légendes, références et bibliographies. Ce seuil remplace celui de dix pages dans la préparation précédente ; il ne repose ni sur le nombre de sections ni sur une estimation de caractères.

| Œuvre | Mots d’analyse | Pages d’analyse seule | Volume illustré | Figures conservées |
| --- | ---: | ---: | ---: | ---: |
| Iliade | 48677 | 107 | 122 | 14 |
| Odyssée | 47341 | 101 | 116 | 13 |
| Théogonie | 48394 | 103 | 117 | 16 |

**Développement :** 72 nouveaux chapitres argumentatifs (24 par œuvre), organisés en lectures suivies des chants et des séquences poétiques. Sources antiques localisées, objections et limites des rapprochements modernes ; bibliographies conservées et relevés de consultation publiés. Une relecture croisée a notamment précisé les passages sur Apollon et Patrocle, le serment d’Héra, la descendance monstrueuse, les Océanides et l’état transmis de la fin de la Théogonie.

**Mise en page :** A4, marges 25 mm, Nimbus Roman 12 points, interligne 1,5, texte continu sans saut forcé par chapitre. Les six PDF de référence sont dans `assets/philosophie/pdf/`. Mesures et empreintes : `assets/philosophie/pagination-2026-11-04.json`. Script reproductible : `scripts/render_philosophie_a4.py` (seuil par défaut : 100 pages).

**Conservation :** 37 sections initiales, leurs textes, bibliographies et légendes conservés intégralement. Les trois photographies ajoutées entre-temps au dépôt sont également conservées : 43 figures au total (31 SVG, 12 documents photographiques ou iconographiques), avec copies locales et provenance. Empreintes de l’état antérieur à l’extension : `corpus/philosophie/reference-avant-extension.json` ; contrôles : `scripts/check_philosophie_integrity.py` et `assets/philosophie/integrite-2026-11-04.json`. Aucun paragraphe analytique long dupliqué.

**Accès et présentation :** liens vers les trois études intégrales depuis les deux entrées Philosophie, et conservation de ces liens dans le générateur. Sommaire repliable des 24 lectures par œuvre, retours au sommaire et navigation immédiate par ancre. Prévisualisation à 360 et 768 pixels avec le graphisme courant : aucune largeur de page débordante ; texte, sommaires et ancres contrôlés. Les PDF ont été rendus et inspectés, sans débordement de texte ni caractère de remplacement détecté.

Ce relevé atteste la préparation et les vérifications de l’édition ; la réussite du déploiement doit être constatée séparément après intégration. Il ne revendique pas une évaluation académique par les pairs.
