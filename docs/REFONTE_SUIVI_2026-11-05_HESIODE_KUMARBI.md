# MYTHOS — Refonte : Hésiode, Kumarbi et généalogies divines

**Date :** 5 novembre 2026. Dépôt : `Bobcribb/Bobcribb.github.io`, `main`.

## Sources et statut éditorial

`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relus. Inventaire vérifié : 336 demandes `editorial/inbox/`, 331 reçus d'attribution (72 Origines, 75 Encyclopédie, 48 Comédies, 48 Tragédies, 88 Comparatif) et cinq retenues explicites. Le manuscrit archivistique `Konnos` est déjà couvert par deux études publiées (volumes 68–69) ; il n'est pas une étude antique inédite à republier. Aucun autre manuscrit universitaire intégral **nouveau et autorisé pour publication** n'a été établi dans les sources examinées. Aucun UUID, compteur ni numéro n'est créé ; les anciens brouillons WordPress privés ne sont pas importés.

## Rattachement de deux textes complets, déjà publiés dans Civilisations et Comparatif

- `/bibliotheque-mythologies-du-monde/civilisations-hourrites-mittani-kumarbi/` : **Hourrites et Mittani : diplomatie d'Amarna, tablettes et Kumarbi**, 29 950 caractères HTML, bibliographies et sections universitaires. SHA source initial : `2d3c7312bfb5ce2e69614806f319d92252844e26`. Rattachement : Sources anciennes → Hourrites.
- `/bibliotheque-mythologies-du-monde/mythos-comparatif-souverainete-cosmique-kumarbi-hesiode-pergame/` : **Souveraineté cosmique, Kumarbi, Hésiode et Pergame**, 18 089 caractères HTML, onze sections et bibliographie. SHA initial : `7654397ed568aad0b7ba1f3466a1145dcfe21b50`. Rattachement : Interprétations philosophiques → Kumarbi et Hésiode.
- Parcours associé avec **Hésiode : organiser les dieux, penser la condition humaine**, `/livre-hesiode/`, 48 568 caractères HTML, SHA source initial `f602ea26fa146139917b9f453daab551d672411e`, conservé sous Cosmogonies.

Aucun de ces trois textes n'est déplacé, abrégé, numéroté ou copié. **Deux nouveaux liens dans le catalogue grec ne sont pas deux premières publications.** Les rapprochements distinguent la chronologie, la tradition littéraire et les hypothèses comparatives sans inventer une filiation.

## Fonctionnalités et vérifications ajoutées

- `scripts/build_greek_corpus.py` : les deux textes déjà publics rejoignent les lectures associées du sommaire grec.
- `scripts/build_greek_folders.py` : deux classements primaires supplémentaires, des retours vers les sous-dossiers et un panneau de **six liens réciproques** entre trois pages, hors des articles ; une deuxième génération ne répète pas ces panneaux.
- `assets/mythos-museum.css` : panneau ivoire/or sur fond anthracite, accent doré, retours à la ligne, disposition mobile sous 480 px.
- `tests/test_greek_cosmic_genealogies_20261105.py` : intégrité des sources publiques, classement, ancres, trois panneaux non dupliqués, deux reconstructions et préservation des articles.

La bannière statue grecque/temple, les huit dossiers illustrés, les archives et le circuit de publication concurrent sont préservés. Les tests GitHub Actions et le reçu HTTPS `/catalog/publication-verification.json` doivent encore confirmer le rendu et le déploiement ; aucune publication nouvelle n'est annoncée sur cette seule base. Les planifications MYTHOS ne sont pas modifiées.
