# MYTHOS — Continuité éditoriale, source de vérité et protection contre les pertes

Dernière consolidation : 2 novembre 2026.

## Architecture retenue

- **GitHub** (dépôt `Bobcribb/Bobcribb.github.io`, branche `main`) est la source de publication de `https://bobmythos.fr/`.
- **WordPress** est une source historique à préserver, et non le moteur de déploiement GitHub. Ne pas y publier de nouvelles pages à la place de GitHub : cela crée des écarts.
- Les **134 brouillons de pages et l'article brouillon** restent privés sur Google Drive, jamais dans ce dépôt public.
- Les **110 médias** sont enregistrés dans `media/2026/10/`, contrôlés par `media/manifest.json`. Une seconde copie indépendante est privée sur Google Drive.
- Une **archive intégrale de l'état du dépôt GitHub**, fichiers HTML, Markdown, médias, workflows et scripts, est conservée dans le Drive privé MYTHOS, dossier « Archives intégrales GitHub — MYTHOS — 2026-11-02 ».
- Les exports GitHub ne remplacent pas un export natif WordPress WXR/XML si l'on veut restaurer les blocs Gutenberg, menus et métadonnées d'origine.

## Circuit obligatoire pour chaque nouveau chapitre automatique

1. Vérifier la dernière production **réellement publiée dans la série concernée**, puis rédiger un nouveau chapitre inédit, sourcé, avec bibliographie et distinction entre faits, hypothèses et reconstitutions.
2. Nommer un chemin **unique** sous `chapitres/`, sans caractères spéciaux ni accent dans les noms de répertoires/fichiers :
   - `chapitres/encyclopedie/chapitre-260-nom-du-dieu.md`
   - `chapitres/comparatif/volume-lv-sujet.md`
   - `chapitres/comedies/auteur-oeuvre-analyse.md`
   - `chapitres/tragedies/volume-xcix-oeuvre.md`
   - `chapitres/origines-du-sacre/tome-xxxviii-chapitres-443-450.md`
3. Le fichier doit commencer par un titre Markdown `#` et, si utile, par le front matter simple `title:` / `description:`. Les contenus sont **publics** ; ne jamais publier des brouillons confidentiels.
4. Vérifier qu'aucun fichier de même adresse n'existe déjà. Utiliser le connecteur GitHub pour créer le nouveau fichier sur `main`; pour compléter une étude existante, récupérer son SHA et mettre à jour uniquement ce fichier.
5. Confirmer le commit GitHub. Le workflow de publication reconstruit le site et référence automatiquement les fichiers de `chapitres/` dans le catalogue, la recherche et le sitemap.
6. Vérifier le workflow et la page HTTPS publique ; si cela échoue, **déclarer « version GitHub enregistrée, publication non vérifiée »**. Si la création GitHub échoue, **déclarer « chapitre livré dans la conversation uniquement, à intégrer »**.
7. Conserver l'ordre et la numérotation propre à chacune des cinq séries. Aucune série ne doit déduire son dernier numéro des autres séries.

## Contrôles de perte et de cohérence

- `.github/workflows/audit-integrity.yml` : vérifier pages locales, liens internes, médias et SHA-256 après reconstruction.
- `.github/workflows/backup-complete.yml` : produire une archive du dépôt en parties vérifiables ; ses artifacts GitHub expirent et ne sont **pas** une sauvegarde hors GitHub avant leur copie sur Drive.
- Contrôler régulièrement les publications WordPress résiduelles ou les productions de conversations non transférées sur GitHub : les automatismes de GitHub n'ont pas accès à ces deux sources sans action supplémentaire.
- Avant tout nettoyage, suppression de fichiers, fusion de pages, changement de domaine ou annulation WordPress, vérifier que le contenu demandé existe dans GitHub et dans une archive indépendante.

## Restauration du site GitHub

1. Télécharger **tous** les volumes ZIP de l'archive intégrale du même jeu de sauvegarde, ainsi que le ZIP manifeste.
2. Extraire les ZIP : chacun contient un fichier `MYTHOS-source-integrale.tar.gz.part-NN`.
3. Vérifier les SHA-256 de chaque morceau à l'aide de `VOLUMES_SHA256.txt`.
4. Réassembler dans l'ordre : `cat MYTHOS-source-integrale.tar.gz.part-* > MYTHOS-source-integrale.tar.gz`.
5. Vérifier la somme de l'archive entière dans `ARCHIVE_SHA256.txt`.
6. Extraire dans un nouveau dossier propre avec `tar -xzf MYTHOS-source-integrale.tar.gz`.
7. Pousser les fichiers dans un dépôt GitHub de restauration, exécuter `python scripts/build_native.py` puis `python scripts/audit_integrity.py`; reconfigurer Pages et le domaine si nécessaire.

**Limite documentée :** l'archive intégrale contient les fichiers de travail de la version GitHub, mais pas l'historique interne `.git`, ni l'état privé des automations, ni un export complet natif WordPress. Les archives privées de brouillons et médias doivent donc être conservées séparément.

## Architecture de navigation pérenne — demande du 2 novembre 2026

**Principe directeur : MYTHOS est une encyclopédie des mythologies du monde**, et non un simple catalogue alphabétique d'articles grecs. La Grèce antique est traitée en priorité et particulièrement visible, mais l'Égypte, la Mésopotamie, la Perse, l'Inde, la Chine, le Japon, les sociétés africaines, les Amériques et l'Océanie doivent rester accessibles au même niveau encyclopédique.

La navigation officielle, commune à toutes les pages, est :
1. **Mythologies du monde** — panorama des grandes traditions, dieux et récits ;
2. **Grèce antique** — porte d'entrée mise en avant : dieux, héros, Homère, Hésiode, cultes et sanctuaires ;
3. **Théâtre grec** — section indépendante pour tragédies, comédies, œuvres perdues, reconstitutions et commentaires ;
4. **Études philosophiques** — section indépendante pour Hegel, Nietzsche, historiographie, lectures philosophiques et mythologie comparée ;
5. **Civilisations du monde** — accès **par continent** : Afrique, Europe, Asie, Amériques, Océanie. Ce classement est un outil de navigation moderne, non une catégorie historique figée ;
6. **Index intégral** — tous les dossiers, consultables alphabétiquement, sans suppression ;
7. **Recherche** — moteur transversal des documents publiés.

L'accueil doit présenter ces parcours, jamais une sélection arbitraire des premiers dossiers par ordre alphabétique. Maintenir la présentation muséale **noir/anthracite, ivoire et or** et une navigation lisible sur téléphone. Ne pas faire disparaître un dossier à l'occasion d'une réorganisation.

**Mise en œuvre durable :** \`scripts/build_navigation.py\` génère l'accueil et les portails \`/mythologies/\`, \`/grece/\`, \`/theatre/\`, \`/philosophie/\`, \`/civilisations/\` et les cinq portails continentaux. \`scripts/build_native.py\` l'appelle lors de chaque publication, puis réindexe l'ensemble. Les mises à jour éditoriales ne doivent pas remplacer ce système par l'ancienne page d'accueil à 24 liens ni par la simple liste alphabétique.

Vérifier après chaque modification le fonctionnement des menus, l'accessibilité mobile, les liens internes, le nombre de dossiers et les 110 médias locaux. Conserver l'indépendance de WordPress et ne pas modifier les DNS ou le domaine pour une simple réorganisation de la navigation.
