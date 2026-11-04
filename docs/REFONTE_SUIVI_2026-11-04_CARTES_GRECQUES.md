# MYTHOS — Iconographie vérifiée dans les dossiers de l'encyclopédie grecque

**Intervention du 4 novembre 2026 — branche `main`.** Avant la modification,
les règles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relues.

## Contenus universitaires et garde de numérotation

Sur le premier état consulté, `editorial/inbox/` contenait 111 demandes et
`editorial/numbering.json` 101 reçus, soit 10 demandes déjà déposées sans
reçu à cet instant. Tous ces UUID restent à la charge de GitHub Actions.
Les études historiques de Chiron et de la série 218–224 demeurent sans
manuscrits anciens intégraux approuvés retrouvés ; ne pas les confondre avec
les 23 nouvelles rédactions déjà publiées. **Nouveaux textes universitaires
soumis par cette intervention : 0.**

## Changement des cartes

`scripts/build_greek_corpus.py` produit désormais des cartes de dossier
illustrées avec des **documents existants du dépôt** et non des images
génériques. Six des huit cycles historiques possèdent un objet ou monument
pertinent, enregistré avec sa source, crédit, alt et légende détaillée dans
`scripts/editorial_media.json` :

- Dynasties attiques : lécythe à Athéna.
- Thésée : amphore antique Thésée–Minotaure (Metropolitan Museum).
- Cultes civiques d'Athènes : grand relief d'Éleusis.
- Apollon, Délos et Delphes : photographie du temple d'Apollon à Delphes.
- Cosmogonies : papyrus de Derveni (témoignage ancien d'exégèse cosmologique).
- Rites et concepts : vase de Déméter et Triptolème (Metropolitan Museum).

**Astres** et **Pélion–Hespérides** conservent une carte sans illustration :
aucun document suffisamment spécifique n'a été sélectionné à leur place.
Les crédits détaillés, liens des sources et licences sont conservés dans
un panneau repliable, sans encombrer la liste de lecture. Sur petit écran,
l'image est alignée à gauche du titre et le sommaire passe sur une colonne.

Les règles de publication préviennent une image sans provenance ou introuvable
dans la sortie du site. Aucun ancien SVG de perspective 2,5D n'est utilisé.
Aucun manuscrit, numéro, bibliographie, texte archivé ou média n'est modifié.

## Tests et vérifications

`tests/test_greek_dossier_iconography.py` garantit que les associations
sont uniques, que les cartes conservent liens et crédits, et qu'une image
demandée mais absente du rendu est refusée. L'index universitaire continue
de pointer vers chaque manuscrit intégral à son adresse canonique.
Vérifier les tests, le générateur et la publication, puis sur
`https://bobmythos.fr/mythologie-grecque/` les sommaires responsives.
**Le commit GitHub ne vaut pas preuve de déploiement public.**

Aucun workflow, aucune planification horaire MYTHOS et aucun registre de
numérotation n'a été modifié.
