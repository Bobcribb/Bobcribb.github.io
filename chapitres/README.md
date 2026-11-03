# Publier de nouveaux chapitres MYTHOS directement sur GitHub

Le site MYTHOS est désormais publié depuis GitHub, sans requête à l'API WordPress.

Pour ajouter une nouvelle étude, créer dans ce dossier un fichier Markdown au nom court, en minuscules sans espaces, par exemple `grece/chiron-etude.md`. Il sera rendu sur le site sous `https://bobmythos.fr/chapitres/grece/chiron-etude/`.

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

Avant de créer une étude, vérifier la branche `main` actuelle et lancer `python scripts/editorial_numbering.py`. Chaque collection a sa propre séquence ; ne pas déduire le prochain numéro d'une ancienne conversation ou d'une seule page. Consulter `EDITORIAL_NUMBERING.json` et `/collections-numerotees/`. Si `main` évolue avant l'écriture, revérifier le numéro sur le nouvel état. Le build et l'audit des pull requests refusent les collisions inconnues. Les anciennes adresses déclarées sont des redirections, pas de nouvelles études.
