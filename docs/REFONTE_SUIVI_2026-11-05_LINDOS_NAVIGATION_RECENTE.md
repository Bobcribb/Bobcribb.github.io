# MYTHOS — Refonte : concordance Lindos, titres scientifiques et navigation mobile

**Date du contrôle :** 5 novembre 2026. **Dépôt :** `Bobcribb/Bobcribb.github.io`, branche `main`.

## État réel avant intervention

- `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md` et le commit historique `ab067829b1012272d275d7417071d7e415676063` ont été relus.
- La branche principale avait dépassé le commit de reprise. Cette correction est réalisée sur une branche isolée, sans modifier le générateur de numéros.
- Un audit GitHub Actions (exécution `42017969675`) a compté **0 erreur critique et 1 avertissement bloquant** : dans la page du chapitre 438, un renvoi vers le chapitre 433 pointait vers une extension Markdown relative inexistante sur GitHub Pages.
- Le manifeste public `https://bobmythos.fr/catalog/publication-verification.json`, interrogé pendant le contrôle, annonçait `source_commit: c46ff854a9c173783ac0801b62fea22aed44750f` et `github_run_id: 42016585966`. Le site public était donc encore en retard sur les commits ultérieurs consultés. Aucune conformité au nouveau commit n'est présumée.
- L'accueil public présentait « Résumé scientifique » comme titre du dernier chapitre des Origines du sacré (689), alors que son titre scientifique réel commence par « Enterrer le roi, montrer l'empire ».

## Inventaire de publications : respect du circuit atomique

Photographie ponctuelle de `editorial/inbox/`, `editorial/holds.json` et `editorial/numbering.json` :

- **400** objets en inbox, **384** identifiants munis de reçus et **12** manuscrits expressément retenus.
- Trois demandes valides sans reçu étaient visibles au moment du contrôle : Magnès, *Poastria* (comédies, UUID `451f59a9-c679-4399-a7d4-dc182568df00`) ; Agathon, *Télèphe* (tragédies, UUID `53bd28f5-628f-43e5-8923-11f805fe8269`) ; Mausolée d'Halicarnasse (Origines, UUID `5c7cf210-3f89-469d-8f8b-6f0ec57d1e71`).
- Un quatrième fichier `20261105-mc-069-souffle-vent-vie-philologie.json` n'est pas un nom UUID valide et est conservé sans réattribution ni changement de nom ; son identité historique est en collision.
- Ces textes **existent déjà dans la file publique approuvée** et doivent être pris en charge par GitHub Actions, sans soumission en double ni numéro choisi manuellement.
- Les sauvegardes WordPress historiques sur Google Drive restent privées selon `docs/PROTOCOLE_DRIVE_VERS_GITHUB.md`. Aucun brouillon privé n'a été transféré ou déclaré publiable sans validation.
- **Manuscrits scientifiques nouvellement intégrés par cette intervention : 0.** Le blocage est documentaire (pas de manuscrit indépendant approuvé à transférer hors de la file existante) et transactionnel (attribution attendue par Actions).

## Correctifs fonctionnels et visuels

1. **Concordance Athéna Lindia :** dans `chapitres/encyclopedie/chapitre-438-athena-lindia-chronique-lindos-danaides-offrandes-epiphanies-memoire.md`, le renvoi du chapitre 438 vers le 433 emploie désormais l'URL HTTPS de lecteur, sans `.md`. Le corps scientifique, les 22 sections, les sources et la bibliographie ne sont pas résumés ni remplacés.
2. **Titres des dernières études :** `scripts/recent_studies.py` reconnaît les titres `# Chapitre N — ...` dans les cinq collections, y compris les Origines du sacré. L'accueil n'utilise plus le premier `## Résumé scientifique` comme titre lorsque le H1 est descriptif.
3. **Sommaire rapide :** un sous-menu relié aux cinq cartes de la page d'accueil donne des ancres stables, utilisables au clavier et en tactile. Sur petit écran, les liens se parcourent horizontalement ; largeur des cibles et surlignage de la carte visée sont assurés par `assets/mythos-museum.css`.
4. **Tests :** `tests/test_recent_studies.py` vérifie les titres, l'idempotence du sommaire et le lien canonique entre les chapitres 438 et 433.

Aucun nouveau visuel vectoriel en perspective 2,5D n'est ajouté. Les images et reconstitutions photoréalistes, notices et crédits préexistants restent inchangés. Aucun texte, numéro, reçu, archive, workflow ni programmation horaire n'est supprimé ou renuméroté.

## Vérifications à effectuer après fusion

- Exécuter `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py` dans les Actions de la branche principale.
- Vérifier la disparition de l'avertissement Athéna Lindia dans l'audit `scripts/audit_integrity.py`.
- Confirmer l'exécution GitHub Pages jusqu'au statut réussi, puis comparer le `source_commit` du manifeste public au commit réellement publié ; contrôler les URLs des lecteurs 433 et 438, le titre réel de l'étude récente et le sous-sommaire sur mobile.
- Ne déclarer **publication confirmée** qu'après vérification du site public et du manifeste, pas après le seul commit GitHub.
