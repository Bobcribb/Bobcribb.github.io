# MYTHOS — Corrections techniques issues de l'audit du 5 novembre 2026

## Périmètre
- Correction du choix du titre des cartes de l'accueil pour les manuscrits comportant deux H1 : un premier H1 générique de série suivi du véritable H1 scientifique, avant les H2 numérotés.
- Complément de **15 notices JSON individuelles** pour les 15 reconstitutions déjà présentes dans le catalogue central, sans changer les 54 WebP ni leurs notices scientifiques existantes.
- Aucun manuscrit universitaire, numéro canonique, reçu, UUID, retenue, URL historique, automatisation horaire ou contenu original modifié.

## Distinctions documentaires
Les quinze nouvelles notices reflètent exactement les champs existants du catalogue photoréaliste. Leur lien documentaire ne certifie pas les choix iconographiques, les éléments conjecturaux ni une précision métrique. Les notices plus riches déjà existantes demeurent inchangées.

## Vérifications attendues
1. Test de non-régression `tests/test_recent_studies.py` : la carte Ménècrate affiche le titre intégral et la source Markdown reste identique.
2. Contrôle qu'une notice JSON individuelle existe pour chaque image déclarée dans `catalogue-photorealiste.json` et conserve son identifiant, son slug, sa légende et son chemin WebP.
3. Vérification de GitHub Actions et, après tout déploiement, consultation HTTPS effective de l'accueil et de la galerie.
