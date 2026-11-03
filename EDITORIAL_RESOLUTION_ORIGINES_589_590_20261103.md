# MYTHOS — Continuité éditoriale et réconciliation des rédactions parallèles 589–590

*État vérifié le 3 novembre 2026 après les commits des quatre fichiers. Ce dossier complète `EDITORIAL_CONTINUITY.md` et `EDITORIAL_RESOLUTION_ORIGINES_582_584_20261103.md`. Il ne remplace pas les manuscrits, ne les supprime pas et n'autorise pas la publication de brouillons privés.*

## Règle de priorité

Une exécution parallèle a créé deux études autonomes numérotées 589 et deux études autonomes numérotées 590. Le critère appliqué demeure celui déjà retenu pour 582 et 583 : **le premier commit GitHub confirmé garde le numéro canonique** ; le second fichier est intégralement conservé, lisible et renvoyé depuis le portail comme **complément non compté deux fois**. Le constructeur doit toujours refuser tout *autre* conflit de numérotation.

## État des fichiers originaux vérifié par l'historique GitHub (UTC)

- **589 canonique, 17:21:20** : `chapitres/origines-du-sacre/589-restaurer-oracles-didymes-recommencements.md`, étude « Réveiller un sanctuaire : Didymes, restauration des cultes et récits de recommencement ». Commit `e8a47be9473dea8a440981368f3a8fb37397de1f`. SHA de contenu relu `56e8780c0fee0c65ec0b8eb38179aadb63b0eaa9`. Taille 22 987 caractères.
- **589 complément, 17:22:22** : `chapitres/origines-du-sacre/589-questions-privees-dodone-famille-metiers-risque.md`, étude « Demander aux dieux pour vivre : famille, métier, commerce et incertitude dans les lamelles de Dodone ». Commit `984ce142c829895d327e2ff0fbdaa58e410c78af`. SHA de contenu relu `6461ef35b852973ce48c02fadc7704f5345e87d0`. 23 620 caractères ; étude indépendante, désormais appelée **complément du 589**, sans prétention à une seconde attribution.
- **590 canonique, 17:24:17** : `chapitres/origines-du-sacre/590-images-perdues-modeles-restauration-divine.md`, étude « Retrouver le dieu : images perdues, modèles retrouvés et légitimité des restaurations ». Commit `f675982ca9175f630bb20c923be23b406ccaf2a6`. SHA de contenu relu `2f72ef622d9937754d18177cbe2782d13e3270ed`. Taille 23 534 caractères.
- **590 complément, 17:24:38** : `chapitres/origines-du-sacre/590-reponse-en-voyage-messagers-ambassades-transmission.md`, étude « La réponse en voyage : messagers, ambassades et transmission des paroles divines entre sanctuaire et pouvoir ». Commit `8dce0854ef9ea8a43b893dce1dc6207a11da2793`. SHA de contenu relu `f8ca026788a381d455711e85e0af3dfbc4df5554`. 27 925 caractères ; étude indépendante désormais appelée **complément du 590**.

## Protection dans le générateur

Le fichier `scripts/origines_reconciliation.py` a été mis à jour par le commit **`0099c9cacb37666997d1763114d6739412865a6e`**. Il ajoute les deux premiers fichiers 589/590 dans `CANONICAL` et les deux versions ultérieures dans `COMPLEMENTS` avec `inline=True`. Les compléments doivent rester accessibles comme **pages intégrales distinctes**, sans redirection forcée, et sont exclus uniquement du sommaire canonique numéroté. Le sommaire des annexes doit offrir un lien ; un renvoi dans le 589/590 canonique doit y mener. Le nombre de sources protégées par SHA-256 augmente avec ces quatre fichiers ; leurs octets restent inchangés pendant la construction.

Le workflow GitHub Pages se déclenche sur la modification de ce module, mais **son succès et la disponibilité HTTPS doivent encore être vérifiés** pour l'exécution issue du correctif. Le seul fait que les commits et les fichiers soient lisibles dans `main` ne suffit pas à dire que les quatre pages sont publiées.

## Règle pour les exécutions suivantes

**Vérifier à nouveau les fichiers `chapitres/origines-du-sacre/` puis le dernier numéro canonique du catalogue avant toute création.** Une étude annoncée comme « prochain chapitre » ne réserve pas ce numéro contre une autre production. Ne pas créer de 589 ni de 590 supplémentaires. Le sujet suggéré à la fin du complément 590, « Une réponse dans les archives : inscriptions publiques, décisions civiques et mémoire des consultations », reste une proposition, **sans numéro réservé**, à confronter à l'état de la série et au corpus existant.

**Bilan :** deux nouvelles études rédigées, 51 545 caractères, intégralement enregistrées dans GitHub et conservées comme compléments ; les premiers 589 et 590 respectés. Aucun contenu WordPress privé modifié.
