# MYTHOS — Encyclopédie sur GitHub Pages

**Site public : https://bobmythos.fr/**  
**Domaine alternatif : https://bobcribb.github.io/** (redirige vers le domaine principal).

MYTHOS est une encyclopédie comparative en français publiée **gratuitement sur GitHub Pages**. Le dépôt et les fichiers HTML sont une copie fonctionnelle des publications WordPress et servent le site depuis novembre 2026.

## État validé le 2 novembre 2026

- Plus de 500 dossiers publics indexés. Le compteur évolue avec les publications GitHub ; consulter `search.json` pour le total réel.
- **110 médias originaux, images et PDF**, hébergés dans `media/2026/10/` sur GitHub Pages (environ 200 Mo), avec hashes SHA-256 dans `media/manifest.json`.
- Les pages utilisent des liens locaux `/media/...` et n'ont plus besoin de WordPress pour afficher les images importées.
- Les **134 brouillons de pages et 1 brouillon d'article** sont stockés **en privé sur Google Drive**, dans 15 volumes d'archive. Ne pas les ajouter au dépôt public.
- Une sauvegarde séparée des **110 médias** existe aussi en privé sur Google Drive (8 archives ZIP).
- DNS du domaine enregistré chez WordPress.com : 4 adresses A GitHub et un CNAME www vers `bobcribb.github.io`.
- HTTPS du domaine **sans `www`** vérifié ; le certificat/accès de `www.bobmythos.fr` peut encore être en attente.

## Forfait WordPress et nom de domaine : abonnements distincts

L'hébergement WordPress.com **Personal** à 9 €/mois n'est plus nécessaire pour servir les pages et les 110 médias déjà copiés sur GitHub. **Ne jamais résilier ni supprimer l'enregistrement du domaine `bobmythos.fr`**, facturé séparément environ 8 €/an, si l'on veut garder cette adresse. Ne pas supprimer le compte WordPress.com ou le site source en cas d'utilisation future de son éditeur.

Pour ne plus payer le forfait Personal : annuler **l'abonnement d'hébergement**, pas le domaine. WordPress.com conserve normalement les pages, les articles et les médias d'un site rétrogradé à l'offre gratuite.

## Nouveau circuit éditorial : Drive → GitHub

Depuis le 2 novembre 2026, **Google Drive est le fonds de travail et de sauvegarde** des documents MYTHOS, tandis que **GitHub est la source technique de publication** de l'encyclopédie. La copie sauvegardée sur Drive comporte notamment un ensemble annoncé de 520 dossiers ; elle ne doit pas être utilisée pour écraser le dépôt GitHub, qui contenait 552 entrées lors de la vérification du 2 novembre.

Pour tout nouveau texte, on lit d'abord le document Drive, on vérifie s'il est déjà publié sur GitHub, puis on intègre la version éditoriale dans `chapitres/` sans doublon. **Les brouillons archivés en privé dans Drive ne sont pas automatiquement rendus publics.**

Le premier dossier transféré dans ce circuit est `chapitres/grece/mycenes-citadelle-palais-et-atrides.md`, issu d'un texte Drive sur Mycènes et adapté à la présentation encyclopédique.

**Procédure détaillée :** [Protocole Google Drive → GitHub](docs/PROTOCOLE_DRIVE_VERS_GITHUB.md).

## Publication entièrement indépendante de WordPress

Depuis le 2 novembre 2026, la publication MYTHOS repose sur le contenu **déjà versionné dans GitHub**, sans appel réseau à WordPress. Le workflow `.github/workflows/publish.yml` exécute `scripts/build_native.py`, contrôle les 110 médias et les 500+ dossiers, puis publie avec GitHub Pages.

Les nouvelles études numérotées passent par `editorial/inbox/` : [attribution atomique et reprise des publications concurrentes](docs/PUBLICATION_CONCURRENTE.md). Le texte intégral approuvé est déposé avec un UUID unique ; le workflow attribue le prochain numéro de sa collection depuis `main` et enregistre le reçu avec le manuscrit. Les études indépendantes sans numéro et les corrections restent des fichiers Markdown dans `chapitres/`. Lire `chapitres/README.md`.

Une vérification horaire republie le site existant si nécessaire, mais **n'invente pas de nouveaux chapitres**. Les automations éditoriales de ChatGPT restent distinctes ; leurs nouvelles productions doivent être enregistrées dans le dépôt GitHub pour apparaître sur le site.

L'ancienne API WordPress n'est conservée que dans `scripts/build.py` à des fins d'archive et d'import manuel. Elle ne fait plus partie du workflow de publication. Le site conserve ses dossiers HTML et ses 110 médias originaux dans GitHub, ainsi que des sauvegardes privées sur Drive. La rétrogradation du site WordPress vers le forfait gratuit ne fait pas disparaître la bibliothèque GitHub.

## Fichiers et restauration

- `scripts/build.py` : conversion WordPress public vers HTML et index.
- `scripts/pin_media.py` : copie/cache des médias WordPress vers GitHub.
- `media/manifest.json` : inventaire des 110 fichiers locaux et checksums.
- `search.json`, `recherche/`, `rubriques/` : catalogue et recherche.
- `sitemap.xml`, `robots.txt`, `CNAME` : indexation et domaine.
- Sauvegardes privées Drive distinctes : brouillons, médias originaux et procédures de restauration.

GitHub Pages est une plate-forme statique : les commentaires, formulaires et plugins WordPress dynamiques ne sont pas reproduits.

## Précautions

Ne pas supprimer le dépôt `Bobcribb/Bobcribb.github.io`, le domaine `bobmythos.fr`, ni les archives Drive. Après toute modification DNS ou renouvellement du domaine, vérifier https://bobmythos.fr/, une page intérieure, une image dans /media/ et le cadenas HTTPS.
