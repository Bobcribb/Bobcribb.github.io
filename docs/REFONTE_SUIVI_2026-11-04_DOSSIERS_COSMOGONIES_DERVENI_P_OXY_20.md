# MYTHOS — Refonte : huit dossiers grecs illustrés, sans duplication éditoriale

**Contrôle du 4 novembre 2026.** Source de vérité : `Bobcribb/Bobcribb.github.io`, branche `main`. Tête d'ouverture : `595fb77afbd8f858815497f7c9c81abe263fc285`. Les deux protocoles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été intégralement lus avant toute modification.

## 1. Recherche de contenu universitaire public non encore intégré

L'arbre de `main` comportait **3 076 fichiers** au premier inventaire de cette séance. L'arbre historique public `Bobcribb/Mythos` comportait **205 fichiers**. La comparaison des chemins exacts relève **14 fichiers historiques non présents au même chemin** dans le dépôt actuel : 3 anciens workflows, 3 anciennes illustrations SVG, 2 anciens WebP, 1 ancien catalogue JSON photoréaliste, 1 notice JSON de reconstitution, 1 rapport technique et 3 anciens scripts ; **aucun manuscrit universitaire intégral** parmi ces 14 fichiers. Les anciens SVG 2,5D ont été supprimés volontairement et ne doivent pas être réimportés.

Parmi les **39 sources `.md` ou `.json` de `corpus/`** dans l'ancien dépôt, 38 chemins sont présents à l'identique ; le seul manquant au même chemin est la notice JSON de l'ancienne vue de Delphes, pas une étude littéraire ou philosophique. Le chapitre `corpus/origines-du-sacre/chapitre-487-iran-inde-mithra-rta-satya.md` a bien un équivalent numéroté et une page HTML dans le dépôt actif. Les anciens manuscrits universitaires d'Aristophane `Aiolosikon`, `Daidalos`, `Géras`, `Holkades`, `Kokalos`, `Lemniai`, `Ploutos protos`, `Polyidos` et `Triphales` ont des versions intégrales sous `chapitres/comedies/`, avec pages HTML et sources historiques conservées. Le texte de *La Galigo* dispose déjà d'une page autonome dans `bibliotheque-mythologies-du-monde/`.

Les 135 anciens brouillons WordPress retrouvés dans Google Drive conservent un statut privé ; ils ne sont **pas des manuscrits publics approuvés**. Ils ne sont donc pas soumis à `editorial/inbox/` et ne sont pas publiés sans validation éditoriale. Une soumission universitaire déjà présente dans la file n'est pas re-déposée sous un second UUID.

**Résultat pour cette intervention : 0 nouvelle monographie intégrale importée.** Le blocage précis est l'absence, dans les sources publiques inspectées, d'un texte intégral approuvé dont la publication manque et dont l'identité ne fait pas doublon. Aucun texte, notice, bibliographie, archive ni identifiant historique n'a été modifié pour satisfaire artificiellement cet objectif.

## 2. Amélioration graphique et documentaire réellement effectuée

La navigation de l'**Encyclopédie grecque**, `/mythologie-grecque/`, distribue déjà l'intégralité des entrées entre **huit dossiers thématiques**, avec liens vers les pages universitaires et leurs sections. Sept cartes disposaient d'une photographie antique contextualisée et d'un crédit. La huitième, **Cosmogonies**, restait sans document iconographique.

Le papyrus de **Derveni** est un **témoin matériel d'un commentaire antique à une théogonie orphique**. Il est pertinent pour ce dossier, mais ne représente aucune scène visuelle de la création. Son image d'archive, déjà présente et déclarée dans `scripts/editorial_media.json`, est utilisée **sans modification de pixels**, avec `alt`, identification du document, musée, auteur de la photographie, licence et lien institutionnel ou vers la source iconographique. Elle apparaît dans la carte Cosmogonies. Le renvoi demeure `/mythologie-grecque/dossiers/cosmogonies/`.

Pour conserver **une image distincte par dossier**, la carte **Sources anciennes** utilise dorénavant la photographie documentaire de **P.Oxy. 20**, témoin de l’*Iliade* II et de sa transmission, déjà archivé sous `media/2026/10/mythos-papyrus-oxyrhynchus-20-iliade-ii.jpg`. La légende distingue l'œuvre d'Homère, le papyrus et la photographie et mentionne sa provenance de reproduction. Le renvoi demeure `/mythologie-grecque/dossiers/sources-anciennes/`. Les six autres cartes, les notices, les sources et les textes demeurent inchangés.

Le générateur `scripts/build_greek_folders.py` utilise désormais ces deux choix explicitement documentés ; ils sont vérifiés par les métadonnées de provenance et par l'existence physique des fichiers, avec refus de la construction si une photographie ou sa source est absente. Les deux cartes HTML du portail ont été actualisées immédiatement pour correspondre au futur rendu autonome. Aucune illustration 2,5D n'a été réintroduite.

Le design noir/ivoire/or, la bannière grecque, le sommaire, les huit dossiers, les liens réciproques et le lecteur des chapitres sont conservés. Les cartes utilisent toujours la grille responsive existante : deux colonnes sur ordinateur, une colonne sous 700 px, photographie à cadrage fluide et crédit dépliable **hors du lien de navigation**.

## 3. Contrôle de non-régression

`tests/test_greek_folder_media.py` vérifie désormais les **huit** affectations exclusives, leur présence dans le registre et sur le disque, les crédits avec liens externes et la restitution des huit images différentes dans la page produite. Le test de reconstruction partielle avec un dossier dépourvu d'image reste possible en fournissant volontairement une seule fixture ; les protections contre une photographie inexistante continuent de s'appliquer.

Vérification après écriture sur `main` : le HTML du portail contient les deux nouveaux `src`, les deux descriptions `alt` et les liens de provenance correspondants. La suite GitHub Actions de la dernière révision était **en cours** au dernier relevé, sans conclusion finale ; la conformité globale n'est pas présumée. Le reçu public `catalog/publication-verification.json` accessible à cette étape affichait encore `source_commit=68f6851073554c2fe66ef143838610ba6961404b`, `github_run_id=41884447199`, **1 371 documents**, **27 archives**, **110 médias**. Le domaine public présentait encore l'ancienne carte Cosmogonies sans photo : **publication publique de ces modifications non encore confirmée**.

Contrôles requis après la prochaine publication réussie : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, contrôle des huit images et liens de provenance sur `https://bobmythos.fr/mythologie-grecque/`, puis comparaison du `source_commit` dans le reçu public.

## 4. Commits enregistrés

- `edcef5dd9b81695d52898fa75855a675dcb64819` : correction durable de la sélection documentaire des huit dossiers.
- `902fc7ea05137ed85394b502369f6031cf74fc6e` : vérification des sources et de la non-duplication des objets.
- `b69c2adebd19efb2641a05f0c03aea6ec3e4456b` : carte Cosmogonies avec photographie et crédit de Derveni.
- `23346f11b0315946bd96c97768a07d8e4d399cb8` : carte Sources anciennes avec photographie et crédit de P.Oxy. 20.
- `96dabffe3153909a4d20c4851ad2c9520183f482` et `5bb32ffeb5fcd02d671d0e868f485f2f1087aa63` : test supplémentaire de rendu et contrôle portable de la provenance.

**Éléments protégés** : textes universitaires, bibliographies et archives ; numéros et registre `editorial/numbering.json` ; `editorial/inbox/` et reçus ; workflows ; horaires des automatisations parallèles ; identité muséale existante.
