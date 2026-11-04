# MYTHOS — Refonte du 4 novembre 2026 : garde de la photographie de Troie et vérification éditoriale

## État contrôlé

Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`. À l'ouverture de la séance, tête `02bb70899ed74b660d9270f7ebf2664a3904db96`. Le fichier `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus intégralement avant toute écriture. Les cinq séries numérotées sont exclusivement attribuées par les reçus de la file `editorial/inbox/` ; aucun numéro et aucun registre n'ont été modifiés.

### 1. Sources universitaires vérifiées et intégrations

À la photographie initiale de `main`, `editorial/inbox/` contenait **253 demandes** : **247 attribuées**, **5 retenues explicitement** et **1 soumission encore sans reçu**. La dernière est `ae7e3d21-8b92-47ce-a9d3-15e4bc70f621`, étude publique intégrale de **9 285 caractères** sur **Makaria (Héraclides, sacrifice volontaire et Athènes)**, collection `encyclopedie`, slug `makaria-heraclides-sacrifice-volontaire-asile-athenes` et cote provisoire `{{numero}}`. Ce manuscrit existe **déjà** dans `editorial/inbox/`, et doit être attribué et publié par GitHub Actions. Aucun second UUID n'est créé pour lui.

Autres sources inspectées :
- dépôt historique `Bobcribb/Mythos`, branche `main` : environ 205 fichiers visibles dans son arbre, dont les anciennes études, les neuf dossiers d'Aristophane et les compilations des *Origines du sacré* ; ces dossiers sont déjà reproduits ou reliés dans le dépôt actif. Leurs numéros et archives sont conservés.
- bibliothèque de fichiers de travail : les premières compilations cumulatives des *Origines du sacré* (notamment tomes I–XVII), déjà dépassées par les 27 tomes préservés dans le dépôt public ; ces fichiers ne constituent pas une nouvelle livraison indépendante.
- sauvegardes Google Drive des 135 anciens brouillons WordPress : elles restent expressément privées ; elles ne sont pas importées automatiquement.

**Nouveau manuscrit universitaire intégral déposé pendant cette intervention : aucun.** Aucun texte intégral inédit, approuvé, disponible et clairement absent du circuit de publication n'a été trouvé parmi ces sources inspectées. Les seuls candidats immédiats sont déjà soumis, déjà accessibles ou privés. Ne pas les dupliquer, tronquer ou remplacer par un résumé.

### 2. Défaillance réelle et correction

L'inspection des logs de la publication GitHub Actions **41887210750** montre deux tests défaillants dans `tests/test_home_eneide_cards.py`, tous deux liés à un texte alternatif vide (`alt=""`) sur la photographie de Troie dans la carte de l’*Énéide*. Le récit universitaire n'était pas perdu : la défaillance concerne la régénération du HTML de l'accueil.

Corrections déposées sur `main` :
1. `scripts/apply_museum_design.py` restaure explicitement le texte alternatif **« Vestiges de Troie VI à Hisarlik : contexte archéologique, non illustration du récit virgilien. »** à chaque passe, après vérification de la présence de la photographie locale authentifiée ; le mécanisme évite d'attribuer au monument réel une scène inventée de Virgile.
2. `index.html` reçoit le même `alt` sur la carte publique d'accès au lecteur intégral existant `/philosophie-eneide.html` ; aucune autre carte ni étude n'est modifiée.
3. `tests/test_home_eneide_cards.py` ajoute un test volontairement régressif : il simule `alt=""` dans la page, reconstruit deux fois puis exige la restauration de la légende et du chemin documentaire.

Ces changements conservent la maquette noir, ivoire et or, la bannière statue grecque/temple, les quatre cartes philosophiques et leur grille responsive, la source des 18 sections de l’*Énéide*, les notes et la bibliographie.

### 3. Commits de cette exécution

- `046474677d42d45eb220ffd073d38e3fc40d7636` : correctif durable du générateur muséal.
- `b12b8b1559e48ca3608ebdcf10997710d1cea98e` : restauration du `alt` dans le HTML d'accueil.
- `2ebbde266383e609438d7dfb07668e8665bf903d` : test de non-régression de la légende.

### 4. Contrôles et publication publique

Relecture GitHub des fichiers modifiés : les deux occurrences attendues du texte alternatif ont été retrouvées ; le test supplémentaire est présent sur `main`. Les tests automatiques de la dernière révision étaient **en cours** au dernier contrôle ; ne pas déclarer la suite complète réussie avant sa conclusion.

Vérification HTTPS indépendante :
- `https://bobmythos.fr/catalog/publication-verification.json` publie **`source_commit=68f6851073554c2fe66ef143838610ba6961404b`**, run **41884447199**, **1 371 documents**, **27 archives**, **110 médias** ;
- la page d’accueil publique contient déjà « **Quatre œuvres à approfondir** » et les quatre liens Iliade, Odyssée, Théogonie, Énéide ;
- cette version publique comporte toujours `alt=""` pour l'image de Troie : **la correction de cette séance est enregistrée sur `main`, mais son déploiement public n'est pas encore confirmé**.

Contrôles à répéter après une exécution réussie : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, reçu public à jour et vérification HTML de `#home-oeuvres a[href="/philosophie-eneide.html"] img[alt]`.

**Aucune modification** des manuscrits et archives, des registres d'attribution, de `.github/workflows/`, des autres automatisations MYTHOS ni de leurs horaires.
