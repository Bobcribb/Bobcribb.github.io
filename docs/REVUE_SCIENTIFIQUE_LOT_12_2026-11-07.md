# MYTHOS — Registre scientifique de révision, lot 12

**Date :** 7 novembre 2026. **Issue :** https://github.com/Bobcribb/Bobcribb.github.io/issues/158.
**Branche indépendante :** scientifique/revue-lot12-20261107-sources-rigueur. **Base main :** efd9e69c7158b80929f980e2a1d74ccbff6203e7. **État éditorial :** annoté en PR brouillon ; non fusionné ; aucune publication publique affirmée.

## Sélection sans doublon
PR 159, 171, 174, 178, 180, 183, 186, 190, 194, 204, 205 et 217 consultées ; le **lot 11** existe déjà en PR 217. Les PR 204 et 205 portent sur les mêmes huit manuscrits du lot 10 et doivent être réconciliées **séparément**, sans modification ici.

1. **Tragédies — Iphigénie à Aulis (CLXI)** — `chapitres/tragedies/volume-clxi-euripide-iphigenie-a-aulis.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.
2. **Comédies — Eupolis, Kolakes (XVI)** — `chapitres/comedies/volume-016-eupolis-kolakes.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.
3. **Égypte — cachette royale TT320 / DB320 (633)** — `chapitres/origines-du-sacre/633-tt320-cache-royale-deir-el-bahari-reinhumation-momies-coffins.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.
4. **Mésopotamie — prophétesses de Mari (603)** — `chapitres/origines-du-sacre/603-voix-feminines-prophetesses-mari-delphes-houlda.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.
5. **Iran / mythologie comparée — MC-095, échelles célestes** — `chapitres/comparatif/volume-cclxxxix-mc-095-echelles-ciel-terre-egypte-jacob-mithra-sankassa-platon.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.
6. **Mythologie comparée — MC-115, roues et chars solaires** — `chapitres/comparatif/volume-cccxxiii-mc-115-roues-sacre-chars-solaires-cycles-temps-souverainete-revelation.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.
7. **Encyclopédie grecque — Triptolème, Eumolpos et Éleusis (331)** — `chapitres/encyclopedie/chapitre-331-triptoleme-eumolpos-eleusis.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.
8. **Philosophie — George Herbert Mead (CXXVI)** — `chapitres/comparatif/volume-cxxvi-george-herbert-mead-geste-soi-autrui-generalise-philosophie-sociale.md` ; annexe datée : témoins, références académiques et françaises, données exactes et limites de collation.

## Méthode
- Les notes distinguent documents primaires consultés, notices de musée ou d'éditeur, articles disponibles en résumé, éditions critiques non intégralement collationnées et interprétations modernes. La notice d'un établissement ne signifie jamais que MYTHOS a été expertisé ou approuvé.
- Conservation stricte des manuscrits : vérification avant commit que chacun des **huit contenus de base** constitue le préfixe intégral du fichier enrichi ; seuls des appendices datés sont ajoutés. Aucun nouveau numéro, renumérotation, perte de texte, image remplacée ni édition de tâches existantes.
- Contributions françaises conservées lorsque pertinentes : Nicole Loraux, Pierre Vidal-Naquet, Michel Dewachter, Dominique Charpin, Pierre Briant, Jean-Pierre Vernant, Daniel Cefaï, Louis Quéré et Pierre Tripier. Les sources étrangères sont également citées et conservées.

## Audit archéologique en lecture seule — Rhamnonte
- Reconstitution **RHA-NEM-001**, sanctuaire de **Némésis et Thémis** à Rhamnonte, vue interprétative vers **420–400 av. J.-C.**. Catalogue : `assets/reconstitutions-3d/catalogue-photorealiste.json` (**94** entrées lues). Image : `/assets/reconstitutions-3d/rhamnonte-nemesis-themis-sanctuaire-panorama.webp`; notice : `/assets/reconstitutions-3d/notices/rhamnonte-nemesis-themis-sanctuaire-panorama.json`.
- SHA-256 **déclaré dans le catalogue, non recalculé** sur le binaire : `39450b0d17260e59b83ff6bd30dca13afb5fb8e1084b3ec73169fa03f9374270`. Existence dans le catalogue vérifiée ; intégrité binaire, lecture de la totalité du WebP et affichage HTTPS **non vérifiés**.
- Site officiel : Hellenic Heritage, https://www.hh.gr/en/destinations/rhamnous/ ; existence de deux sanctuaires et vue sur le golfe d'Eubée. Prudence : ses indications sculpturales ne distinguent pas correctement toutes les attributions.
- **Distinction épigraphique :** inscription **IG II³ 4, 513**, dédicace à Thémis, attribution signée à **Chairéstratos**, statue habituellement identifiée à Thémis, **Athènes NM 231**, édition et traduction https://www.atticinscriptions.com/inscription/DNO/2372. **Némésis** est associée à **Agoracritos** (copie au Louvre **Ma 2219**, https://collections.louvre.fr/ark:/53355/cl010276168 ; original et base discutés dans Basile Petrakos, « La base de la Némésis d'Agoracrite », *BCH* **105/1 (1981)**, p. **227–253**, DOI **10.3406/bch.1981.1938**, https://www.persee.fr/doc/bch_0007-4217_1981_num_105_1_1938).
- Les inscriptions et les copies anciennes documentent les sculpteurs et des formes iconographiques, mais **pas** la totalité des toitures, décors latéraux ou couleurs de la reconstitution. Les identifications sculpturales méritent une correction **dans un lot ultérieur dédié**, après collation ; rien n'a été modifié dans la notice ni l'image ici.

## Contrôles restant ouverts
- Collation de l'ensemble du chapitre Kovacs et d'une édition grecque de *Iphigénie à Aulis* ; variantes de la pièce ; PCG et transmetteurs d'Eupolis ; inventaires individuels et étiquettes de TT320 ; ARM 26 204 original et contexte ; traductions et variantes d'Origène ; objets de Trundholm, Éleusis et Rhamnonte.
- Vérifier les tests de génération, l'audit intégral GitHub Actions, les liens et le rendu du lecteur. Aucune fusion ni vérification publique post-déploiement n'a été demandée.

**Aucune PR antérieure, aucun workflow, numéro, UUID, reçu, image, catalogue, tâche ni horaire modifié.**
