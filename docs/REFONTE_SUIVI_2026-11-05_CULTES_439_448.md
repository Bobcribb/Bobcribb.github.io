# MYTHOS — Refonte des dossiers : études locales 439–448 (5 novembre 2026)

## Source de vérité et périmètre

Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`. Avant la modification,
consultation de `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`,
`scripts/build_greek_folders.py` et des titres de dix sources Markdown
existantes : `chapitres/encyclopedie/chapitre-{439..448}-*.md`.
Tous les dix manuscrits et leurs pages HTML existent dans `main`.
Aucune attribution, suppression, réécriture, copie ou renumérotation.

## Classement vérifié des dix monographies conservées

| Chapitre | Objet principal | Famille primaire |
| --- | --- | --- |
| 439 | Apollon Karneios, Karneia à Sparte, Théra et Cyrène | Cultes et sanctuaires |
| 440 | Zeus Diktaios, Palaikastro, hymne du Kouros | Cultes et sanctuaires |
| 441 | Euthymos de Locres et Témésa, héroïsation | Héros et héroïnes |
| 442 | Poséidon Onchestios à Onchestos, chars et fédération | Cultes et sanctuaires |
| 443 | Artémis Orthia à Sparte, masques votifs et rites | Cultes et sanctuaires |
| 444 | Éros à Thespies, pierre aniconique, Praxitèle, Érotidies | Cultes et sanctuaires |
| 445 | Hermès Kriophoros à Tanagra | Cultes et sanctuaires |
| 446 | Artémis Tauropolos à Halai Araphénides | Cultes et sanctuaires |
| 447 | Héraclès à Thasos, héros/dieu et Melqart | Cultes et sanctuaires |
| 448 | Amphiaraos et l'Amphiaréion d'Oropos, incubation | Cultes et sanctuaires |

Leur ancien classement générique, parfois « Nouvelles études à classer »,
ne reflétait pas la documentation locale sur les rites, sanctuaires et cultes.
Le chapitre 441 est précisément consacré à une héroïsation ; il conserve
une rubrique héroïque. Les récits mythiques et personnages évoqués incidemment
ne doivent pas déterminer un classement au détriment du sujet principal.

`scripts/build_greek_folders.py` décide uniquement les dossiers thématiques
et leurs sous-sections. Le sommaire et le lien retour des pages sont
régénérés par la procédure existante, sans toucher à la prose des articles.
Le menu unique de la mythologie grecque, les huit familles, leurs images, la
bannière statue/temple et les styles responsives restent conservés.

## Couverture technique

`tests/test_greek_recent_local_cults_20261105.py` contrôle :
les dix sources existantes, leur longueur, l'appareil bibliographique,
les affectations thématiques indépendantes des mots parasites, deux
générations consécutives sans doublons, la présence des renvois et la
conservation stricte des articles ainsi que les empreintes des sources.

## État des contenus non attribués

La consultation préalable de `editorial/inbox/`, `editorial/numbering.json`
et `editorial/holds.json` montre que plusieurs manuscrits intégraux
approuvés sont **déjà** soumis dans la file transactionnelle (notamment
des études grecques, des comédies et des dossiers « Origines du sacré »).
Leur absence de reçu ne permet ni de leur inventer un numéro, ni de les
réémettre sous un autre UUID. Un manuscrit MC-069 au nom non conforme
reste explicitement en quarantaine. Aucun brouillon privé WordPress ne
doit être importé automatiquement.

**Premières publications nouvelles par cette séance : zéro.**
Les seuls travaux de cette intervention concernent la navigation des
monographies intégrales déjà présentes. Confirmer séparément les tests
GitHub Actions, l'attribution de nouveaux textes et leur visibilité HTTPS
avant de parler de déploiement effectif.

Aucune modification des cinq registres de numérotation, des manuscrits,
des archives, des programmes horaires ou des autres automatisations.
