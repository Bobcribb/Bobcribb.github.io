# Audit complet de MYTHOS — 4 novembre 2026

Le site répond, mais son bon fonctionnement HTTP ne suffit pas à valider ses liens internes, son iconographie et son contenu universitaire. Ce rapport distingue les corrections techniques vérifiées des travaux éditoriaux restant à réaliser.

## Bilan des liens contrôlés

| Contrôle | Relevé initial | Reconstruction corrigée |
|---|---:|---:|
| Références à des fichiers absents | 150 | 38 |
| Renvois vers des ancres absentes | 540 | 32 |
| Lecteurs HTML oubliés de la recherche | 20 | 0 |
| Pages comportant des identifiants dupliqués | 2 | 1 |

Ces valeurs comptent les occurrences, pas nécessairement des cibles distinctes. Les 38 références restantes concernent huit fichiers historiques réellement absents.

## Périmètre et preuves

- **1 104 adresses HTML publiques testées par GET : 1 104 réponses HTTP 200**  sans échec. Le fichier 404.html est exclu de ce total ; une URL volontairement absente renvoie bien 404.
- 224 ressources locales référencées testées par HEAD : quatre fichiers présents dans GitHub mais oubliés par la publication renvoyaient 404.
- Les domaines HTTP, www et bobcribb.github.io redirigent vers https://bobmythos.fr/ ; HTTPS est accessible.
- Après intégration des corrections : **1147 fichiers HTML analysés**, 1101 entrées de recherche, 54361 références internes inspectées.
- 27 tomes des Origines du sacré et 110 médias originaux contrôlés ; les tailles et empreintes SHA-256 des médias sont vérifiées.
- 31 tests de publication et 13 tests iconographiques réussis, dont les conflits Git concurrents, les attributions de numéro, la recherche, les ancres et les reconstructions répétées.
- Le contrôle graphique commun vérifie chaque page non redirigée ; cinq lecteurs historiques sont également contrôlés pour la conservation des paragraphes, tableaux et illustrations.
- Inspection directe dans le navigateur : accueil, recherche et étude philosophique de la Théogonie. Les vérifications publiques après déploiement sont consignées à la fin du rapport.

Le premier relevé correspond au commit `ba3e617730a6ec27129dab0560e817d3fbd13972`. Les corrections concurrentes de graphisme, de numérotation et de publication atomique ont été conservées ; la base d’intégration est `864dca672e13e1b58f91128b8f451cafc5c5c801`.

## Corrections de cet audit

1. **Recherche et sitemap** : les 20 lecteurs HTML autonomes initialement oubliés sont intégrés, dont les études de l’Iliade, de l’Odyssée et de la Théogonie et neuf dossiers de sites archéologiques. La récupération de cet index revalide désormais le cache HTTP à chaque ouverture.
2. **Bibliographies et sommaires** : les ancres documentaires échappées dans les manuscrits sont rétablies de manière limitée et sûre ; les intitulés de chapitres sont raccordés aux liens du sommaire.
3. **Archives grecques** : les liens relatifs qui visaient des fichiers supprimés de l’ancien export pointent vers les pages migrées existantes. Les ressources déjà liées du corpus (CSS et trois catalogues JSON notamment) sont désormais copiées dans le site.
4. **Théâtre** : suppression de l’accumulation de repères HTML vides identiques à chaque reconstruction ; correction de la fermeture des listes de 51 analyses.
5. **Iconographie** : vérification et conservation du nouveau sélecteur par sujet intégré en parallèle. Les deux galeries génériques sont remplacées par des documents choisis selon le titre et le sujet explicite de la page. Les images rédigées dans le texte éditorial sont conservées.
6. **Contrôle permanent** : l’audit examine maintenant tous les fichiers `.html`, les identifiants dupliqués et les liens avec fragments. L’ancien audit ne parcourait que les `index.html` et annonçait zéro avertissement malgré ces défauts.

## Corrections concurrentes vérifiées

