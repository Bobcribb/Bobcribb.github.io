# MYTHOS — 4 novembre 2026 : rattachement de quatorze monographies au dossier grec et navigation tactile

## 1. Garde éditoriale et vérification des sources

Dépôt de référence : `Bobcribb/Bobcribb.github.io`, branche `main`. À l'ouverture, commit `93ad123fc79154d66ef73a0c770d17f7dc929117` ; `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` lus avant la moindre modification. Aucun chapitre numéroté n'est créé à la main, aucun numéro ou reçu n'est inventé, et les fichiers de `editorial/numbering.json`, `editorial/holds.json` et `editorial/inbox/` restent inchangés.

Inventaire de contrôle : **205 fichiers** dans le dépôt historique `Bobcribb/Mythos`, **3 106 fichiers** dans la branche active à l'instant de comparaison. Sur **14 anciens chemins non repris à l'identique**, il y a des workflows obsolètes, des anciens médias 2,5D à ne pas réintroduire, des anciens outils et un rapport technique historique ; **aucun manuscrit universitaire intégral non publié**. Les neuf monographies anciennes d'Aristophane, les compilations `Origines du sacré` et le dossier *La Galigo* ont déjà leur contenu dans le dépôt public. Un fichier `contenus/philosophie/homere-hesiode-dossier-preparatoire.md` existe, mais son texte se déclare expressément **plan de préparation, non monographies complètes, non page publiée**, avec bibliographie à compléter : il ne doit pas être présenté comme une nouvelle étude approuvée.

La file officielle comportait, au moment du contrôle, **264 demandes**, dont **258 attribuées**, **5 retenues** et **1 sans reçu**. Cette dernière est déjà sous un UUID unique ; son arrivée ne justifie aucune duplication. Le chapitre **420, Makaria**, se trouve déjà sur `main` avec son texte Markdown intégral et une page HTML. Son URL publique est accessible et son lecteur affiche **25 sections** jusqu'à la bibliographie et la conclusion. Il n'est pas comptabilisé comme une nouvelle importation.

**Bilan contenu nouveau : 0 manuscrit ajouté.** Blocage exact : aucune source publique complète, approuvée et actuellement non publiée n'a été identifiée dans les deux arbres historiques et actifs. Les 135 brouillons WordPress privés trouvés antérieurement ne sont pas assimilés à des textes validés, sans intervention manuelle. Ni réécriture ni publication artificielle n'a eu lieu.

## 2. Travail éditorial réel : réparer l'accès aux textes complets

Le générateur `scripts/build_greek_folders.py` avait un classement générique « Nouvelles études à classer » pour de nombreuses publications récentes pourtant documentées. Quatorze études **déjà numérotées et publiées** reçoivent désormais un classement primaire cohérent, selon leur sujet (jamais selon les seuls dieux mentionnés en passant) :

| Chapitre | Sujet vérifié | Famille principale |
| --- | --- | --- |
| 420 | Makaria et les Héraclides | Grandes familles mythologiques |
| 419 | Agdistis, Attis et la Phrygie | Divinités |
| 418 | Eunostos, héroon et interdit à Tanagra | Cultes et sanctuaires |
| 417 | Épiménide et purification d'Athènes | Cultes et sanctuaires |
| 416 | Eiresionè, fêtes et rameaux d'Apollon | Cultes et sanctuaires |
| 415 | Alastôr, vendetta et cycle des Atrides | Grandes familles mythologiques |
| 414 | Bendis et les cultes thraces au Pirée | Cultes et sanctuaires |
| 413 | Courètes et enfance de Zeus | Cosmogonies |
| 411 | Pothos, puissance du désir | Divinités |
| 410 | Télesphore et guérison | Cultes et sanctuaires |
| 409 | Agathos Daimôn et culte domestique | Cultes et sanctuaires |
| 408 | Asôpos, fleuve divin et ses descendants | Divinités |
| 407 | Cnossos, palais et contexte archéologique | Sources anciennes |
| 404 | Zeus Meilichios, épithète et rites | Cultes et sanctuaires |

Les dossiers ont déjà une navigation par rubriques, un sommaire ancré par sous-thème, des liens vers le texte complet et un fil d'Ariane réciproque sur chaque lecteur. Les nouvelles règles utilisent **ce système existant** et ne copient pas les chapitres. Le classement des textes inconnus reste dans la rubrique explicite à trier. L'ancienne entrée « Grande Encyclopédie » reste absente du menu.

Un défaut de conversion interne a été découvert par l'exécution des tests : le nouveau terme primaire `familles` n'était pas accepté par le dictionnaire de conversion des anciennes familles thématiques, d'où `KeyError: 'familles'`. La correction est ajoutée explicitement ; elle évite d'inventer une affiliation « Atrides » pour Makaria.

## 3. Présentation responsive et accessibilité

Le style muséal noir/ivoire/or et la bannière statue grecque/temple sont conservés. Dans le CSS généré **uniquement pour les huit dossiers grecs** :
- les boutons de sommaire des sous-dossiers disposent d'une hauteur tactile minimale de **44 px**, d'une taille de boîte explicite, de césures et d'un alignement stable ;
- les fils d'Ariane longs peuvent revenir à la ligne sans faire déborder le viewport ;
- les liens de sous-dossiers prennent toute la largeur sur smartphone ; la grille existante reste à **une colonne sous 700 px** et deux colonnes au-dessus.

Les huit couvertures documentaires et leurs crédits restent inchangés. Les anciennes illustrations vectorielles 2,5D ne sont pas restaurées.

## 4. Commits et vérifications

Commits de cette intervention :
- `dd316a3f121bfcc6501fb2d4f83f1638bd4dd138` — quatorze règles de classement vérifiées par sujet ;
- `f616c57914398228df9976beca4e171f1ef106ad` — test de présence des sources et du dossier primaire pour chaque chapitre ;
- `bcb99b48caf6ac07d839b7f058ed2bd1e480463d` — correctif responsive/tactile de la navigation ;
- `9297bd62f3ce4852e1ef227a5391d769055be09f` — correction du dictionnaire `familles` à la suite d'un vrai échec des tests GitHub Actions.

Après lecture sur `main`, le script modifié et le nouveau test sont présents avec les chemins attendus. Les **premiers workflows** déclenchés avant `9297bd62` ont effectivement échoué sur la nouvelle assertion `KeyError: 'familles'`. **Le verdict sur le commit corrigé est à contrôler** : les workflows `41902913993` (tests) et `41902914121` (publication) étaient respectivement en cours et en attente au dernier examen. Ne pas annoncer le déploiement avant succès et mise à jour du reçu.

Contrôle externe indépendant sur `https://bobmythos.fr/` : le reçu `/catalog/publication-verification.json` indique encore `source_commit=767359f8236fef3d221e3d3b9b1a49999581173f`, run `41896997055`, **1 382 entrées**, **27 archives**, **110 médias**. La page `/mythologie-grecque/dossiers/familles/` ne cite **pas encore Makaria**, mais la monographie `/chapitres/encyclopedie/chapitre-420-makaria-heraclides-sacrifice-volontaire-asile-athenes/` est publique. Cela distingue clairement **texte déjà disponible** et **nouveau classement pas encore déployé**.

Après publication : vérifier `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, puis vérifier les liens `dossiers/familles` ↔ `chapitre-420`, et les autres destinations/ancres, avec le reçu public correspondant au commit de build.

Aucun changement apporté aux workflows et horaires des autres automatisations MYTHOS, aux archives, numéros, notices ou manuscrits complets.
