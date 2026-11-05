# MYTHOS — Réconciliation documentaire : Lydie, Phrygie, Thrace et Séleucides

**Date du contrôle : 5 novembre 2026, 06 h 52–07 h 00 UTC.**
**Dépôt :** `Bobcribb/Bobcribb.github.io`, branche `main`.
Référence initiale lue sur `main` : `58079282f2010e33ec7e9aa75a217c7bbc4846e2`.

## 1. Garde éditoriale et recherche de textes intégraux

`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus **avant les modifications**. Le registre `editorial/numbering.json`, `editorial/holds.json`, la file `editorial/inbox/`, les sources archivées publiques et les références Google Drive accessibles ont été examinés. À la lecture : **330 demandes JSON**, **325 allocations** (70 Origines du sacré, 74 Encyclopédie, 47 Comédies, 47 Tragédies, 87 Comparatif), **5 retenues pour collisions éditoriales** explicitement documentées. Aucune de ces cinq retenues ne doit recevoir un nouveau numéro ou un UUID de substitution.

Google Drive répertorie quinze volumes de sauvegarde des 135 anciens brouillons WordPress : ces documents sont des sauvegardes privées et ne valent pas autorisation de publication. Les autres mémoires universitaires identifiés, La Galigo et l'Horizon d'Aton notamment, sont déjà restaurés ou attribués dans le dépôt. L'ancien dépôt a été confronté au dépôt actif dans les rapports de réconciliation antérieurs. **Aucune nouvelle source universitaire intégrale, absente du site et explicitement approuvée pour publication, n'a pu être établie dans les sources examinées.** Aucune insertion dans `editorial/inbox/`, aucune attribution manuelle ni nouvelle première publication ne sont donc revendiquées.

## 2. Quatre textes universitaires complets retrouvés, déjà accessibles dans Civilisations

Les quatre pages HTML contiennent leurs développements, sections, sources et appareils bibliographiques. Elles étaient absentes des destinations `RELATED` de `scripts/build_greek_corpus.py` avant la modification et sont désormais **référencées dans l'encyclopédie grecque**, sans copie ni altération de leur manuscrit. Leur statut est *nouveaux rattachements au catalogue grec*, et non *premières publications*.

| Étude intégrale | Chemin historique conservé | Blob Git original | Famille grecque |
|---|---|---|---|
| Lydie, Sardes et Crésus | `/bibliotheque-mythologies-du-monde/civilisations-lydie-sardes-cresus/` | `012133f15c0898230a1a49fe08567b5ecf325499` | Sources anciennes : Hérodote, monnaies et histoire lydienne |
| Phrygie, Midas et Gordion | `/bibliotheque-mythologies-du-monde/civilisations-phrygie-midas-gordion/` | `2147651f1b703a1393acc1d29ab2a27e2e16a559` | Cultes et sanctuaires : Gordion, Matar et récits de Midas |
| Thraces, Odryses et Kazanlak | `/bibliotheque-mythologies-du-monde/civilisations-thraces-odryses-kazanlak/` | `e97f2a054f2b6d4b07f254d59627f95796d80fc6` | Cultes et sanctuaires : rites funéraires et royaumes thraces |
| Empire séleucide, Séleucos et Antiochos | `/bibliotheque-mythologies-du-monde/civilisations-empire-seleucide-antiochos/` | `458ddea0c3b364a12ebafd9294c5e62d8fff6994` | Sources anciennes : cités, chroniques et inscriptions |

Longueurs HTML vérifiées avant et après référencement : **26 597**, **31 157**, **12 551** et **25 929** caractères. Tous comportent un `article.content`, des sous-sections et des références documentaires. Les quatre blobs Git d'origine sont préservés ; les noms des fichiers et leurs URL n'ont pas été modifiés. Les sources archéologiques et historiques ne sont pas converties en synthèses ou en reconstitutions imaginaires.

## 3. Navigation, graphisme et préservation

- `scripts/build_greek_corpus.py` : quatre URL ajoutées une seule fois à `RELATED` pour assurer leur découverte et leur classement.
- `scripts/build_greek_folders.py` : sous-dossiers thématiques précis, fil d'Ariane et panneaux `frontieres` comportant trois liens vers les autres études, **douze renvois réciproques** dans le groupe de quatre. Les panneaux demeurent *hors du bloc universitaire `article`*. Une garde dans `verify` rejette les panels manquants, répétés ou non réciproques.
- `assets/mythos-museum.css` : déclinaison noir/ivoire/or des panneaux, focus et liens tactiles communs, colonnes adaptatives et traitement typographique à 700 et 480 px. La bannière grecque statue/temple, les huit familles thématiques, les illustrations documentées et les crédits archéologiques demeurent en place. Aucun SVG 2,5D ne revient.
- `tests/test_greek_anatolia_thrace_references.py` : contrôle des quatre sources réelles, de leurs bibliographies, de l'unicité du référencement, des familles, de l'intégrité du bloc `article`, des douze liens, de l'absence de doublons après deux reconstructions et des styles mobile.

Les périodes et les cultures ne sont pas artificiellement assimilées : les récits grecs sur la Lydie, la Phrygie et la Thrace ne documentent pas directement toutes leurs pratiques, et les Séleucides appartiennent à une période ultérieure. Le nouveau parcours explicite cette différence.

## 4. Commits effectivement écrits

1. `8d3c8466255df5d218f2497edfea4f489d00630e` — quatre titres intégrés au catalogue grec.
2. `a152ae43372a0fcb65f326231cfeedb605a942ad` — classement en dossiers, fil d'Ariane, renvois et vérifications.
3. `4cd9c5b146ce41e9856c1cffca16fbb382ef591c` — CSS muséal responsive.
4. `8b1b03eafa75c989dd9073ce0885396b5e430caf` — tests d'intégrité et d'idempotence.

## 5. État des validations, à distinguer de la publication

Les modifications sont lues dans `main`. Le workflow `Valider le générateur autonome MYTHOS` n° **41984045186**, déclenché par le commit des tests, a franchi les premières étapes et était en **génération** au dernier contrôle ; il n'est pas présenté comme terminé. L'exécution de publication n° **41983976847** était encore en attente. Les exécutions de publication antérieures remplacées par des commits plus récents étaient annulées, ce qui ne constitue pas un déploiement réussi.

Le dernier reçu `catalog/publication-verification.json` visible sur `main` mentionnait une version *antérieure* : `source_commit=927bd996b4f10a08246209df1b189a7dcd59a0c5`, **1 449 documents**, **27 archives**, **110 médias**, exécution `41981406624`. L'accès HTTPS direct à `bobmythos.fr` via la recherche externe a échoué lors du contrôle. **Le classement nouveau et les panneaux ne sont pas encore vérifiés en production : aucune annonce de déploiement confirmé.**

Aucun registre de numérotation, manuscrit original, archive, workflow, planification horaire ou autre automatisation MYTHOS n'a été modifié.
