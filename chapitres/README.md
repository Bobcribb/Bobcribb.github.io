# Publier de nouveaux chapitres MYTHOS directement sur GitHub

Le site MYTHOS est désormais publié depuis GitHub, sans requête à l'API WordPress.

Pour une nouvelle étude **numérotée**, utiliser la [file de publication et son attribution atomique](../docs/PUBLICATION_CONCURRENTE.md). Déposer le texte intégral approuvé sous `editorial/inbox/<uuid>.json`, avec `{{numero}}` ou `{{volume}}`. GitHub Actions choisit le prochain numéro d'après les fichiers réellement présents sur `main`, enregistre le manuscrit et son reçu ensemble, puis reconstruit le site. Ne plus créer directement de nouveau chemin numéroté dans les cinq collections contrôlées. Les corrections d'études existantes conservent leur chemin et leur numéro.

Pour une étude indépendante **sans numéro de série**, créer un fichier Markdown au nom court, en minuscules sans espaces, par exemple `grece/chiron-etude.md`. Il sera rendu sur le site sous `https://bobmythos.fr/chapitres/grece/chiron-etude/`.

Modèle :

```markdown
---
title: Chiron — le centaure et le savoir
description: Étude des traditions grecques sur Chiron et la transmission des savoirs.
---

# Chiron — le centaure et le savoir

## Sources anciennes

Développer ici une analyse universitaire complète, avec références et bibliographie...
```

La publication se lance automatiquement après chaque modification validée sur la branche `main`. Le générateur conserve les **502 dossiers déjà publiés**, ajoute la nouvelle page à la recherche et au catalogue, et reconstruit le sitemap.

**Important :** ce dépôt GitHub est public. Ne jamais déposer ici les 135 brouillons sauvegardés en privé, les identifiants, ni un texte qui ne doit pas être publié. Le fichier Markdown envoyé est une publication, non un brouillon privé.

Le workflow conserve également une exécution horaire pour vérifier le site, sans inventer automatiquement de nouveaux chapitres. La génération horaire de textes dans ChatGPT n'est pas, en soi, une publication sur GitHub. Pour un nouveau chapitre issu des travaux éditoriaux, demander explicitement : « Publie ce chapitre dans MYTHOS sur GitHub ».

Les anciennes pages de WordPress restent figées dans le dépôt. Si WordPress devient privé ou inaccessible, cela n'a plus d'effet sur la publication du site public.

## Numéros uniques et publications simultanées

Les corrections historiques et leurs redirections sont décrites dans `EDITORIAL_NUMBERING.json` ; le contrôle `python scripts/editorial_numbering.py` vérifie l'unicité canonique. Pour une nouvelle étude, passer par la [file transactionnelle](../docs/PUBLICATION_CONCURRENTE.md) : une simple lecture de `main` ne réserve pas un numéro. `editorial/numbering.json` conserve les attributions et les reçus de cette file ; les fichiers effectivement présents sur la branche principale sont relus à chaque tentative.
