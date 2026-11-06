# MYTHOS — Raccordement du sommaire 3D à Métaponte (6 novembre 2026)

Source `main` examinée : `dc7038a2f8258b762adc39afc64f81da833d9ff0`.

L'audit GitHub Actions 42283656241 a également révélé un blocage de collision historique MC-110, sans rapport avec cette galerie. Le registre `editorial/holds.json` comporte désormais la demande 8d8ea771-7635-4d19-b3e9-fc06110a2b44 en attente ; ni ce registre ni les manuscrits ne sont modifiés ici.

## Anomalie vérifiée

Le fichier existant `reconstitutions-photorealistes.html` contient une cible réelle `id="lecture-section-76"` pour l'étude de Métaponte, mais conserve dans son sommaire un lien littéral `href="#lecture-section-{LECTURE_INDEX}"`, ce qui rend impossible la navigation vers la section et fait échouer `tests/test_iconography_audit_paths_20261104.py`.

## Correctif minimal

Remplacement **exclusif** du `href` non résolu par `#lecture-section-76` à son emplacement historique, sans modifier le contenu scientifique, l'ordre des 82 reconstitutions, leurs images WebP ou leurs notices. Le test `tests/test_gallery_toc_anchor_20261106.py` vérifie le respect de toutes les ancres du sommaire et le lien explicite Métaponte.

Les séries numérotées, les registres transactionnels, les workflows, la charte noir et or et les autres automatisations MYTHOS demeurent inchangés.

## Validation de publication

Une présence dans GitHub et des tests réussis ne prouvent pas que le domaine HTTPS est à jour. La confirmation exige une exécution de publication réussie, puis l'empreinte du manifeste `/catalog/publication-verification.json` et la disponibilité du lien Métaponte sur `https://bobmythos.fr/reconstitutions-photorealistes.html`.
