# MYTHOS — Refonte du 4 novembre 2026 : accès automatique aux études universitaires attribuées

**Contrôle : 4 novembre 2026, vers 16 h 00 UTC.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`. La garde éditoriale `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` a été lue sur la branche réelle avant toute intervention. Photo initiale de `main` : `0b656b645e5c7d43d4da9142df45914fa138b52a`.

## 1. Recherche d'études universitaires intégrales

L'inventaire de la file `editorial/inbox/` et du registre `editorial/numbering.json` a révélé **215 demandes**, dont **209 attributions enregistrées** dans les cinq collections (Origines 38 ; Encyclopédie 46 ; Comédies 27 ; Tragédies 29 ; Comparatif 69), **5 demandes en attente explicite** dans `editorial/holds.json`, et **1 demande valide apparemment non encore attribuée** au point de contrôle.

Cette dernière demande, **UUID `c3fb9c0e-4af8-4aa1-9edf-d43d508ab049`**, porte sur **MC-049, « Faire vivre l'image divine »** (`comparatif` ; environ **72 219 caractères Markdown**). Elle est **déjà déposée** sous `editorial/inbox/` par un autre chantier. **Ni un nouveau UUID, ni une deuxième soumission, ni un numéro manuel ne sont créés** : GitHub Actions doit produire le reçu et le lecteur après contrôle concurrent de `main`. Aucune attribution ou publication de cette demande n'est annoncée ici.

Les archives du dépôt historique `Bobcribb/Mythos`, le registre de récupération grec et les précédents audits n'ont pas livré de manuscrit complet approuvé inédit pour Chiron 118–133 et les anciens chapitres Nyx–Hypnos 218–224. Sur le Google Drive connecté, les volumes `MYTHOS — Brouillons sauvegardés` restent expressément des archives privées ; les exemplaires de `L'Horizon d'Aton` sont déjà publiés. Rien de ces sources n'a été versé au dépôt public ni substitué par un résumé.

**Nouvelle étude intégrale intégrée par cette exécution : aucune.** L'inédit complet disponible de MC-049 est déjà dans le circuit de publication ; le publier autrement contournerait la règle de numérotation concurrente. Les 209 études attribuées ne doivent pas être dupliquées.

## 2. Modification effective de la navigation et de la présentation

Un nouveau générateur `scripts/recent_studies.py` sélectionne, pour **chacune des cinq collections numérotées**, le dernier **numéro réellement attribué** dans les reçus, et vérifie **à la fois** le fichier universitaire intégral Markdown et son lecteur HTML produit. Ni les dossiers non reçus, ni les textes trop courts, ni les lecteurs absents n'obtiennent de carte publique.

Le générateur complète `index.html` de **cinq cartes illustrées** (si les cinq études sont effectivement rendues), sous « Dernières études par collection », et d'un **renvoi direct dans le sommaire centré**. Cette section prend place entre les parcours guidés et les trois œuvres philosophiques déjà présentées.

Au contrôle, les dernières attributions utilisables sont :

- **Origines du sacré, chapitre 636** : Psousennès Ier et Tanis.
- **Encyclopédie, chapitre 403** : Ennodia, Thessalie et cultes.
- **Comédies, volume LXXXVI (86)** : Archippos, `Hēraklēs gamōn`.
- **Tragédies, volume CCXXX (230)** : Sophocle, `Triptolème`.
- **Comparatif, volume CCXXVIII (228)** : chorégie et financement du rire démocratique.

Les cartes utilisent des **photographies et reproductions déjà archivées dans `media/manifest.json`**. Le code ne modifie ni les manuscrits sources, ni les bibliographies, ni les archives, ni les références institutionnelles, ni les numéros. Il réutilise les classes `portal-grid` et `portal-card`, déjà adaptées aux écrans larges, tablettes et téléphones, et le style noir, ivoire et or avec bannière grecque. Aucune image 2,5D n'est réintroduite.

## 3. Commits

- `6c7f8e33c93c7d24257f0a356b85e7917b63bff4` : nouveau générateur de cartes des études attribuées.
- `7242a6d8297d7272a864a03036a73b893267227a` : appel en fin de génération du site, après les outils de lecture, sans réécrire les études.
- `68fe688b171fa1377ce7a20b3e1d19f56aab8b5b` : tests de non-duplication, d'idempotence, de conservation et du filtrage des demandes non attribuées.

Aucun changement de `editorial/numbering.json`, `EDITORIAL_NUMBERING.json`, `editorial/holds.json`, `.github/workflows/` ou des automatisations MYTHOS.

## 4. Contrôles et statut public

Vérification locale avec un jeu de données synthétique : compilation Python du module, sélection d'un manuscrit intégral reçu, création de la carte et de son renvoi, répétition sans doublon, conservation du texte existant et de la bibliographie. Les tests automatisés sont enregistrés dans `tests/test_recent_studies.py` ; leur exécution complète dans GitHub Actions doit être vérifiée.

Le contrôle **HTTPS réel** de `https://bobmythos.fr/catalog/publication-verification.json` a répondu avec `source_commit=05c68a64605501f7dc90889fbd74961c4350528c`, run `41859720860` terminé avec succès, **1 333 entrées indexées, 27 archives et 110 médias vérifiés**, dernier chapitre des Origines **636**. La page d'accueil publique servie au même contrôle **ne contenait pas encore** « Dernières études par collection » : **les commits de cette exécution sont enregistrés, mais pas encore confirmés en production**.

Contrôles requis avant de conclure à la livraison : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, succès de l'exécution GitHub Pages, puis contrôle de `#home-etudes-recentes` et des cinq lecteurs HTTPS. Le contenu MC-049 ne pourra être présenté comme publié qu'après présence du reçu et de son URL publique.
