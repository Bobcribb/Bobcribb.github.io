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

## Édition et synchronisation

Le workflow [Synchroniser MYTHOS vers GitHub Pages](.github/workflows/publish.yml) construit le site depuis les **pages WordPress publiées**, puis préserve localement les médias, les publie sous la racine GitHub Pages et déploie le site. Il est programmé environ une fois par heure, sous réserve de la disponibilité de l'API publique WordPress.com et des délais GitHub Actions. La publication ultérieure de nouveaux chapitres nécessite qu'ils apparaissent dans WordPress, ou soient ajoutés directement à GitHub. Les tâches de rédaction ChatGPT ne publient pas automatiquement des pages.

Le générateur impose au moins **400 pages publiques** avant de remplacer le site : si le site WordPress devient inaccessible ou privé après rétrogradation, le workflow échouera, **mais les 502 dossiers déjà copiés et les 110 médias resteront publiés sur GitHub**. Il faudra alors passer à une gestion éditoriale GitHub-native.

Les six PDF externes figurant dans les bibliographies ne sont pas revendiqués comme médias MYTHOS et conservent leurs URL d'origine.

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
