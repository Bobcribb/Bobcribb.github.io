# MYTHOS — refonte : hiérarchie documentaire, sommaires et état de publication
Date du contrôle : 4 novembre 2026 (matin, Europe/Paris).

## Source de vérité et garde de numérotation

Dépôt canonique : `Bobcribb/Bobcribb.github.io`, branche `main`.
Les règles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relues avant écriture.
État consulté avant les correctifs : `d50b025b0c6688bafeb872bb6750e04f2681c29f`; les correctifs ont été committés sur les nouvelles têtes lues juste avant chaque transaction.

Aucun numéro éditorial n’a été attribué ou réservé, aucun fichier numéroté n’a été créé directement dans `chapitres/`, aucun registre de numérotation, workflow ni planification horaire n’a été modifié.

## Contenus universitaires intégrés et blocage

**Nouvelle étude intégrale importée par cette intervention : aucune.**
Lors du contrôle ciblé de la file sur `main`, `editorial/inbox/` contenait **93 demandes** et le registre `editorial/numbering.json` comportait **93 reçus d’attribution**, soit **0 demande non attribuée à cet instant**. Les manuscrits de ces demandes ne doivent pas être soumis à nouveau sous un UUID différent.

La recherche précédente dans l’ancien dépôt `Bobcribb/Mythos` (204 fichiers) n’avait pas identifié de manuscrit universitaire inédit intégral en dehors des textes déjà transférés ; les anciens manuscrits cités comme manquants, notamment Chiron (118–133) et la séquence historique Nyx–Hypnos (218–224), n’ont pas été retrouvés en version intégrale approuvée. Une notice ou un sommaire ne constitue pas un texte scientifique publiable. Aucun substitut, reconstruction par conjecture ou résumé n’a été inséré.

**Vigilance sur la duplication historique MC-025 :** trois fichiers distincts et des reçus distincts portent sur Maât et Isfet :
- Volume CLXXXIII (183) : `chapitres/comparatif/volume-clxxxiii-maat-isfet-justice-verite-ordre-cosmique-desordre-egypte.md`.
- Volume CLXXXVII (187) : `chapitres/comparatif/volume-clxxxvii-maat-isfet-verite-justice-ordre-cosmique-egypte.md`.
- Volume CLXXXIX (189) : `chapitres/comparatif/volume-clxxxix-mc-025-maat-isfet-justice-verite-desordre-egypte-ancienne.md`.

Il s’agit d’une **redondance thématique à collationner**, non d’une preuve d’identité mot à mot. Il ne faut ni effacer ces textes, ni renuméroter arbitrairement ces attributions ; conserver les trois versions et leurs sources jusqu’à examen philologique.

## Corrections concrètes et traçabilité

1. **Hiérarchie de lecture universelle** — commit `6e2609c7540346b87436c12aa06afc5c8b4ef9a9` :
   - `scripts/apply_museum_design.py` réserve `h1` au titre du bandeau commun et transforme les autres titres `h1` de l’article en `h2` sans altérer leurs textes, identifiants HTML, liens ni bibliographies.
   - Le lecteur public de Phèmè, étude 388, illustrait le défaut avec deux `h1` dans son HTML.
   - `tests/test_museum_hierarchy.py` introduit deux tests de reconstruction répétée, préservation des renvois et non-modification des redirections.

2. **Grande Encyclopédie, sommaires numérotés** — commit `c5f9f2bf336b7c7cdde39c740552d9aea71edbaa` :
   - `scripts/build_navigation.py` corrige deux fins de listes `</ul>` incorrectes qui fermaient des listes `<ol>` dans le sommaire des collections et les listes de notices.
   - `tests/test_encyclopedia_markup.py` vérifie les six collections, les liens, l'unicité des cotes de registre et le refus des URL répétées.
   - Les sources universitaires originales, archives, bibliographies et images demeurent inchangées.

Le style musée noir et or, la bannière statue grecque / temple, les images photoréalistes attestées et les règles responsive ont été conservés. Aucune illustration 2,5D n'a été réintroduite.

## Résultat public et limites de preuve

La preuve publique `https://bobmythos.fr/catalog/publication-verification.json` consultée pendant l’intervention donnait :
- source `4b4ac0753f8243f6ddd1d3b36acbba32491671c7` ;
- déploiement GitHub Actions **41790851372**, terminé avec succès ;
- **1 205 documents indexés**, **27 tomes** et **110 médias** vérifiés.

Le chapitre 388 sur Phèmè répondait en HTTPS avec un texte universitaire de plus de 40 000 caractères, son sommaire et ses sources. Les illustrations antérieurement ajoutées aux cartes des parcours et aux trois études philosophiques étaient désormais servies depuis le domaine public.

Ces preuves concernent **le déploiement antérieur**. Au dernier contrôle effectué lors de cette intervention, les workflows de validation et de publication propres aux deux nouveaux commits étaient encore en cours ou en attente. Leur exécution réussie et leur présence sur le site public **ne sont pas affirmées avant vérification**.

## Contrôle avant clôture technique

- `python -m unittest discover -s tests -v` ;
- `python scripts/build_native.py` ;
- `python scripts/verify_publication.py` ;
- `python scripts/verify_museum_design.py` ;
- vérifier ensuite le workflow de publication le plus récent et le contenu HTML public, notamment `/chapitres/encyclopedie/chapitre-388-pheme-rumeur-renommee-athenes-aeschine-demosthene/` et `/grande-encyclopedie/`.

La conservation des textes et le principe d'attribution atomique restent prioritaires sur la cadence des ajouts.

## Addendum — collision de deux générateurs et résolution

Le premier jeu de tests sur `c5f9f2bf336b7c7cdde39c740552d9aea71edbaa` a révélé une collision préexistante de fonctions : deux définitions de `create_encyclopedia(entries)` coexistaient dans `scripts/build_navigation.py`. La seconde masquait le registre à six rubriques, de sorte que les assertions destinées à ce registre portaient sur le portail grec sommaire. Cette cause a été constatée dans les journaux de l'exécution GitHub Actions [41792542527](https://github.com/Bobcribb/Bobcribb.github.io/actions/runs/41792542527), terminée en échec à cause de **deux nouveaux tests**. Ces échecs n'étaient pas dus au contenu universitaire et ne justifient aucune suppression.

**Correction réelle enregistrée : commit `ad9b2249bc0b3d25f887827a961d5ea265d6f8c0`.**
- Renommage du générateur jusque-là masqué en `create_encyclopedia_registry(entries)`.
- Production de la page distincte `/grande-encyclopedie/registre-integral/` référençant les pages existantes des six collections, sans reproduire leurs textes.
- Conservation du portail `/grande-encyclopedie/` et ajout d'un lien réciproque d'accès au registre intégral.
- Correction de la documentation descriptive sur les tomes déjà publiés, sans toucher aux manuscrits.
- Trois tests du registre : listes ordonnées bien fermées, refus des URL répétées, navigation entre portail et registre.

Sur l'exécution [41792957943](https://github.com/Bobcribb/Bobcribb.github.io/actions/runs/41792957943), les étapes « Tester les attributions concurrentes et les reprises » et « Vérifier la pertinence et la conservation des illustrations » ont été **réussies** au contrôle effectué ; la génération complète était encore en cours.

L'adresse publique de ce nouveau registre ne doit pas être annoncée comme déployée avant l'exécution réussie de la chaîne de publication et une requête HTTPS.
