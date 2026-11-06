# MYTHOS — Refonte du menu muséal : état accessible, clavier et mobile

**6 novembre 2026, 20 h 20 (heure de Paris).** Source de vérité : `Bobcribb/Bobcribb.github.io`, branche `main`. Site : https://bobmythos.fr.

## Audit préalable

`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus : aucun numéro canonique ne peut être attribué manuellement ; les études originales, les archives et les reconstitutions photoréalistes doivent être préservées.

Au dernier contrôle, le manifeste public n'était pas vérifiable directement depuis les outils réseau de cette intervention. GitHub Actions montrait toutefois une publication réussie `42271985907` (6 novembre, 18 h 51 UTC) et une nouvelle publication `42276372391` encore en cours. Un audit intégral `42276706067` avait réussi.

Une validation de générateur ultérieure `42278527660` a échoué sur la collision historique MC-109. La première soumission `0b2e3ecb-74df-4bc3-9776-202611061953` consacrée aux masques rituels a depuis reçu le volume CCCXVIII (318). La soumission postérieure `a6c192ec-148a-4ba1-a909-202611061954`, consacrée aux ombrelles du sacré, a été placée en retenue par **un autre chantier**, sous l'empreinte SHA-256 `65ce69d4ef2705f55d185226af33aa72150e673c56f35d30043e4c76ea3c4823`. Cette intervention ne crée donc aucune autre soumission ni ne modifie ce registre.

## Anomalie d'accessibilité identifiée

L'en-tête partagé utilise un `<details class="mythos-menu">` natif. Le déclencheur `<summary>` avait toujours pour libellé accessible **« Ouvrir le menu »**, même lorsque la liste des rubriques était ouverte. La fermeture au clavier (Échap) et par clic extérieur existait déjà.

## Correction fonctionnelle

`assets/mythos-museum.js` met maintenant à jour le libellé du `<summary>` en fonction de l'état réel du `<details>` :

- fermé : « Ouvrir le menu » ;
- ouvert : « Fermer le menu ».

L'écoute de l'événement natif `toggle` garde le texte cohérent lors d'une interaction souris, tactile ou clavier. La touche Échap referme toujours le menu et restitue le focus au déclencheur ; un clic à l'extérieur referme également le menu. En l'absence de JavaScript, le `<details>` et ses liens restent utilisables. Aucun `aria-expanded` redondant n'est ajouté.

## Contrôles

- `tests/museum_menu_state_20261106.cjs` exécute le JavaScript réel avec un DOM simulé : ouverture/fermeture, changement du libellé, Échap, focus, clic intérieur et extérieur, initialisation ouverte et absence du menu.
- `tests/test_museum_menu_state_20261106.py` lance ce test avec Node et vérifie que les portails accueil, mythologie grecque, théâtre et Origines du sacré conservent les menus et liens accessibles, sans entrée « Grande Encyclopédie » en doublon.

Le CSS noir et or, la bannière statue/temple, les 3D photoréalistes, toutes les images, les textes universitaires et leurs bibliographies ne sont pas modifiés. Aucun workflow ou horaire d'automatisation n'est changé.

Une fusion de code n'atteste pas la publication : contrôler la réussite des tests et de GitHub Pages, puis le rendu accessible sur le domaine public avant de déclarer le déploiement confirmé.
