# MYTHOS — Refonte du portail Origines du sacré : images sourcées et concordance des études canoniques

**Intervention : 6 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`, site `https://bobmythos.fr`.

## 1. Garde de publication et statut des manuscrits

Lecture préalable de `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md` et `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md`. Départ : `main` au commit `17ae135cffe29494ab62da90c0f8585186015b9c`. Cette intervention n'attribue **aucun nouveau numéro**, ne crée **aucun nouveau manuscrit canonique**, ne modifie aucun reçu ou registre de publication et ne publie aucun brouillon privé.

**Premières publications universitaires : zéro (0).** Les sources universitaires retrouvées dans les archives grecques, les livres, les séries numérotées et les publications philosophiques étaient déjà déposées en entier et accessibles depuis GitHub ; leur duplication aurait créé de fausses premières publications. La recherche ciblée dans Google Drive a retrouvé principalement des volumes de sauvegarde historiquement désignés comme *brouillons WordPress privés* et des versions d'œuvres déjà publiées. Leur présence ne constitue ni une validation de diffusion ni une preuve d'absence dans le corpus public. **Blocage éditorial précis : aucun manuscrit intégral supplémentaire, autorisé pour publication publique et établi comme réellement absent, n'a pu être identifié avec certitude.** Reprendre l'analyse individuelle de ces documents privés exige une confirmation explicite de leur statut éditorial ; ne pas les verser automatiquement dans `editorial/inbox/`.

Les demandes `editorial/inbox/` déjà persistées et les manuscrits en retenue demeurent sous la responsabilité de GitHub Actions et de la réconciliation canonique, sans resoumission ni nouvel UUID ici.

## 2. Quatre études déjà numérotées et conservées : accès croisés nouvellement ajoutés

Les fichiers Markdown d'origine, leur bibliographie et les lecteurs HTML sont présents dans le dépôt ; aucune citation, ligne ou page n'a été résumée ou modifiée. Les numéros ci-dessous **sont des numéros historiques existants**, jamais des attributions de cette intervention.

| Numéro canonique | Titre / sujet | Markdown original | Lecteur intégral |
| --- | --- | --- | --- |
| 499 | Grèce : consécration et sanctuaires | `chapitres/origines-du-sacre/499-grece-consecration-dedicace-sanctuaires.md` | `/chapitres/origines-du-sacre/499-grece-consecration-dedicace-sanctuaires/` |
| 500 | Mésopotamie : Gudéa et fondation de l'E-ninnu | `chapitres/origines-du-sacre/500-mesopotamie-fondation-temples-gudea.md` | `/chapitres/origines-du-sacre/500-mesopotamie-fondation-temples-gudea/` |
| 501 | Égypte : Séchat et étirement du cordeau | `chapitres/origines-du-sacre/501-egypte-fondation-cordeau-seshat.md` | `/chapitres/origines-du-sacre/501-egypte-fondation-cordeau-seshat/` |
| 502 | Inde : `pratiṣṭhā` et installation des images | `chapitres/origines-du-sacre/502-inde-pratistha-images-temples.md` | `/chapitres/origines-du-sacre/502-inde-pratistha-images-temples/` |

Une nouvelle rubrique `#origines-etudes-fondations` est ajoutée par le générateur au sommaire `/origines-du-sacre/#origines-archives-documentaires`. Chaque lien mène au **lecteur intégral déjà publié**. Les liens sont strictement distingués des cotes d'archives ODS-CONV et ODS-S28 ; aucun double emploi de numéro.

## 3. Cinq documents matériels réellement sourcés, sans images de remplissage

La galerie des **neuf archives historiques XXV–XXXIII** est désormais enrichie de cinq illustrations précisément documentées dans `scripts/editorial_media.json`, avec `alt`, provenance, datation lorsque attestée, licence et commentaire de portée scientifique, sous un panneau de crédit explicite.

