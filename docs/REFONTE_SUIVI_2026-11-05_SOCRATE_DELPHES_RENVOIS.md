# MYTHOS — Rattacher le mémoire de Socrate aux dossiers grecs et créer le parcours delphique

**Séance : 5 novembre 2026.** Dépôt de publication : `Bobcribb/Bobcribb.github.io`, `main`. Tête à l'ouverture : `8208672276dbf47b56b09bc7618628cc9ad269d2`. `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus sur cette branche avant toute modification.

## 1. Inventaire éditorial, absence de nouveau manuscrit à soumettre

Au contrôle initial du circuit canonique, **306** fichiers JSON distincts dans `editorial/inbox/` ; **301** demandes avec allocation dans `editorial/numbering.json` (62 *Origines du sacré*, 70 *Encyclopédie*, 43 *Comédies*, 43 *Tragédies*, 83 *Comparatif*) et **5** demandes explicitement retenues avec empreinte et motif dans `editorial/holds.json`. **Aucune demande non attribuée et non retenue.** Le décompte est fondé sur les UUID effectivement présents, non sur une annonce de prochain numéro.

Arbre de l'ancien dépôt public `Bobcribb/Mythos` : **37 fichiers Markdown** ; **36** ont une adresse de même nom dans le dépôt actif. L'unique chemin non repris à l'identique, `docs/etat-publication-images-3d.md`, est une **note technique de suivi 3D** (5 325 octets), pas une monographie scientifique intégrale à publier. Les compilations anciennes et les pièces d'Aristophane possèdent leurs adresses de consultation dans le dépôt actif. Aucun manuscrit public, complet, approuvé et extérieur au circuit actuel n'a donc été identifié dans ce périmètre.

**Nouveau texte universitaire intégral importé : aucun.** Les archives et les brouillons privés ne sont pas publiés par supposition. **Nouvel UUID et nouveau numéro : aucun.** Cette intervention travaille sur un texte complet **déjà publié**, mais absent de la navigation thématique grecque, ce qui constitue une amélioration documentaire vérifiable sans copie.

## 2. Source intégrale vérifiée et dossier thématique créé

Le manuscrit hors des cinq collections numérotées `chapitres/philosophie/socrate-oracle-delphes-paradoxe-sagesse.md` est **déjà publié** à `/chapitres/philosophie/socrate-oracle-delphes-paradoxe-sagesse/` avec sa cote indépendante **PHY-SOC-2026-01**. Relecture : **96 556 caractères** UTF-8 décodés, six parties, conclusion, bibliographie commentée, quatre annexes et avertissements sur le statut du travail universitaire et des traductions. Son PDF source de 30 pages est conservé dans `assets/philosophie/socrate-oracle-delphes-paradoxe-sagesse-2026.pdf` (512 110 octets dans l'arbre Git). Blob du manuscrit au contrôle : `67c79e82531c09337ee0f238d894569f2d46b994`.

Jusqu'ici, cette étude figurait déjà dans la bibliothèque de philosophie et dans son propre lecteur, mais **pas** dans le sous-dossier grec « Interprétations philosophiques ». Elle a maintenant une entrée de source dans `scripts/build_greek_corpus.py`, et une affectation explicite, sans équivoque cultuelle, vers **Interprétations philosophiques → Socrate — oracle, enquête et sagesse** dans `scripts/build_greek_folders.py`. Ce sont des liens vers le mémoire *intégral existant*, pas une transcription abrégée.

## 3. Parcours réciproque « Delphes : textes, oracle et connaissance de soi »

Trois lecteurs complets déjà accessibles et vérifiés :

1. `/chapitres/philosophie/socrate-oracle-delphes-paradoxe-sagesse/` — **PHY-SOC-2026-01**, mémoire de philosophie (Platon, Xénophon, réfutation et sagesse).
2. `/chapitres/encyclopedie/chapitre-348-pythie-delphes-parole-inspiree/` — **chapitre 348**, 15 174 caractères de Markdown source, pratiques de consultation, autorité et témoignages ; blob `d47df62c9b940c36a58abc4af5fcae1df787239d`.
3. `/chapitres/encyclopedie/chapitre-349-maximes-delphiques-connais-toi-toi-meme/` — **chapitre 349**, 14 645 caractères de source, maximes, inscriptions et interprétations ; blob `6bbeb2c92e3941e7b02d7e475eea1585ad173177`.

Le générateur construit **un panneau de deux liens réciproques par lecteur**, en dehors de l'élément `article` qui contient le texte scientifique. L'appareil critique et les identifiants restent intacts. Le panneau distingue explicitement l'institution de l'oracle de sa réélaboration philosophique : il n'invente pas une continuité rituelle ni une équivalence entre les trois sources.

Les panneaux sont retirés puis reconstruits à chaque génération ; aucun doublon n'est créé lors d'une seconde passe. La rubrique grecque contient une **seule** destination principale pour chaque œuvre.

## 4. Graphisme et ergonomie

Conservation de l'identité muséale existante : fond anthracite, caractères ivoire/or, bannière statue grecque à gauche et temple à droite, cartes et crédits photographiques ; ni ancien SVG 2,5D, ni visuel historique inventé. Le parcours delphique réutilise les cartes documentaires de `assets/mythos-museum.css` en grille **deux colonnes**, puis **une colonne sous 700 px** ; cibles tactiles d'au moins **44 px**, liens longs repliables, focus clavier visible. Nouvelle variante sobre : accent latéral or, filet de titre, fond sombre en dégradé et marges adaptées sous **480 px**.

Aucune image source, métadonnée iconographique ou bibliographie n'a été remplacée.

## 5. Commits enregistrés sur `main`

- `26805c70da71977c7f777ea0a7cbd27a1a9963ad` : mémoire intégral de Socrate ajouté aux sources de navigation du corpus grec.
- `0de1a37587ac68572a478b6c804bfaddd688d211` : classification et liens Delphes–Socrate–maximes dans le générateur.
- `4900d79a3bf0e1c4567c540bf826d60722d26943` : tests de conservation, classification, deux liens réciproques, idempotence et présence de la source PDF.
- `749a2620b419f0819c96b037e93e2b2a8add48b4` : variante noir/or responsive du panneau Delphes.
- `65d753091ef3e0f3a90a11dec258e999a5148bbe` : test de garde du style mobile.

## 6. Vérification GitHub et limite du déploiement

À la vérification initiale du domaine public, `https://bobmythos.fr/catalog/publication-verification.json` renvoyait `source_commit=7310586e543b9b32b493d1fda3b0cc844f6c121e`, exécution **41955356964** (succès), **1 425 documents indexés**, **27 archives** et **110 médias**. Le mémoire de Socrate est déjà lisible sur sa page d'origine, mais le sous-dossier `/mythologie-grecque/dossiers/interpretations-philosophiques/` **ne l'énumérait pas encore** et aucun panneau Delphes n'était visible à cette version.

Les workflows de vérification de l'éditeur et de reconstruction étaient encore **en cours ou en attente** au dernier contrôle des nouveaux commits. Les ajouts sont confirmés sur GitHub, **pas encore confirmés sur le site HTTPS**. Avant toute déclaration de publication, vérifier le succès des tests et de la reconstruction, la progression du reçu public, l'entrée Socrate dans le sous-dossier, les trois panneaux réciproques, et l'intégrité des trois lecteurs et du PDF.

Contrôles du dépôt : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`. Cette séance ne modifie ni les workflows GitHub, ni les allocations numérotées, ni aucun manuscrit source, ni les horaires des autres automatisations MYTHOS.