Le nouveau graphisme commun (bannière, typographie et navigation), le sélecteur iconographique par sujet, les sommaires grecs complétés et le mécanisme de publication atomique ont été intégrés pendant cet audit. Ils sont préservés. La collision arrivée sur Protésilas / Lycurgue est réconciliée dans le dépôt : Protésilas est CCI (201), avec redirection de son ancienne adresse. Les anciennes études restent conservées.

| Collection | Études numérotées actives contrôlées | Dernier numéro |
|---|---:|---:|
| encyclopedie | 55 | 357 |
| tragedies | 102 | 201 |
| comparatif | 104 | 158 |
| comedies | 58 | 58 |
| origines-du-sacre | 148 | 598 |

**Aucun doublon actif de numéro** dans ces cinq collections. Les compléments et les archives historiques suivent leurs règles explicites ; les chevauchements de titres anciens ne sont pas interprétés comme des doublons canoniques.

## Travaux restant à réaliser

### 38 références à des ressources absentes dans les anciens livres

Les liens de navigation réparés ne recréent pas les fichiers qui manquent réellement. Les références ci-dessous se trouvent dans `/corpus/mythologie-grecque/archives/`. Il s’agit de huit chemins distincts : sept images et un script.

| Ressource relative absente | Occurrences |
|---|---:|
| `assets/img/olympiens.webp` | 2 |
| `assets/img/cycles.webp` | 9 |
| `assets/img/carte.webp` | 6 |
| `assets/img/heros.webp` | 2 |
| `assets/img/genealogie.webp` | 4 |
| `assets/app.js` | 13 |
| `assets/img/hero.webp` | 1 |
| `assets/img/tableau-dieux.webp` | 1 |

### 32 renvois internes sans cible vérifiable

Il reste notamment des renvois vers des identifiants de reconstitutions qui ne figurent pas dans la galerie actuellement publiée. Une page de redirection accessible ne prouve pas que le monument et l’image demandés existent à destination. Quelques ancres du glossaire et d’une archive de navigation sont également à reprendre.

