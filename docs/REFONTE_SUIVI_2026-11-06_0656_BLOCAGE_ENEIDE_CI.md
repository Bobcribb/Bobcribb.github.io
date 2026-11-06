# MYTHOS — Refonte du 6 novembre 2026 : réparer la publication des sources de l’Énéide

## Périmètre et règles

Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`. Les fichiers `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, `EDITORIAL_CONTINUITY.md`, le registre `editorial/numbering.json`, les archives et les statuts `editorial/holds.json` ont été relus. La maquette noir et or et sa bannière statue grecque / temple, les manuscrits historiques, les numéros canoniques, les archives et les autres automatisations sont préservés.

## Cause déterminante vérifiée

GitHub Actions `42171076793` (validation sur PR), `42170724021` (validation de `main`) et `42170723991` (déploiement) étaient en échec avant cette réparation.

- Deux tests `tests/test_eneide_source_access_20261106.py` échouaient : le sélecteur `section > h2[id^=eneide-]` trouvait **19** titres au lieu de 18, parce que le titre technique du nouveau panneau partageait accidentellement le préfixe des dix-huit chapitres ; et la sérialisation BeautifulSoup ajoutait un saut de ligne à chaque cycle devant `html`, rendant les liens non idempotents.
- Le générateur public s'arrêtait dans `scripts/eneide_source_access.py`, `RuntimeError: MYTHOS : titre du récit d'Énée absent`. Le titre `h1` figure effectivement **dans la bannière muséale**, hors du `main article.content`. Le premier titre interne du récit est un `h2`. Le code cherchait exclusivement un `h1` dans l'article : la condition était trop restrictive.
- Le déploiement étant interrompu avant la reconstruction, l'export direct des 18 sources complètes de `corpus/philosophie/eneide/` n'était pas accessible sur le domaine public. Contrôle HTTPS indépendant : `/corpus/philosophie/eneide/00-introduction.md` renvoyait **404**, et le manifeste public affichait toujours `source_commit=00c888fd4b1f2d9a83beb82c40012f2eceb562a4` (`github_run_id=42163598977`), antérieur à cette réparation.

## Corrections enregistrées

Dans `scripts/eneide_source_access.py` : (1) le titre technique utilise `sources-eneide-heading` et ne fausse plus le décompte universitaire ; (2) les liens vers l'étude et le récit sont insérés après le `h1` interne quand il existe, ou avant le `h2` de la première section quand le `h1` est, comme en production, dans la bannière ; (3) le DOCTYPE est sérialisé de façon stable à chaque reconstruction. Le contenu des 18 Markdown est toujours copié **octet pour octet** ; aucun paragraphe de source n'est retouché.

Dans `tests/test_eneide_source_access_20261106.py`, un cas de non-régression reproduit la structure réelle : titre `h1` dans le header muséal, premier `h2` dans l'article, renvoi avant le premier chapitre, puis deuxième exécution idempotente.

Dans `assets/mythos-eneide-sources.css` : renforcement du contraste au survol, lisibilité des sections ouvertes, zones tactiles sous 480 px. L'ajout sous `assets/**` déclenche le workflow de publication sans modifier sa planification ni sa définition.

**Commits :** `6692dafe27ee303c4c6e00958f5dc2aa630c2e51`, `a58b21a330bbd53c35716d4562a6c73113888b44`, `2e6cd305acb232e21d65409babf3300d85c5fe55`, `2364fd70c78f5c2a4272b58e694ec5428a0c5379`.

## Corpus et règles de numérotation

Les 18 manuscrits d'Énéide, déjà publiés en version HTML, sont **un contenu existant**, pas de nouvelles études. Cette intervention répare leur diffusion en Markdown et leur navigation réciproque ; elle ne revendique pas une nouvelle monographie.

État observé lors de la relecture des reçus : 497 soumissions `editorial/inbox/`, 468 UUID attribués, 23 identités sur liste d'attente, et 6 sans reçu ni retenue explicite. Parmi les six, **cinq monographies intégrales déjà déposées dans la file** étaient consultables et demandaient à être traitées par le workflow (études de la `Lysistrata`, *Aithon* d'Achéos, MC-094 sur les clefs, Nabta Playa, Gebel Ramlah). Elles font entre 36 778 et 94 825 caractères Markdown. Le sixième chemin historique `20261105-mc-069-souffle-vent-vie-philologie.json` n'est pas un UUID ordinaire ; conserver la procédure de quarantaine / réconciliation et ne pas l'attribuer manuellement. Ne pas republier ces manuscrits sous un nouvel UUID ni anticiper leur numéro. Une exécution de reconstruction antérieure en CI avait attribué cinq demandes **dans un espace temporaire seulement**, puis échoué avant synchronisation.

**Nouvelles premières publications confirmées pendant l'intervention : zéro** au moment du contrôle initial. Les attributions et déploiements ultérieurs doivent être établis par reçus, workflow terminé et contrôle HTTPS, sans inférence à partir de la seule présence dans la file.

## Contrôles et statut de publication

- Source et contexte du récit vérifiés sur `main` ; le `h1` de la bannière précède `<main>`, le premier `h2` du récit suit dans `main article.content`.
- Le correctif et le test ont été réinspectés après commits, et le cas de normalisation du DOCTYPE a été reproduit localement à l'aide de BeautifulSoup.
- GitHub Actions de validation `42171943603` était en cours au contrôle ; workflow de publication associé à la modification de CSS : `42172201994`, initialement en attente. **Aucune publication ou conformité de bout en bout n'est déclarée avant leurs conclusions**.
- Conditions de clôture : tests verts, génération complète, reçu d'attribution des demandes effectivement traitées, manifeste public avec commit postérieur aux correctifs, HTTP 200 de `/corpus/philosophie/eneide/00-introduction.md` et `17-reperes-et-sources.md`, liens réciproques visibles, contrôle responsive réel.

Aucune autre automatisation MYTHOS, aucun fichier numéroté et aucune archive n'a été modifié par cette réparation.
