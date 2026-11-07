# MYTHOS — Revue scientifique, lot 04 — 7 novembre 2026

**Issue maîtresse :** [#158](https://github.com/Bobcribb/Bobcribb.github.io/issues/158).  
**Méthode :** ajout de notes datées à des manuscrits existants et contrôle documentaire d'une reconstitution ; aucune réécriture, aucun changement de numéro, d'UUID, de reçu, d'image, de calendrier ni de texte ancien. La branche est un **projet non fusionné et non déployé**.

## Provenance de la méthode et non-chevauchement

Consultés : `AGENTS.md` sur `main` et le répertoire `docs/REFERENCES_CHERCHEURS_FRANCAIS_2026-11-07.md` de la PR [#159](https://github.com/Bobcribb/Bobcribb.github.io/pull/159). Les fichiers modifiés par les PR [#171](https://github.com/Bobcribb/Bobcribb.github.io/pull/171) et [#174](https://github.com/Bobcribb/Bobcribb.github.io/pull/174) ont été exclus de ce lot. La PR [#175](https://github.com/Bobcribb/Bobcribb.github.io/pull/175) modifie uniquement la bibliographie publique. Le présent lot préserve leurs travaux non fusionnés.

## Huit annotations datées proposées

| Corpus | Chemin du manuscrit | Document primaire / source indépendante examinée | Chercheur(s) français intégrés | Limite explicitée |
|---|---|---|---|---|
| Tragédie 151, *Hippolyte* | `chapitres/tragedies/volume-cli-euripide-hippolyte.md` | Euripide 769–815 ; Nicole Loraux, « La main d'Antigone », *Mètis* 1/2 (1986), [texte](https://www.persee.fr/doc/metis_1105-2201_1986_num_1_2_869) | Nicole Loraux | Mort sur scène ≠ pratiques sociales |
| Comédie 10, Cratinos | `chapitres/comedies/volume-010-cratinos-dionysalexandros.md` | *P.Oxy.* IV 663 ; Ariane Tatti (1986), DOI [10.3406/metis.1986.877](https://doi.org/10.3406/metis.1986.877) | Ariane Tatti, Frontisi-Ducroux (cadrage) | Résumé fragmentaire ≠ dialogue et datation certaine |
| Origines 494, Isis | `chapitres/origines-du-sacre/494-egypte-isis-nom-secret-ra.md` | Museo Egizio, **Cat. 1993 / CGT 54051**, recto 2.11–5.5, [notice](https://collezionepapiri.museoegizio.it/en-GB/document/185) | Grimal ; Dunand et Zivie-Coche (cadrage) | Date du manuscrit ≠ date de rédaction première |
| Origines 468, Akītu | `chapitres/origines-du-sacre/468-mesopotamie-akitu-annee.md` | ORACC [SAA 20.015, KAR 215 + PKT 16](https://oracc.museum.upenn.edu/saao/saa20/P336233), notices Marduk/Nabû | Bottéro (cadrage) | Rituels de lieux et périodes différents |
| Origines 687, Iran | `chapitres/origines-du-sacre/687-videvdad-nasu-sagdid-barasnom-cadavres-feu-eau-terre-iran.md` | *Vidēvdād* 7.2–4, 8.10–13, 9.42 ; [Boyce 1993](https://www.iranicaonline.org/articles/corpse-disposal-of-in-zoroastrianism/), [Moazami 2016](https://www.iranicaonline.org/articles/nasu-demon/) | Briant (contexte non direct) | Gloses pehlevies et rituels récents distincts de l'Avesta |
| Encyclopédie grecque 470, Bassae | `chapitres/encyclopedie/chapitre-470-apollon-epikourios-bassae-phigalie-epikouroi-frise-architecture-rituel.md` | Pausanias VIII, 41, 7–9 ; [UNESCO n° 392](https://whc.unesco.org/fr/list/392/) | — | Attribution à Iktinos = témoignage de Pausanias |
| Comparatif MC-044 | `chapitres/comparatif/volume-ccxxiii-mc-044-enfants-exposes-rois-sauves-fleuves-oracles-adoption-legitimite-sargon-moise-cyrus-persee-oedipe.md` | [CDLI P365306](https://cdli.earth/artifacts/365306), K.3401 + Sm.2118 ; Hérodote I, 107–130 | Briant (cadrage) | Analogie narrative ≠ emprunt certain |
| Philosophie, Castoriadis | `chapitres/comparatif/volume-cxl-cornelius-castoriadis-imaginaire-social-democratie-autonomie.md` | Christophe Pébarthe, *REA* 114/1 (2012), 139–157, DOI [10.3406/rea.2012.5776](https://doi.org/10.3406/rea.2012.5776) ; BnF édition 1975 | Pébarthe et Vidal-Naquet (réception) | Philosophie de l'autonomie ≠ description positive de toutes les institutions |

**Note de méthode.** Les articles Persée, les notices Museo Egizio, CDLI, UNESCO, ORACC et *Encyclopaedia Iranica* ont été consultés en ligne. Les livres de Grimal, Dunand/Zivie-Coche, Bottéro, Briant, Frontisi-Ducroux, Loraux et les éditions payantes sont ici utilisés en **bibliographie de cadrage dont les métadonnées sont contrôlées**, non présentés comme intégralement lus ; aucun passage ou avis personnel ne leur est artificiellement attribué. Les sources étrangères et les anciennes bibliographies demeurent intégralement conservées. Aucune notice de bibliothèque ne constitue un arbitrage scientifique externe de MYTHOS.

## Audit complémentaire d'une reconstitution : Bassae

Sur `main` :
- La notice `assets/reconstitutions-3d/notices/bassae-apollon-exterieur-vue.json` possède l'identifiant **R3D-008**, la datation « vers 420–400 av. J.-C. », les champs de certitude explicitant le niveau élevé pour l'architecture générale, moyen pour la toiture et faible pour peinture et détails sculptés, ainsi qu'un renvoi UNESCO.
- Un fichier photographique numérique existe à `assets/reconstitutions-3d/bassae-apollon-exterieur-vue.webp` ; sa présence dans GitHub ne démontre **pas** que l'image s'affiche dans la galerie publique.
- Le catalogue `corpus/reconstitutions-3d/catalogue.json` possède deux notices distinctes **BAS-001** (extérieur) et **BAS-002** (cella), toutes deux marquées `image_status: retirée`. Il existe donc **plusieurs régimes de catalogue**, qu'il serait abusif d'assimiler à un statut unique de publication de R3D-008 sans rapprochement technique.
- Sources externes consultées : [UNESCO bien n° 392](https://whc.unesco.org/fr/list/392/), classé en **1986**, et [Pausanias VIII, 41, 7–9](https://ftp.theoi.com/Text/Pausanias8C.html). Le recours à la tradition de Pausanias n'authentifie pas le toit, les couleurs, le paysage ou l'identité de l'architecte restitués numériquement.

**Décision conservatoire :** aucune modification des fichiers WebP, des JSON de notices, du catalogue ou de la galerie. **Statut : inspection du dépôt effectuée ; correspondance des catalogues et publication HTTPS non vérifiées.** Les droits de l'image numérique n'ont pas été revus dans ce lot.

## Anomalies et travail restant

1. **Cratinos : double traitement** de *Dionysalexandros* dans les volumes X et XXXVIII. Ne pas renuméroter, fusionner ou supprimer ; envisager des renvois historiographiques après vérification du registre canonique.
2. **Source primaire / édition critique :** plusieurs passages sont repérés par des éditions numériques et études consultées, mais leurs variantes manuscrites et le texte intégral de certaines éditions payantes restent non collationnés. Aucun DOI ne doit être fabriqué pour des ouvrages qui n'en possèdent pas.
3. **Modèle Bassae :** distinguer notice R3D-008 et entrées historiques BAS-001/BAS-002, vérifier l'affichage des images publiées par un contrôle HTTPS distinct.
4. **Intégration :** une PR brouillon ne signifie ni fusion, ni déploiement, ni validation universitaire externe. Les tests Actions, comparaison complète de la PR et l'état de `main` doivent être contrôlés après création.

**États de travail :** huit chapitres **annotés en PR** ; reconstitution Bassae **auditée en lecture seule**, diffusion **non vérifiée**. Aucune tâche planifiée n'a été modifiée.
