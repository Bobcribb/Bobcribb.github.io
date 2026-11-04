# MYTHOS — Refonte : titres de monographies, galerie 3D et suivi de publication

**Contrôle : 4 novembre 2026, vers 17 h UTC.** Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`. Règles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relues avant toute écriture. Photographie initiale de `main` : `7238a5cd6c438e0fdd5ac992abd472a887ac1249`.

## Corpus intégral et décisions éditoriales

Inventaire de la dernière photographie de `main` disponible pendant ce contrôle : **232 demandes conservées** dans `editorial/inbox/`, **223 reçus d'attribution** dans `editorial/numbering.json`, **5 retenues explicites** dans `editorial/holds.json`, donc **4 demandes complètes en file sans reçu**. Ces nombres sont un instantané mobile : d'autres chantiers peuvent soumettre des textes simultanément.

Demandes intégrales nouvelles **déjà soumises par d'autres chantiers et non resoumises ici** :
- `72b851ce-ec51-4ae7-8101-bc4851e3f051`, `comparatif`, MC-051, oracles et décisions de Deir el-Médina à Dodone ; **97 839 caractères Markdown** ;
- `e7c2e458-6c43-4b71-96b5-d72ca83df409`, `comedies`, Nicocharès, *Agamemnon*, Cassandre et paratragédie ; **49 803 caractères** ;
- `7edc91a6-6980-4a18-9426-3f9c6eb71c52`, `comparatif`, MC-052, rites de substitution et expulsion du mal ; **101 271 caractères** ;
- `f6a1e3d8-4b2c-4fc5-86c9-0d8e5a783bf1`, `encyclopedie`, Télésphore, guérison et Pergame ; **49 430 caractères**.

Ces quatre demandes portent leurs propres UUID, collections et variables `{{numero}}` / `{{volume}}`. Les cinq autres demandes sans reçu sont **bloquées intentionnellement** pour collisions documentées. Elles ne doivent pas être attribuées à la main. Les manuscrits historiques Chiron 118–133 et Nyx–Hypnos 218–224 ne sont toujours pas identifiés comme textes intégraux approuvés dans les emplacements consultés. Les archives parallèles, les brouillons privés et les études déjà publiées ne sont pas de nouveaux chapitres.

**Nouvelle étude déposée ou attribuée par cette exécution : zéro.** Déposer à nouveau l'un de ces quatre manuscrits ferait un doublon. Aucun résumé de remplacement ni texte fictif n'a été créé. Les fichiers `chapitres/` et les registres de numérotation n'ont pas été modifiés par cette intervention.

## Corrections concrètes

1. **Titres universitaires** : `scripts/recent_studies.py` extrait désormais le titre complet depuis le H1 pour les chapitres encyclopédiques (p. ex. « Chapitre 409 — Agathos Daimôn : le Bon Génie, le serpent protecteur et Alexandrie »), et conserve le H2 du sujet pour les autres collections. L'ancien rendu erroné affichait seulement « 1. Sources et méthode ». `tests/test_recent_studies.py` verrouille cette distinction et la conservation de la cote et de la navigation.
2. **Mise en valeur illustrée** : `assets/mythos-museum.css` donne aux cinq cartes des études attribuées de véritables images pleine largeur avec légende, au lieu de miniatures 90 × 113 px héritées des cartes compactes ; mise en page flexible, bordures et lisibilité noir/ivoire/or, variantes mobiles et impression.
3. **Galerie 3D réellement accessible** : `index.html` comporte désormais dans « Les collections » une carte illustrée unique `/reconstitutions-photorealistes.html` avec `/assets/reconstitutions-3d/delphes-apollon-panorama.webp`, son caractère interprétatif et une mention des degrés de certitude ; `scripts/build_navigation.py` référence le même parcours parmi les principaux dossiers générés. `scripts/apply_museum_design.py` restaure la carte après refonte lorsqu'une section `#home-collections` est présente, sans duplication ; `tests/test_museum_navigation.py` vérifie l'idempotence. Les autres cartes, bibliographies et textes sont préservés.

## Commits de cette intervention

- `e5182b0517d109cf53105b8b2eda72fb7f292f67` : première tentative du correctif des titres, **remplacée immédiatement** par la restauration fiable `9923ed4adb7ba5fc24747179377349456c7317d1`. Ne pas utiliser la version intermédiaire ;
- `e7e96aaf3f078a5be06d84f807d03a6131acff62` : test des titres, corrigé pour la bonne écriture des retours de ligne en `9ae03051fe13942fc0d744b081cb013c9c0c945d` ;
- `d99ed1e82bce16a65e7ef0115b10a2270d48e06c` : styles des cartes récentes ;
- `01806ba28a9d022f4cc5cfcb5dd5999219c220f0` : carte 3D illustrée dans l'accueil du dépôt ;
- `1323b3512c936a0e4cb727ab86caeb927d54304a` : carte galerie dans le constructeur du portail ;
- `a8e2b233e9b58980944d0d02ca8d308a970e95d2` : conservation de la carte après passe musée ;
- `27c9508e7f1863f10983fb415bf3f45427eb8af4` : test de reconstruction idempotente.

## Vérifications et blocages

Sur une exécution de validation antérieure, **les 179 tests se terminaient avec deux échecs** : l'absence de la carte 3D (corrigée ci-dessus) et l'incohérence préexistante du journal `docs/MYTHOS_ICONOGRAPHIE_ALTERNANCE.json` (la `latest_session` diffère de `history[-1]` et une paire historique initiale ne respecte pas l'alternance). Cet état relève du suivi de l'autre chantier iconographique : aucune tâche, aucune cadence et aucun état historique de son automatisation ne sont modifiés ici.

La validation des derniers commits et leur déploiement doivent être confirmés par GitHub Actions. Le site HTTPS `bobmythos.fr` et son document `/catalog/publication-verification.json` n'étaient pas accessibles depuis le contrôle HTTP externe ; **aucune preuve de mise en production de ces corrections n'est donc annoncée**. Contrôles de sortie : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, puis vérification de la nouvelle carte et du titre du chapitre 409 sur le domaine public.

Aucune étude universitaire, archive, image 2,5D bannie, numérotation, commande de planification, autre automatisation ni workflow n'a été modifié.
