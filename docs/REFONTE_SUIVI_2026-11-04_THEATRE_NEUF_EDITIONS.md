# MYTHOS — Refonte du portail Théâtre : neuf éditions critiques raccordées

**Date : 4 novembre 2026.** Dépôt `Bobcribb/Bobcribb.github.io`, branche `main`.
À l'ouverture de la séance, `main` avait pour tête `1da5038ff04c4bdccd006d1c20601a66a7822bc8`.
`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus avant toute intervention.

## 1. Recherche d'études intégrales

L'examen de `corpus/theatre-grec/comedies/` a confirmé **neuf dossiers complets** qui existaient déjà publiquement dans le dépôt. Chacun conserve une source Markdown, une édition critique HTML avec bibliographie et une page HTML séparée de scènes modernes. Les trois fichiers de chaque dossier ont été ouverts et leur structure contrôlée. Le registre `corpus/theatre-grec/REGISTRE-INTEGRATIONS.md` documente leurs reprises intégrales antérieures ; cette séance ne revendique pas une nouvelle collation philologique.

| Dossier | Cote historique source | Markdown source (caractères) | Étude et scènes |
|---|---|---:|---|
| Polyidos | XXV | 15 806 | Présents, distincts |
| Daidalos | XXVI | 18 028 | Présents, distincts |
| Kôkalos | XXVII | 17 835 | Présents, distincts |
| Aiolosikôn | XXVIII | 11 173 | Présents, distincts |
| Holkades | XXIX | 12 387 | Présents, distincts |
| Lemniai | XXX | 13 461 | Présents, distincts |
| Géras | XXXI | 12 197 | Présents, distincts |
| Ploutos I | XXXII | 11 931 | Présents, distincts |
| Triphalès | XXXIII | 12 439 | Présents, distincts |

**Problème réel découvert :** aucun des neuf liens directs vers ces éditions critiques ne figurait dans `theatre/index.html` au contrôle préalable ; les études étaient physiquement accessibles mais absentes du sommaire central du Théâtre. Elles ne doivent pas être copiées une deuxième fois.

À la relecture de `main` après les modifications, la file comprenait **233 soumissions**, **223 attributions reçues**, **5 mises en attente explicites** et **5 soumissions sans reçu**. Ces cinq manuscrits universitaires sont déjà déposés dans `editorial/inbox/` : une nouvelle soumission ou attribution manuelle serait contraire à la garde transactionnelle. Les 135 brouillons WordPress sauvegardés dans Google Drive sont explicitement privés ; aucune sauvegarde n'a été transférée.

**Nouveau manuscrit inédit soumis lors de cette exécution : aucun.** Il n'a pas été identifié de manuscrit intégral nouveau et autorisé qui soit absent à la fois du site et du circuit éditorial. Les neuf éditions présentes ont été effectivement raccordées à la navigation, **sans se présenter comme de nouvelles publications**.

## 2. Modifications vérifiables

- `scripts/theatre_fragment_index.py` : sélectionne les neuf dossiers seulement lorsque source intégrale, étude critique, bibliographie et scènes modernes sont présentes ; rejette les éditions partielles ou entièrement absentes. Produit un sous-sommaire en neuf fiches sur la page `/theatre/`, avant la longue liste des pièces perdues, avec deux liens clairement distincts par œuvre et leur **cote historique inchangée**.
- `scripts/build_native.py` : appelle ce module après l'habillage et l'enrichissement des pages. Les fichiers sources universitaires ne sont ni déplacés ni réécrits.
- `assets/mythos-museum.css` : présentation noir, ivoire et or, trois colonnes sur grand écran, deux sur tablette, une sur mobile, liens accessibles de 44 px et adaptation à l'impression.
- `tests/test_theatre_fragment_index.py` : vérifie les liens, le volume historique, l'idempotence, la préservation des trois fichiers sources et les refus de publication pour une édition incomplète.

L'interface maintient la bannière grecque et la séparation demandée entre **texte critique** et **créations scéniques contemporaines**. Aucun SVG 2,5D ne réapparaît.

## 3. Commits enregistrés

1. `c11d3e3613ddc12a9a150d1284acbf0aec5a2a28` — générateur de sommaire critique.
2. `a113eb15649ce3f8f895f6b57ee4311f770f932a` — tests de conservation et de navigation.
3. `fe678c05a9d136432ffd474fadb7cb9667a32731` — connexion au build natif.
4. `b58e37008eb7f53ae9bc4d4962f25ca4e407e403` — styles adaptatifs.
5. `acb73a5632275bae5afa1111ef535823db1e3266` — normalisation stable de l'espacement du DOCTYPE lors des reconstructions.
6. `fe005d322077cea1e3012c59abb3a5b915d94c45` — refus de suppression silencieuse d'une archive déclarée.
7. `5c5d443d8227480935e3fccba5cf4e17d566c46d` — test de non-disparition des archives.

## 4. Contrôles et limites

Une validation de la première version du nouveau test a **échoué** : des sauts de ligne insérés par BeautifulSoup autour du DOCTYPE empêchaient la stricte identité binaire entre deux reconstructions. Le correctif `acb73a56` normalise cet espace. **La réussite de la CI après ce correctif reste à constater** ; ne pas annoncer de succès avant une nouvelle exécution concluante.

Une lecture indépendante de `https://bobmythos.fr/catalog/publication-verification.json` a confirmé une **version publique antérieure**, `source_commit=5d64aa9c910d52b635ec7cab3ea6455e7626b01c`, comportant **1 347 entrées indexées, 27 archives, 110 médias**. La page `/theatre/` publique ne présente pas encore « Comédies perdues d’Aristophane : éditions critiques et scènes modernes ». **L'enregistrement dans GitHub est certain ; le déploiement du nouveau sommaire n'est pas confirmé.**

Contrôles de sortie requis : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, conclusion `success` du workflow Pages et comparaison du reçu public avec le commit effectivement déployé.

Les registres de numérotation, les attributions, les fichiers Markdown universitaires, les 27 archives, les 110 médias, les autres automatisations et les planifications horaires **n'ont pas été modifiés**.
