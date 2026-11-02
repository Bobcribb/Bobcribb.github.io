# MYTHOS — Encyclopédie sur GitHub Pages

**Site public : https://bobmythos.fr/**  
**Domaine alternatif : https://bobcribb.github.io/** (redirige vers le domaine principal).

MYTHOS est une encyclopédie comparative en français publiée **gratuitement sur GitHub Pages**. Le dépôt et les fichiers HTML sont une copie fonctionnelle des publications WordPress et servent le site depuis novembre 2026.

## État validé le 2 novembre 2026

- 502 dossiers publics indexés lors de la dernière synchronisation vérifiée. Le catalogue peut évoluer.
- **110 médias originaux, images et PDF**, hébergés dans `media/2026/10/` sur GitHub Pages (environ 200 Mo), avec hashes SHA-256 dans `media/manifest.json`.
- Les pages utilisent des liens locaux `/media/...` et n'ont plus besoin de WordPress pour afficher les images importées.
- Les **134 brouillons de pages et 1 brouillon d'article** sont stockés **en privé sur Google Drive**, dans 15 volumes d'archive. Ne pas les ajouter au dépôt public.
- Une sauvegarde séparée des **110 médias** existe aussi en privé sur Google Drive (8 archives ZIP).
- DNS du domaine enregistré chez WordPress.com : 4 adresses A GitHub et un CNAME www vers `bobcribb.github.io`.
- HTTPS du domaine **sans `www`** vérifié ; le certificat/accès de `www.bobmythos.fr` peut encore être en attente.

## Forfait WordPress et nom de domaine : abonnements distincts

L'hébergement WordPress.com **Personal** à 9 €/mois n'est plus nécessaire pour servir les pages et les 110 médias déjà copiés sur GitHub. **Ne jamais résilier ni supprimer l'enregistrement du domaine `bobmythos.fr`**, facturé séparément environ 8 €/an, si l'on veut garder cette adresse. Ne pas supprimer le compte WordPress.com ou le site source en cas d'utilisation future de son éditeur.

Pour ne plus payer le forfait Personal : annuler **l'abonnement d'hébergement**, pas le domaine. WordPress.com conserve normalement les pages, les articles et les médias d'un site rétrogradé à l'offre gratuite.

## Publication entièrement indépendante de WordPress

Depuis le 2 novembre 2026, la publication MYTHOS repose sur le contenu **déjà versionné dans GitHub**, sans appel réseau à WordPress. Le workflow `.github/workflows/publish.yml` exécute `scripts/build_native.py`, contrôle les 110 médias et les 500+ dossiers, puis publie avec GitHub Pages.

Les nouvelles études peuvent être ajoutées à `chapitres/` comme fichiers Markdown, directement dans GitHub ou depuis ChatGPT avec le connecteur GitHub. Lire `chapitres/README.md` : les fichiers sont publiés automatiquement après push sur main, référencés dans le catalogue et indexés pour la recherche.

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
