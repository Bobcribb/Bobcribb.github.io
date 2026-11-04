# MYTHOS — Refonte, 4 novembre 2026 (21 h 56–22 h 03, Paris) : renvois exacts vers les sous-dossiers grecs

## 1. Contrôle préalable et garde éditoriale

- Dépôt public `Bobcribb/Bobcribb.github.io`, branche `main` ; tête initialement contrôlée `f96442c423be72a9bcccece40e49988616018885`.
- `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relus avant toute opération. Aucun chapitre numéroté n'a été créé directement ; le registre d'attribution, les demandes de `editorial/inbox/`, les cinq collections et les workflows n'ont pas été modifiés par cette intervention.
- Recherche parmi les sources accessibles : l'ancien dépôt `Bobcribb/Mythos` et sa comparaison avec le dépôt principal ont déjà été audités (205 anciens fichiers, sans manuscrit universitaire public complet absent du dépôt principal identifié) ; une nouvelle recherche de fichiers Google Drive pour MYTHOS a trouvé 21 documents intitulés MYTHOS ou liés au dossier. Il s'agit notamment de 15 volumes de **brouillons** WordPress sauvegardés, de l'inventaire documentaire et des versions d'un dossier *Horizon d'Aton* dont le lecteur se trouve déjà sur GitHub. Les brouillons privés ne sont pas assimilés à des textes approuvés.
- **Photographie de la file sur `main` après les premières corrections : 272 demandes, dont 265 ayant reçu une attribution, 5 explicitement retenues dans `editorial/holds.json` et 2 nouvelles demandes en attente de reçu.** Deux dernières soumissions, déjà présentes dans la file et à ne pas dupliquer : `6d7fd89c-2d44-4ef5-95a7-5d574d6d0057` (mythologie comparée, MC-057, environ 78 577 caractères) ; `7ba0d991-faa9-4dd0-995c-95a71a3bff61` (Salmakis et l'inscription d'Halicarnasse, environ 43 983 caractères). Chacune a sa collection et son slug, les variables requises et une bibliographie ; leur numérotation reste à attribuer par Actions.
- Le chapitre 421, consacré aux Praxidikai, est déjà présent avec son Markdown et sa page HTML. Le chapitre 420, Makaria, et les archives des 27 tomes sont également conservés.

**Nouvelle publication universitaire effectuée par cette intervention : aucune.** Aucun texte entier, approuvé, public, nouveau et indépendant n'a été trouvé en dehors du circuit d'attribution existant. Les manuscrits en attente ne sont **pas** libres d'être resoumis ou copiés ; les cinq retenues exigent une réconciliation philologique, les anciennes sauvegardes sont privées ou déjà couvertes.

## 2. Modification réelle : liens bidirectionnels de précision

Les dossiers grecs étaient bien organisés en huit familles thématiques, mais sur les pages des études le retour ne visait que la **page générale de la famille**. Par exemple, une étude sur l'oracle de Delphes pouvait revenir à « Cultes et sanctuaires », mais pas directement à la sous-section exacte où figurait son lien.

Le générateur `scripts/build_greek_folders.py` utilise désormais une unique table ordonnée `subsets_by_folder` pour :

1. construire le sommaire des sous-dossiers d'une famille, dont les ancres ont la forme `#theme-1`, `#theme-2` ... ;
2. générer dans la page de lecture, **hors du texte scientifique**, un troisième maillon du fil d'Ariane : « Sous-dossier : [rubrique exacte] », pointant vers la même ancre ;
3. reconstruire les listes de ces sous-dossiers avec exactement la même numérotation, sans copier ni déplacer l'étude.

Un lecteur de *Delphes* dispose ainsi d'un retour vers `/mythologie-grecque/dossiers/cultes-sanctuaires/#theme-1` dans la fixture vérifiée ; l'étude de *Bendis*, dans une rubrique distincte de la même famille, retourne vers `#theme-2`. Les valeurs sont calculées automatiquement sur le vrai inventaire à chaque reconstruction ; aucun numéro de chapitre ni classement canonique n'est inventé.

### Graphisme, responsive et accessibilité

Le design de référence noir, ivoire et or et la bannière statue/temple sont préservés sans nouvel SVG ni illustration 2,5D. L'ajout porte sur le fil d'Ariane et la consultation :

- lien de retour souligné en or, contrasté et accessible au clavier ;
- débordement des titres très longs maîtrisé par les styles préexistants ;
- marge `scroll-margin-top:115px` sur les destinations `#theme-*`, afin d'éviter que le bandeau fixe ne masque le titre du sous-dossier sur smartphone et ordinateur ;
- contour visible de la destination ciblée (`:target`) ; aucune modification du HTML de l'étude elle-même, de son sommaire interne, de ses sources ou de sa bibliographie.

## 3. Commits réalisés dans cette séance

1. `edc507d0f309ccab49f9dcc448a652e4d4569be6` — génération partagée des liens retour et amélioration CSS.
2. `5e9c3ad7e6ac7b5deea7a26fcb515818a631ba35` — régression testant l'identité de l'ancre entre le lecteur et le sommaire.
3. `cc8c242feab99881e0e2276a45f37bb5df9437f2` — ajout d'une deuxième sous-rubrique dans la fixture, pour contrôler les indices distincts et la répétabilité sans altération du texte.
4. `41a8f641d9775aa2ff406112bdad5455eeb236be` — correction du test : la rubrique de Bendis se nomme exactement « Cultes thraces et célébrations en Attique » ; le test ne doit pas chercher « Bendis » dans cette rubrique.

Des commits indépendants ont également été soumis par d'autres cycles horaires pendant cette séance. Ils ne sont pas revendiqués comme modifications de cette intervention.

## 4. Vérification et état du déploiement

- Relecture de `main` après modifications : le générateur possède la table partagée et le lien `greek-folder-return-topic`, les styles d'ancrage et le test correctif sont présents.
- GitHub Actions, ancienne exécution `41911906113` sur `cc8c242f` : **échec observé** du test du second thème, avec `AssertionError: 'Bendis' not found in 'Sous-dossier : Cultes thraces et célébrations en Attique'`. Cette erreur d'assertion est corrigée en `41a8f641`.
- La validation `41912286689` sur le correctif et `41912337278` sur un commit postérieur étaient **en cours** au dernier contrôle. La publication correspondant au nouveau générateur n'est donc **pas revendiquée comme achevée**.
- Le reçu HTTPS `https://bobmythos.fr/catalog/publication-verification.json` affichait encore `source_commit=38558e7b9335f7314dde6803f721c2e4e512b562`, 1 389 documents, 27 archives, 110 médias. Le navigateur public montrait bien les sommaires `#theme-1` dans `/mythologie-grecque/dossiers/cultes-sanctuaires/`, mais le retour nouveau `greek-folder-return-topic` n'était pas encore visible sur le lecteur *Épiménide*.

**Vérifications restantes après déploiement :** tests complets `python -m unittest discover -s tests -v` ; `python scripts/build_native.py` ; `python scripts/verify_publication.py` ; résultat GitHub Actions ; mise à jour du reçu public ; puis HTML public d'une étude avec lien direct vers son sous-dossier et ancre effectivement présente. Ne pas annoncer un nouveau chapitre comme publié tant que son reçu et son URL HTTPS ne sont pas vérifiés.

Aucune automatisation ni horaire MYTHOS n'a été modifié.
