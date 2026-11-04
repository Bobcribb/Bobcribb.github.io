# MYTHOS — Refonte du 4 novembre 2026 : dix monographies grecques reclassées et documents contrôlés

**Dépôt de vérité :** `Bobcribb/Bobcribb.github.io`, branche `main`.
**État initial contrôlé :** `37fd1cd3a148b1ca296e31f7a319ad5f56ae2ff9` (4 novembre 2026 à 22:52:55 UTC).
**Garde préalable :** lecture de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` sur `main`.

## A. Contenus intégraux nouveaux réellement intégrés

**Aucun nouvel inédit intégral déposé durant cette séance.** Justification vérifiable :

- État instantané de la file officielle : `editorial/inbox/` contient **282 demandes JSON**, dont **277 déjà attribuées** dans `editorial/numbering.json` et **5 retenues** dans `editorial/holds.json` ; **aucune demande valide non attribuée** à la lecture. La numérotation n'est jamais anticipée manuellement.
- Le dépôt public historique `Bobcribb/Mythos` comporte **205 fichiers suivis** dont **37 Markdown** ; l'inventaire exact, comparé aux chemins de l'actuel `main`, retrouve **36 Markdown sur 37**. La seule différence Markdown est `docs/etat-publication-images-3d.md`, une ancienne note de suivi de reconstitutions, **pas une étude universitaire intégrale inédite**. Les neuf anciennes études de comédie, les tomes historiques des *Origines du sacré*, les textes de Chiron et le document préparatoire Homère/Hésiode sont présents sous leurs chemins d'origine.
- Les quelques fichiers binaires, SVG 2,5D, scripts et notices d'anciennes reconstitutions absents par chemin ne sont pas de nouveaux manuscrits scientifiques à publier. Les SVG en perspective 2,5D retirés à la demande de l'utilisateur restent exclus.
- Les 135 anciens brouillons WordPress retrouvés dans Google Drive sont des archives **privées non approuvées** pour publication, et ne sont pas copiés dans le dépôt public. La recherche de matériaux publics nouveaux doit se poursuivre sans transformer un brouillon en monographie attribuée.

Il serait incorrect de créer un nouveau numéro, une seconde file UUID ou un résumé substitué à un texte intégral. Aucun manuscrit ni registre n'est modifié.

## B. Contenus universitaires existants effectivement améliorés dans la navigation

Les neuf manuscrits intégraux **391, 392, 393, 394, 395, 396, 397, 399, 400** figuraient encore, sur la dernière page de dossiers examinée, dans « Nouvelles études à classer (9) ». Le dixième, **423**, était déjà accessible mais rangé dans la catégorie générale des Olympiens, sans sous-dossier spécifique à son épiclèse cultuelle. Les dix Markdown sources ont été lus à leur chemin canonique, avec vérification des sections, des sources citées, de leur longueur et de leur bibliographie. Les numéros et chemins des lecteurs restent inchangés.

| Cote existante | Sujet du manuscrit intégral | Rubrique et nouveau sous-dossier |
|---|---|---|
| 391 | Aristée, apiculture et oliviers | Cultes et sanctuaires / Aristée — apiculture, techniques agraires et cultes |
| 392 | Hormè et l'élan vers l'action | Divinités / Hormè — impulsion et personnifications de l’action |
| 393 | Eukleia, renommée civique et sanctuaires | Cultes et sanctuaires / Eukleia — renommée civique et sanctuaires |
| 394 | Despoina et les mystères arcadiens | Cultes et sanctuaires / Lykosoura — Déméter, Despoina et mystères arcadiens |
| 395 | Britomartis et Dictynna | Cultes et sanctuaires / Crète — Britomartis, Dictynna et sanctuaires |
| 396 | Palémon, Mélicerte et Isthmia | Cultes et sanctuaires / Isthmia — Palémon, Mélicerte et jeux funéraires |
| 397 | Mélinoé et la tradition orphique | Divinités / Mélinoé — hymnes orphiques et puissances nocturnes |
| 399 | Iynx, torcol et roue magique | Sources anciennes / Pindare et Théocrite — persuasion et magie amoureuse |
| 400 | Ényô et la violence guerrière | Divinités / Ényô — puissances guerrières et violence destructrice |
| 423 | Apollon Agyieus et les piliers de seuil | Cultes et sanctuaires / Apollon Agyieus — voies, piliers et seuils sacrés |

La modification est volontairement limitée à dix règles explicites de `scripts/build_greek_folders.py`. Après reconstruction et déploiement réussi, le sommaire des dossiers créera une ancre `#theme-N` par sous-dossier ; le lecteur intégral conservera un renvoi réciproque vers son emplacement exact. Le générateur `verify()` rejette les références dupliquées, les URL absentes et les ancres inexistantes. **Il ne faut pas confondre cette correction de classification avec une nouvelle étude publiée.**

