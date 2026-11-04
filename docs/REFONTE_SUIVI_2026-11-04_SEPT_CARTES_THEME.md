# MYTHOS — Sept cartes illustrées des dossiers encyclopédiques

Intervention du 4 novembre 2026 sur `Bobcribb/Bobcribb.github.io`, branche
`main`. Les règles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été lues
avant toute écriture. Les modifications sont exclusivement documentaires et
graphiques ; aucune édition universitaire n'a été remplacée ou abrégée.

## Corpus disponibles et décision d'intégration
Le premier état de la file éditoriale contenait 119 demandes persistantes
et 111 reçus d'attribution : huit manuscrits intégraux déjà soumis, en attente
de traitement par Actions. Les importer à nouveau créerait des doublons. Les
anciens manuscrits historiques absents ne sont pas reconstitués arbitrairement.
**Nouvelle étude intégrale distincte et approuvée importée ici : aucune.**

## Correction livrée
`scripts/build_greek_folders.py` et `scripts/build_greek_corpus.py` enrichissent
la navigation des huit familles du corpus grec. Sept cartes s'appuient sur
des documents déjà présents et munis d'une notice de provenance dans
`scripts/editorial_media.json` :

- Divinités : bronze du cap Artémision (Zeus ou Poséidon, identification discutée).
- Héros : amphore grecque représentant Thésée et le Minotaure.
- Grandes familles : porte des Lionnes de Mycènes (vestige, non preuve des Atrides).
- Cycles épiques : Priam et Achille, coupe du Peintre de Briséis.
- Cultes et sanctuaires : temple d'Apollon à Delphes, état archéologique.
- Sources anciennes : fragments du papyrus de Derveni.
- Interprétations philosophiques : Mort de Socrate par David (réception moderne,
  explicitement distincte de l'Antiquité).

La famille « Cosmogonies » reste volontairement sans image tant qu'aucun
objet grec précisément lié au thème n'est sélectionné. Aucun document
mésopotamien n'est utilisé comme illustration générique de la Grèce.

Sur les cartes, un panneau dépliable conserve la notice complète :
description de l'objet, auteur de la photographie, provenance, lien à la source,
licence et réserves historiques. Les illustrations sont uniquement des repères
de dossier, jamais des preuves pour tous les manuscrits du thème.
Les cartes conservent leur ordre, leur cote et leurs liens ; un contrôle
vérifie que le média existe dans le site généré, sinon la publication échoue
plutôt que de remplacer une image sans justification.

Le catalogue reste classé par les huit familles vérifiées, avec ses
liens réciproques, ses rubriques propres et ses anciennes adresses.
La mise en page noire et or et le responsive sont conservés.

## Périmètre protégé
Aucun fichier de `chapitres/`, `editorial/numbering.json`, aucune archive,
aucun média binaire, aucune numérotation, aucune planification et aucun
workflow n'a été modifié. Le script de musée, qui remplace les anciennes
images génériques des `.portal-card`, ne retire pas ces visuels documentaires :
les nouvelles cartes ont leurs propres classes CSS et sont construites
à partir du registre de provenance.

## Contrôle
`tests/test_greek_folder_media.py` vérifie le nombre d'images, les crédits,
les liens et le refus des fichiers manquants. La CI doit ensuite exécuter les
tests du dépôt et le générateur complet avant que le résultat soit déclaré
publié sur le domaine. Un commit Github seul n'est pas une preuve de déploiement.
