# MYTHOS — Refonte : recherche partageable et navigation des dossiers grecs

**Contrôle documentaire :** 5 novembre 2026, environ 09 h 54 UTC. Dépôt public `Bobcribb/Bobcribb.github.io`, branche `main`. Consignes `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relues avant l'intervention.

## 1. Recherche de contenu intégral et état de publication

État de la file GitHub lors de la lecture : **378** fichiers `editorial/inbox/*.json`, **363** UUID avec attribution dans les cinq collections de `editorial/numbering.json`, **9** demandes retenues dans `editorial/holds.json`, et **6** demandes déjà soumises mais sans attribution. Les six objets en attente ne sont **pas des manuscrits oubliés à retransférer** : leur source intégrale existe déjà sous le même UUID dans la file. La file et les reçus continuent d'évoluer avec les autres travaux MYTHOS.

Les six demandes en attente au contrôle concernent deux études comparatives sur le souffle divin et la prière sans réponse, trois textes des `Origines du sacré` autour de Nombres 19 et Lévitique 21, et une étude encyclopédique de Poséidon Onchestios ; les candidats ne doivent pas recevoir un numéro ou un second UUID sans le workflow d'attribution. Plus précisément, les slugs étaient `mc-069-quand-les-dieux-respirent-souffle-vent-vie-parole-mortalite`, `nombres-19-vache-rousse-cendres-eau-lustrale-mort-impurete`, `mc-073-quand-les-dieux-se-taisent-prieres-sans-reponse-ecoute-divine-attente-justice`, `levitique-21-pretres-deuil-cadavre-saintete-ezechiel-44-nazir`, `poseidon-onchestios-onchestos-chars-sans-conducteur-federation-beotie` et `levitique-21-pretres-morts-proches-grand-pretre-ezechiel-44`. Deux titres portent sur Lévitique 21 : vérifier leur rapport éditorial sans supprimer ni fusionner leurs manuscrits.

Ont également été inspectés l'inventaire `corpus/mythologie-grecque/archives/` (archives grecques HTML déjà dans le dépôt), les neuf dossiers existants de comédies dans `corpus/theatre-grec/comedies/` (leurs études HTML sont déjà présentes et servent de ressources au site), le corpus source de l'Énéide (18 fichiers, de l'introduction aux sources déjà exploitées par la publication), et le dossier `contenus/philosophie/homere-hesiode-dossier-preparatoire.md` (document annoncé comme préparatoire, non une monographie intégrale inédite et approuvée).

L'étude intégrale *La Galigo* est déjà accessible à `/bibliotheque-mythologies-du-monde/mythos-volume-19-la-galigo-bugis-sawerigading/` ; un nouvel import serait un doublon. Les 135 sauvegardes WordPress sur Google Docs portent une restriction documentaire explicite de non-publication sur GitHub : elles restent des brouillons privés.

**Premières publications universitaires intégrales cette séance : 0.** Aucun candidat complet, approuvé, distinct et absent du site public n'a été établi. Ce refus de transfert est intentionnel : ne pas transformer un texte déjà public, un document préparatoire ou un brouillon privé en prétendue découverte, et ne pas créer de doublon ou de collision de numérotation.

## 2. Travail concret sur les huit dossiers

`assets/greek-folder-filter.js` conserve désormais le critère dans le paramètre `?filtre=` d'un lien partageable ; une visite directe restaure automatiquement les résultats, y compris les accents. Le filtre ne modifie ni les textes scientifiques ni l'ordre de classement : il agit sur la visibilité des entrées de sommaire, tout en conservant les autres paramètres URL.

Lorsqu'un lien de sommaire `#theme-…` mène vers une rubrique actuellement masquée, la rubrique complète est réaffichée et le critère enregistré supprimé, afin d'éviter une ancre inaccessible. La recherche s'efface au clavier (Échap) ou au bouton prévu ; la navigation par l'historique restaure également un filtre présent dans l'URL. Le compteur accessible demeure annoncé par `role=status` et `aria-live=polite`. Sans JavaScript, tous les liens restent présents dans le HTML source.

La charte noir/anthracite, or et ivoire, la bannière statue grecque à gauche/temple à droite, les huit cartes thématiques avec images sourcées, le responsive et les liens réciproques restent préservés, sans retour des images 2,5D. Aucun fichier de chapitre, manuscrit, bibliothèque, archive, registre de numérotation ou automatisation n'est modifié.

## 3. Commits et régressions

- `d0ede6fda1581cc51e6288d7d987423033c3fe5d` — filtre URL partageable, retour d'ancre et historique navigateur.
- `c2140f80e23117c0b5aa4ca1491168ee4069399b` — nouveau test JS avec DOM simulé, deux sous-dossiers, entrée directe, recherche, effacement et retour historique.
- `1b5b2814f6b1b06d1d5ac854dd5074bd48a5fb7b` — intégration du test JS à la suite Python `unittest` (saut explicite en l'absence de Node.js).

Contrôle prévu et reproductible : `node tests/greek_folder_filter_bookmarks_20261105.cjs` puis `python -m unittest discover -s tests -v`. Le workflow GitHub `42006233397` avait démarré en **cours d'exécution** au contrôle suivant les commits. Son résultat final, comme la réussite du déploiement, ne doit pas être présumé.

Le reçu `catalog/publication-verification.json` dans le dépôt indiquait alors `source_commit=c619d0c709f37a10555ef681bfec00b77ad2dc92`, **1 488 documents indexés, 27 archives et 110 médias** : il ne prouve pas encore le déploiement de la présente modification. Le domaine HTTPS `bobmythos.fr` et le reçu public n'ont pas pu être interrogés de manière concluante via l'outil de navigation. Vérifier le succès Actions et le reçu public actualisé avant d'annoncer la mise en ligne du filtre partageable.