## C. Graphisme muséal et adaptation mobile

La charte **noir/anthracite et or/ivoire**, la bannière grecque avec statue à gauche et temple à droite, les huit familles illustrées, les crédits photographiques et les livres intégraux existants sont inchangés.

Améliorations CSS dans la génération des dossiers :
- Le titre de chaque carte et les photographies existantes s'adaptent aux **écrans de moins de 400 px** sans débordement horizontal.
- Les commandes de divulgation des **crédits d'images** et du **catalogue complet** disposent d'une zone tactile d'au moins **44 px**, en **conservant le marqueur natif** de `<summary>` (`display:list-item`).
- Les liens de sommaire et de monographie conservent leurs cibles tactiles, leur contraste et leurs indicateurs de navigation clavier.

Aucun SVG 2,5D ni photo hors sujet n'est introduit.

## D. Commits de l'intervention

1. `d3d04676991286719319f5e291414754bcbaa191` — dix classements thématiques vérifiables.
2. `f5897a5dff7c3c9a97b9af02081f1a31f942d107` — tests des manuscrits intégraux, cotes, sections et bibliographies.
3. `eb63b775c90522c2ef7ae7b9c4787207d0a62d52` — première adaptation CSS des cartes et accordéons.
4. `09af104017717b23bb112baff34dcd02439cccd0` — conservation des indicateurs natifs de divulgation.
5. `5b8c85522d044d3950b3bb5f7727e2be404084f2` — test de la mise en page étroite et des contrôles tactiles.

Le présent rapport constitue une sixième modification documentaire autonome.

## E. Vérification et limite

Le site public HTTPS `https://bobmythos.fr/catalog/publication-verification.json` affiche au premier contrôle **`source_commit=2f6cb0265003ba7a351af2964604d3a9f130807a`**, run **41925584632**, **1 401 documents indexés**, **27 archives** et **110 médias** vérifiés. Ce reçu correspond à une version **antérieure à nos correctifs**. La page publique des sources anciennes montrait encore les anciens rattachements lors de ce contrôle.

Les validations GitHub Actions des commits ci-dessus ont été déclenchées ; au dernier contrôle avant ce rapport, elles étaient en cours et n'étaient pas toutes terminées. Il reste à vérifier le succès du workflow, le nouveau reçu de publication et les pages publiques `/mythologie-grecque/dossiers/` et `/mythologie-grecque/dossiers/cultes-sanctuaires/` ; **ne pas annoncer un déploiement non confirmé**.

Contrôles attendus après succès : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, présence des dix renvois dans le HTML, de leurs sections et des ancres de retour ; absence des neuf études dans la rubrique générique.

**Préservation :** aucun fichier de `chapitres/`, des archives, `editorial/numbering.json`, `editorial/holds.json`, `EDITORIAL_NUMBERING.json`, ni aucun workflow GitHub ou horaire d'automatisation MYTHOS n'a été modifié.