| Page d’origine | Occurrences |
|---|---:|
| [/iliade/](https://bobmythos.fr/iliade/) | 1 |
| [/sites/dodone.html](https://bobmythos.fr/sites/dodone.html) | 3 |
| [/sites/nemee.html](https://bobmythos.fr/sites/nemee.html) | 3 |
| [/sites/corinthe.html](https://bobmythos.fr/sites/corinthe.html) | 3 |
| [/sites/bassae.html](https://bobmythos.fr/sites/bassae.html) | 4 |
| [/sites/egine-aphaia.html](https://bobmythos.fr/sites/egine-aphaia.html) | 2 |
| [/sites/brauron.html](https://bobmythos.fr/sites/brauron.html) | 4 |
| [/sites/sounion.html](https://bobmythos.fr/sites/sounion.html) | 2 |
| [/sites/messene.html](https://bobmythos.fr/sites/messene.html) | 4 |
| [/sites/delphes.html](https://bobmythos.fr/sites/delphes.html) | 2 |
| [/heracles/](https://bobmythos.fr/heracles/) | 3 |
| [/corpus/mythologie-grecque/archives/MYTHOS_bibliotheque_navigable.html](https://bobmythos.fr/corpus/mythologie-grecque/archives/MYTHOS_bibliotheque_navigable.html) | 1 |

### Grande compilation des Origines du sacré

`/corpus/origines-du-sacre/edition-integrale-tomes-I-XXVII.html` conserve des identifiants HTML répétés, notamment `ref-1` et `chap-1013`. Il faut les rendre propres à chaque tome et ajuster leurs renvois, pour qu’un clic atteigne la bonne référence dans cette compilation.

### Contenu universitaire et iconographie

- 18 manuscrits comptent moins de 300 mots bruts, dont 16 dans les Origines du sacré. Ce seuil signale une vérification éditoriale nécessaire ; il ne suffit pas, à lui seul, à juger un texte.
- Les trois études philosophiques sont présentes et illustrées. L’exigence de dix pages A4 par étude reste à mesurer par rendu paginé : le nombre de sections ne constitue pas cette preuve.
- Le nouveau sélecteur iconographique supprime les insertions génériques sans sujet explicite. La pertinence scientifique des illustrations éditoriales et des cartes de sommaire demande encore un contrôle article par article.
- L’exactitude de toutes les affirmations et des milliers de liens universitaires externes n’est pas certifiée par cet audit technique.
- Les règles CSS adaptatives sont présentes, mais aucun test sur le téléphone ou la tablette physique de l’utilisateur n’a été effectué.

### Structure et référencement à améliorer

- 632 pages ne déclarent pas de lien canonique. Ce constat ne signifie pas que leur contenu est inaccessible, mais leur métadonnée de référence peut être harmonisée.
- 137 pages contiennent plusieurs titres de niveau 1, souvent le titre de bannière puis le titre du texte. Une harmonisation de la hiérarchie faciliterait la navigation des lecteurs d’écran.

### Manuscrits courts à revoir

| Manuscrit | Mots bruts |
|---|---:|
| `chapitres/comedies/volume-002-eupolis-heilotes.md` | 159 |
| `chapitres/encyclopedie/chapitre-318-egee-voiles-noires.md` | 292 |
| `chapitres/origines-du-sacre/459-musique-grecque-mousike.md` | 172 |
| `chapitres/origines-du-sacre/460-choeurs-grecs-choreia.md` | 220 |
| `chapitres/origines-du-sacre/461-mesopotamie-lamentations-emesal.md` | 154 |
| `chapitres/origines-du-sacre/462-egypte-sistre-hathor.md` | 238 |
| `chapitres/origines-du-sacre/463-iran-inde-chant-liturgique.md` | 235 |
| `chapitres/origines-du-sacre/464-chine-rites-musique.md` | 212 |
| `chapitres/origines-du-sacre/465-afrique-ameriques-rythmes.md` | 268 |
| `chapitres/origines-du-sacre/466-philosophie-musique-sacree.md` | 299 |
| `chapitres/origines-du-sacre/467-temps-sacre-grece-calendriers.md` | 140 |
| `chapitres/origines-du-sacre/468-mesopotamie-akitu-annee.md` | 170 |
| `chapitres/origines-du-sacre/469-egypte-calendrier-sothis.md` | 207 |
| `chapitres/origines-du-sacre/470-iran-zoroastrisme-temps.md` | 181 |
| `chapitres/origines-du-sacre/471-inde-yuga-calendriers.md` | 180 |
| `chapitres/origines-du-sacre/472-chine-calendrier-mandat.md` | 194 |
| `chapitres/origines-du-sacre/473-ameriques-afrique-calendriers.md` | 260 |
| `chapitres/origines-du-sacre/474-philosophie-temps-sacre.md` | 261 |

## Reproduire les contrôles

```bash
python -m unittest discover -s tests -v
python scripts/editorial_queue.py check
python scripts/editorial_numbering.py scan
python -m unittest discover -s scripts -p test_editorial_illustrations.py -v
python scripts/build_native.py
python scripts/validate_publication.py
python scripts/verify_museum_design.py
python scripts/audit_integrity.py
```

Le résultat « core integrity: PASS » signifie que les contrôles bloquants passent. Il ne signifie pas que les avertissements éditoriaux et les ressources historiques manquantes ont disparu. Les détails structurés sont dans [audit-site-2026-11-04.json](audit-site-2026-11-04.json).

## Vérification publique après déploiement

Contrôles effectués le `2026-11-03T23:51:16.098361+00:00` (UTC). **35/35 contrôles ciblés réussis.**

Le [déploiement GitHub Actions](https://github.com/Bobcribb/Bobcribb.github.io/actions/runs/41742087357) a publié la source `a0d5b72a6e790cc1fdb7419d0b1ede732717b204`. La [preuve publique de publication](https://bobmythos.fr/catalog/publication-verification.json) confirme 1102 entrées de recherche, 27 tomes et 110 médias originaux contrôlés.

Le site a reçu une étude supplémentaire de Danaé, volume CCII (202), pendant cet audit. Le déploiement compte donc 514 manuscrits et 1 105 pages habillées, plus 43 redirections (1 148 fichiers HTML), contre 513 manuscrits et 1 147 fichiers dans la reconstruction locale détaillée ci-dessus. Le nouveau lecteur répond également HTTP 200.

Le catalogue public confirme désormais 103 tragédies numérotées, jusqu’au volume 202 ; les quatre autres collections conservent les totaux du tableau. Aucune collision active n’est signalée.

| Vérification ciblée | Résultat |
|---|---|
| HTTP /search.json | OK |
| HTTP /assets/search.js | OK |
| HTTP /chapitres/tragedies/volume-ccii-euripide-danae/ | OK |
| HTTP /catalog/publication-verification.json | OK |
| HTTP /catalog/numbering.json | OK |
| HTTP /corpus/theatre-grec/comedies/ploutos-protos-controle.json | OK |
| HTTP /corpus/theatre-grec/comedies/triphales-controle.json | OK |
| HTTP /corpus/reconstitutions-3d/catalogue.json | OK |
| HTTP /corpus/mythologie-grecque/archives/assets/style.css | OK |
| HTTP /chapitres/origines-du-sacre/archives-integrales/tome-xxiii/ | OK |
| HTTP /chapitres/origines-du-sacre/tome-xxxviii-chapitres-443-450/ | OK |
| HTTP /chapitres/origines-du-sacre/471-inde-yuga-calendriers/ | OK |
| HTTP /chapitres/origines-du-sacre/462-egypte-sistre-hathor/ | OK |
| HTTP /theatre-grec-conserve-etudes-philosophiques/ | OK |
| HTTP /philosophie-theogonie.html | OK |
| HTTP /chapitres/tragedies/volume-cci-euripide-protesilas/ | OK |
| HTTP /chapitres/tragedies/volume-clxxxviii-euripide-protesilas/ | OK |
| HTTP /corpus/mythologie-grecque/archives/bibliotheque.html | OK |
| HTTP / | OK |
| Index HTTP revalidé à chaque ouverture | OK |
| Recherche /philosophie-iliade.html | OK |
| Recherche /philosophie-odyssee.html | OK |
| Recherche /philosophie-theogonie.html | OK |
| Dossiers archéologiques recherchables | OK |
| /chapitres/origines-du-sacre/archives-integrales/tome-xxiii/#ref-1 | OK |
| /chapitres/origines-du-sacre/archives-integrales/tome-xxiii/#chap-853 | OK |
| /chapitres/origines-du-sacre/tome-xxxviii-chapitres-443-450/#chapitre-443 | OK |
| Repère des archives théâtrales unique | OK |
| Pas de Derveni hors sujet /chapitres/origines-du-sacre/471-inde-yuga-calendriers/ | OK |
| Pas de Derveni hors sujet /chapitres/origines-du-sacre/462-egypte-sistre-hathor/ | OK |
| Ancienne adresse Protésilas redirigée | OK |
| Lien archive vers école de Paris migré | OK |
| Habillage commun / | OK |
| Habillage commun /philosophie-theogonie.html | OK |
| Habillage commun /corpus/mythologie-grecque/archives/bibliotheque.html | OK |

Vérification dans le navigateur : la recherche « Théogonie » retourne six résultats, dont « PHILOSOPHIE DE LA THÉOGONIE ». Un clic ouvre bien https://bobmythos.fr/philosophie-theogonie.html ; son titre, son texte et la bannière commune sont visibles.

Les liens universitaires externes et chaque affirmation historique ne sont pas validés exhaustivement par ces contrôles techniques. Les anomalies historiques répertoriées plus haut restent ouvertes.
