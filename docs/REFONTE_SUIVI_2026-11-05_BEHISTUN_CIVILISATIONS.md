# MYTHOS — Renvoi scientifique CIV-01 et contrôle des publications

Date du contrôle : 5 novembre 2026.
Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`.
Parent GitHub de cette modification : `8987a06baea2796944f320269d2347dd66a8c322`.

## Contenu universitaire intégral

Monographie identifiée : `corpus/civilisations/perse-iran-ancien-behistun.html` (cote documentaire existante CIV · 01). Son texte public de plus de 30 000 caractères était déjà conservé en HTML, avec étude critique de l'inscription DB, bibliographie, sources, iconographie créditée et exercices universitaires. Le document était accessible sur `https://bobmythos.fr/corpus/civilisations/perse-iran-ancien-behistun.html` avant cette intervention. Il ne serait donc **pas exact de le compter comme première publication nouvelle**.

Cette intervention rend le texte intégral directement découvrable depuis `/civilisations/`, au moyen d'une carte illustrée ; elle répare le fil d'Ariane obsolète et ajoute un retour vers la carte du portail. La matière scientifique de l'article n'est ni réécrite, ni résumée, ni amputée. Le générateur du portail conserve cette navigation lors des reconstructions.

Photo documentaire : relief de Behistun ; Mahdimanavimvi, 2018, CC BY-SA 4.0, avec liens de provenance et de licence déjà conservés dans la monographie.

## Recherche de nouveaux textes autonomes

Au moment de l'inventaire, 417 soumissions figuraient dans `editorial/inbox`, 384 reçus étaient inscrits dans `editorial/numbering.json`, et 16 demandes en collision étaient explicitement conservées dans `editorial/holds.json`. Parmi les 17 noms de fichiers non attribués et non retenus, un nom non conforme au format UUID est déjà signalé par le protocole. Les seize autres sont des manuscrits intégraux publics, **déjà soumis** et en attente du traitement transactionnel par GitHub Actions. Ne pas les recréer ni leur attribuer de numéro à la main.

La collision historique MC-077 a bloqué plusieurs builds antérieurs ; le second texte distinct a été resoumis sous MC-078, sans toucher à l'original en attente. Les workflows récents doivent être revérifiés avant toute annonce de première publication. Les anciennes archives WordPress privées du Drive ne sont pas des manuscrits publics approuvés transférables sans nouvelle vérification de leur statut.

**Nouvelles premières publications universitaires confirmées par cette intervention : 0.** Aucun texte intégral inédit approuvé et absent du circuit de publication n'a été identifié.

## Modifications contrôlables

- `scripts/build_navigation.py` : section CIV-01 avec photo et lien vers le dossier complet.
- `civilisations/index.html` : carte visible avant régénération.
- `corpus/civilisations/perse-iran-ancien-behistun.html` : fil d'Ariane et navigation retour, sans changement du corps scientifique.
- `assets/mythos-museum.css` : largeur de carte responsive et focus clavier visible.
- `tests/test_civilisations_behistun_access_20261105.py` : vérification des sources, crédits, sections, liens réciproques et mise en page.

La bannière noire et or, les images archéologiques et la galerie photoréaliste ne sont pas remplacées. Aucun numéro, reçu, autre manuscrit ni planification automatique n'est modifié.

## Limite de déploiement

Au contrôle HTTPS préalable, `/catalog/publication-verification.json` indiquait encore `source_commit=c46ff854a9c173783ac0801b62fea22aed44750f`, `indexed_documents=1509`, `verified_archives=27` et `verified_media=110`. Il faut contrôler le succès d'une publication GitHub Actions puis relire le manifeste pour qualifier la nouvelle carte de déployée publiquement.