| Tome / cote | Illustration documentée | Limite d'interprétation |
| --- | --- | --- |
| XXV / ODS-CONV-XXV | Temple d'Apollon à Delphes, photographie Bernard Gagnon | Exemple de sanctuaire grec et non modèle universel |
| XXVI / ODS-CONV-XXVI | Plan moderne de l'aire sacrée de Délos, incluant le lac sacré | Plan topographique, non représentation de rite |
| XXXI / ODS-CONV-XXXI | Statue d'Artémis Éphésienne au musée d'Éphèse | Iconographie cultuelle dont certains motifs restent discutés |
| XXXII / ODS-CONV-XXXII | Rondelles hellénistiques de terre cuite ornées de masques théâtraux, Met | **Ne documente pas** une cérémonie de possession |
| XXXIII / ODS-CONV-XXXIII | Disque votif d'Enheduanna, Penn Museum | **N'est pas** un manuscrit autographe de ses hymnes |

Les quatre autres tomes restent sans photographie faute d'attribution iconographique suffisamment pertinente. Aucun schéma 2,5D, illustration fantaisiste, menu incrusté dans une image ou image non sourcée n'est ajouté.

## 4. Modifications enregistrées sur `main`

- `scripts/origins_archival_concordance.py` : construit des crédits accessibles sous chaque carte illustrative et vérifie l'existence des lecteurs canoniques ; refuse les fichiers manquants et les notices de média incomplètes.
- `scripts/origins_archive_navigation.py` : appelle l'enrichissement à partir de son sommaire de neuf archives existantes. Les neuf renvois réciproques vers l'archive, les Markdown et la composition scientifique ne changent pas.
- `assets/mythos-museum.css` : fond anthracite, typographie ivoire/or, visuels adaptatifs, focus clavier, grille de lectures comparées en deux colonnes et une seule colonne mobile.
- `tests/test_origins_archival_concordance_20261106.py` : contrôle les références d'images réelles, les quatre manuscrits déjà numérotés, les neuf URL uniques, la séparation des crédits, l'absence de copie ou tronçonnage des textes, et l'arrêt si lecteur ou média manque.

Commits de cette intervention (avant le présent rapport) :
- `50d16eb15cd243ff82e0cceaac2c04c544580988` — module de concordance ;
- `d1f6147c8f94a7d007c6fa96fe7af7282f1ab58f` — raccordement du générateur ;
- `54b31a559745de66acbfab48529e32f9809bc19e` — mise en page responsive ;
- `d289b1bd13fe8a5451502384ba3e2f5e923758ba` — tests ;
- `afdd8ce94ec626fd9906081a66d06f7af156bd13` — unicité des liens de tests.

## 5. Contrôles vérifiés et publication effective

**Constat HTTPS positif pour l'intervention précédente :** `https://bobmythos.fr/origines-du-sacre/` expose déjà les **neuf liens directs historiques XXV–XXXIII**. Le manifeste `https://bobmythos.fr/catalog/publication-verification.json` renvoyait au contrôle `source_commit=fabb3cd46c62a177bb0541b23015339a60ebcc1e`, `github_run_id=42153925962`, `indexed_documents=1584`, `verified_archives=27`, `verified_media=110`.

**Nouveautés de ce rapport :** les cinq images et les quatre liens canoniques ont été enregistrés dans la branche `main`, **mais leur présence en HTTPS n'était pas encore confirmée** au contrôle. La validation du commit `afdd8ce` (Actions `42158262823`) était encore en génération au dernier état consulté ; la publication de `54b31a` (`42158090264`) a été annulée par une publication concurrente, sans démontrer un défaut dans son code. D'autres actions horaires sont actives : ne pas annoncer leur résultat anticipé.

À confirmer après une publication GitHub Actions réussie postérieure aux commits ci-dessus : `source_commit` public, neuf cartes, cinq images et crédits, quatre liens `#origines-etudes-fondations`, contenu intégral des lecteurs, absence de doublon, navigation mobile. Le résultat du workflow doit primer sur le simple état de la branche.

**Préservation :** aucune source, archive, PDF, page universitaire d'origine, numéro éditorial, fichier de file, registre, workflow ou planification horaire MYTHOS n'a été modifié par cette séance.
