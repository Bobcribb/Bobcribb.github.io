# MYTHOS — Refonte : accès réciproque à l'édition historique ODS I–XXVII

**Séance du 6 novembre 2026, 04 h 49 (France).** Dépôt `Bobcribb/Bobcribb.github.io`, branche `main` examinée avant intervention. Instructions `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relues ; aucun numéro attribué manuellement.

## 1. Contenus et contrôle de doublons

- L'édition universitaire historique `corpus/origines-du-sacre/edition-integrale-tomes-I-XXVII.html`, 1 852 364 octets recensés dans l'arbre Git, existe déjà et figure dans `sommaire-general.html` ; elle n'était pas liée directement depuis `origines-du-sacre/index.html`. Il s'agit donc d'un **rattachement de corpus déjà hébergé**, et non d'une première publication. Son origine HTML est conservée.
- Les neuf tomes historiques XXV–XXXIII ont déjà un sommaire dédié ; cette intervention ne les duplique pas, ne les renumérote pas et maintient leurs neuf cartes.
- La file `editorial/inbox/` et les reçus de `editorial/numbering.json` appartiennent au circuit automatique. Aucun manuscrit supplémentaire distinct, public, intégral, approuvé et absent du dépôt n'a été confirmé lors de ce contrôle ; les anciens brouillons WordPress du Drive restent privés selon `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md`.
- **Nouvelles premières publications : 0.** **Corpus historique intégral rattaché à son portail : 1 (27 tomes dans un lecteur).**

## 2. Changements logiciels

- `scripts/origins_integral_reader.py` : vérifie source et rendu, longueur du texte, présence d'appareil documentaire et continuité du début et de la fin ; produit une carte d'accès direct et ajoute un lien retour au rendu public uniquement. La comparaison du texte de l'article avant et après insertion est obligatoire et le traitement est idempotent.
- `scripts/origins_archive_navigation.py` : rattache cette vérification au générateur déjà utilisé pour le portail des Origines du sacré, sans modifier ses neuf archives ni la numérotation.
- `assets/mythos-museum.css` : une carte documentaire illustrée à deux colonnes sur écran large et une colonne sur téléphone, contrastes ivoire/or, cadre anthracite, focus clavier et préférence de mouvement réduit. L'image d'Ounas est explicitement présentée comme un exemple égyptien, non comme l'iconographie de tout le corpus.
- `tests/test_origins_integral_reader_20261106.py` : vérifie l'unicité du lien et du retour après deux passages, la conservation exacte du texte universitaire, l'absence de lien quand les deux fichiers manquent et le refus d'un lecteur tronqué.

## 3. Vérifications et réserve de déploiement

Le fichier intégral reste à son chemin et à son identifiant historique. Aucun PDF, chapitre scientifique, numéro canonique, reçu, workflow GitHub, archive ou automatisation horaire n'est modifié.

La présence de la nouvelle carte dans le rendu `_site` doit être confirmée par les tests GitHub Actions et par le `source_commit` du manifeste public `/catalog/publication-verification.json`. Un commit GitHub ou une PR fusionnée ne valent pas confirmation HTTPS ; tant que ces contrôles ne sont pas réussis, **ne pas annoncer la nouvelle navigation comme déployée**.
