# MYTHOS — Google Drive vers GitHub, sans WordPress

**Décision éditoriale : 2 novembre 2026.**

## Rôles

- **Google Drive : fonds de travail et sauvegarde externe.** Les textes d'origine, versions de recherche, dossiers bibliographiques et archives conservés dans Drive sont les pièces à inventorier et à relire avant leur publication.
- **GitHub : dépôt public et source technique de publication.** Le dépôt `Bobcribb/Bobcribb.github.io` sur la branche `main` héberge les fichiers HTML et Markdown, le catalogue, les médias et le générateur.
- **GitHub Pages : hébergement du site `bobmythos.fr`.** Le workflow `.github/workflows/publish.yml` reconstruit le site avec `scripts/build_native.py`. Il n'a pas besoin de l'API WordPress.
- **WordPress : archive historique uniquement.** Aucune nouvelle étude ne doit y être publiée ou modifiée dans ce circuit. Aucun domaine, abonnement ou contenu WordPress n'est supprimé automatiquement.

## Inventaire reconnu

Lors du contrôle du 2 novembre 2026 :

1. Le Drive privé « MYTHOS — sauvegarde privée (images et brouillons) » contient une archive intégrale du dépôt GitHub, avec un dossier annoncé à **520 dossiers** et une sauvegarde précédente à 503 dossiers.
2. Une autre série contient **15 volumes de sauvegarde, correspondant à 134 pages et 1 article initialement enregistrés comme brouillons WordPress**. Ces contenus historiques restent **privés sur Drive** jusqu'à examen individuel ; ne pas transférer automatiquement les documents bruts dans ce dépôt public.
3. Les documents de médiathèque incluent un inventaire des **110 médias originaux** ; les fichiers correspondants sont déjà versionnés dans `media/2026/10/` et leur intégrité est vérifiable par `media/manifest.json`.
4. L'index GitHub `search.json` comporte **552 entrées au contrôle préalable**. Il est donc plus récent ou plus complet que le nombre indiqué par l'archive de 520 ; **ne jamais écraser le dépôt par une sauvegarde ancienne**.

Ces chiffres sont des instantanés, pas des compteurs mis à jour automatiquement par ce fichier.

## Mode opératoire de publication

1. **Lire Google Drive en premier** : identifier le texte original, ses versions, sa source et son statut de diffusion.
2. **Comparer avec GitHub** : chercher par auteur, œuvre et titre dans `search.json`, `chapitres/` et les HTML publiés. Éviter les doublons et conserver les identifiants des séries universitaires existantes.
3. **Préparer la publication** : conserver le contenu original dans Drive. Rédiger un texte destiné au public avec titres, sources et distinctions explicites entre faits attestés, hypothèses et reconstitutions. Ne pas importer des informations personnelles ni des notes de travail internes.
4. **Importer sur GitHub** :
   - nouvelle étude publique : `chapitres/<collection>/<nom-unique>.md` (minuscules, chiffres et tirets uniquement pour le chemin) ;
   - correction d'une étude déjà publiée : modifier **le fichier existant**, à partir de son SHA actuel, sans créer une version parallèle ;
   - les liens médias doivent viser les fichiers locaux `/media/...` quand ils existent.
5. **Contrôler** le commit, la génération GitHub Actions, le titre, le référencement dans `search.json`, les liens internes et l'URL publique. Un commit réussi **n'est pas** à lui seul une preuve que Pages a été déployé.
6. **Sauvegarder** : après publication vérifiée, intégrer la version du dépôt dans les sauvegardes Drive selon le processus habituel, sans supprimer les versions antérieures.

## Règles de classement

- **Tragédies / comédies** : auteur → œuvre → résumé et sources ; reconstitution moderne identifiée.
- **Analyses philosophiques** : bibliothèque distincte, renvois explicites à l'œuvre correspondante, sans mélanger les résumés.
- **Numéros** : la numérotation de présentation des œuvres ne se confond jamais avec celle des volumes universitaires. Les séries de recherche conservent leur suite propre, sans doublon.
- **Design** : musée numérique noir/anthracite, ivoire et or, images sourcées, navigation mobile lisible, Grèce en priorité et accès complet aux autres civilisations.
- **Confidentialité** : aucun brouillon privé, fichier personnel, identifiant de compte ou sauvegarde ZIP intégrale privée ne doit entrer dans le dépôt public sans examen de diffusion.

## Première intégration depuis Drive

- **Mycènes — citadelle, palais et mémoire des Atrides** :
  `chapitres/grece/mycenes-citadelle-palais-et-atrides.md`
- Source éditoriale : document Google Drive « Mycènes », septembre 2026.
- Seule l'étude historique a été adaptée : les consignes personnalisées de visite et les données pratiques datées restent dans le document source.
- L'image de la Porte des Lionnes est prise dans la médiathèque GitHub déjà versionnée.

## Limite technique explicite

Aucun service de synchronisation automatique permanente de Google Drive vers GitHub n'a été installé. Le transfert est effectué par les outils connectés lorsque l'utilisateur le demande ; GitHub Actions assure ensuite la compilation et la publication autonome **à partir des fichiers présents dans GitHub**. Pour un import automatique récurrent, un connecteur de service et une authentification Drive dédiés seraient nécessaires. Ils ne doivent jamais être ajoutés au dépôt sous forme d'identifiants en clair.
