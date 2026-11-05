# MYTHOS — Raccorder les manuscrits 491 et suivants à leur portail universitaire

5 novembre 2026. Contrôle préalable de main, AGENTS.md et docs/PUBLICATION_CONCURRENTE.md.
État source initial : f8e6a32d1e17602c4e7dcbe7787301897be57a67.

## Recherche d'un texte intégral inédit
Inventaire réel : 431 fichiers dans editorial/inbox, 413 reçus dans editorial/numbering.json, 17 demandes retenues dans editorial/holds.json. Un seul fichier hors reçus et retenues, 20261105-mc-069-souffle-vent-vie-philologie.json, doit rester hors allocation (nom non UUID et cote MC-069 concurrente). Aucune étude autonome, intégrale, approuvée et absente du circuit éditorial n'a été découverte dans les sources publiques inspectées. Les archives de brouillons WordPress du Drive sont privées.
Nouvelles premières publications directement dues à cette intervention : 0. Les manuscrits déjà attribués ne sont pas redéposés.

## Problème de navigation vérifié
Le portail /origines-du-sacre/ se concentrait sur les 48 dossiers historiques 443–490 et les 27 tomes, malgré l'existence des monographies numérotées au-delà de 490. Le chapitre 697, étude intégrale de Palmyre (46 598 octets Markdown), est accessible en public ; les autres chapitres universitaires 491–696 étaient insuffisamment visibles depuis cette porte d'entrée.

## Correction génératrice
scripts/build_navigation.py ajoute désormais une section dynamique « Études universitaires complémentaires » qui est construite seulement depuis les URLs canoniques présentes dans le catalogue, le Markdown scientifique intégral présent et son lecteur HTML effectivement rendu. Les six derniers manuscrits sont des cartes de lecture directes et les autres sont listés par groupes de 25 en détails accessibles. Les titres scientifiques sont extraits des en-têtes réels du Markdown ; un simple « Résumé scientifique » est refusé. Tous les liens sont générés depuis les manuscrits existants, sans copie, numérotation manuelle ni inventaire secondaire.
assets/mythos-museum.css conserve le graphisme anthracite/or, l'affichage responsive et les repères de focus clavier. tests/test_origins_additional_index_20261105.py vérifie la couverture, l'unicité des accès, les titres et le refus des lecteurs non construits.

## Publication antérieure vérifiée
Le workflow GitHub Actions 42036779274 a réussi et le manifeste HTTPS source_commit=f677da8325522702913bb69d77498cba6285f333 indiquait 1539 documents, 27 archives et 110 médias. La nouvelle section de ce commit ne sera déclarée en ligne qu'après contrôle séparé du workflow et de l'URL publique. Tous les textes, archives, reçus et automatisations MYTHOS sont préservés.