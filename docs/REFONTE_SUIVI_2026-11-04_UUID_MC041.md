# MYTHOS — Réconciliation d'un UUID éditorial mal formé (4 novembre 2026)

Le dépôt de référence est `Bobcribb/Bobcribb.github.io`, branche `main`. Les consignes `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été examinées avant l'opération.

## Incident vérifié

Les contrôles GitHub Actions précédents échouaient dans `scripts/editorial_queue.py` avec `ValueError: badly formed hexadecimal UUID string`, lors du balayage de `editorial/inbox/` : un manuscrit public et non attribué portait un nom composé d'un identifiant de 37 caractères au lieu d'un UUID canonique de 36 caractères.

Source historique : `editorial/inbox/85ed9610-42a9-4b7b-90e0-2aeb8a619d041.json`.

Nouvel identifiant de dépôt : `editorial/inbox/85ed9610-42a9-4b7b-90e0-2aeb8a619d04.json`.

Collection : `comparatif`. Sujet : `mc-041-reves-souverains-gudea-thoutmosis-hattusili-joseph-daniel-xerxes-pouvoir` (MC-041 — songes de souveraineté). Texte Markdown intégral présent : **66149 caractères**. Le JSON a le schéma `version/collection/slug/markdown`, les variables `{{volume}}` et `{{numero}}` ; le manuscrit contient ses sections universitaires, sources et bibliographie. Le fichier source est déjà rendu public comme demande de publication ; aucune rédaction nouvelle n'a été inventée.

## Intervention conservatoire

Le nom invalide a été remplacé par un UUID valide en déplaçant **le même objet blob Git**, sans réécriture du JSON, du texte, des citations ni de la bibliographie. Son SHA blob Git initial était `db3a4a2dc727955820c5cb12bcb5525d6ca09343`. La version sous l'ancien nom reste récupérable dans l'historique Git ; le dépôt ne contient qu'une demande active pour ce manuscrit sous son nouveau nom.

La mise en quarantaine temporaire inscrite dans `scripts/editorial_queue.py` permettait d'éviter l'arrêt du workflow sans perdre le texte ; elle était utile pendant le diagnostic mais n'attribuait aucun numéro. La demande maintenant corrigée doit passer par la file ordinaire et **GitHub Actions seul** est autorisé à lui attribuer son numéro.

## Absence de doublon et limites

Avant la mutation : 172 demandes dans l'inbox, 154 attributions dans le registre, 18 demandes non attribuées, dont deux en attente explicite dans `editorial/holds.json` (versions parallèles des pièces d'Apollophanès). Le présent déplacement ne crée pas une seconde soumission active, ne touche pas au registre d'attribution et ne lève aucune attente éditoriale. Il ne modifie aucune autre automatisation.

La nouvelle étude MC-041 ne doit être annoncée comme **publiée et numérotée** qu'après présence d'un reçu sous son nouvel UUID dans `editorial/numbering.json`, réussite du workflow de publication et vérification du déploiement sur `bobmythos.fr`. Les tests et workflows doivent être revérifiés après écriture.

## Refonte de navigation menée en parallèle

Une précédente transaction de ce cycle (`b7eb2b03c4bc6715e6b65cc6422325cdc23b0a85`) a ajouté la navigation de fin de lecture aux études déjà publiées, avec trois renvois (collection, catalogue intégral, titre), style noir et or, cibles tactiles d'au moins 44 px, une colonne sur téléphone et impression sans navigation. Tests : `tests/test_museum_study_endnav.py`. Aucune modification du manuscrit de l'étude.
