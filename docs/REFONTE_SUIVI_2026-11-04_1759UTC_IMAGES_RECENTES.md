# MYTHOS — garde des images universitaires et état documentaire (4 novembre 2026, 17 h 59 UTC)

## Source de vérité et intégrité éditoriale

Contrôle effectué sur `Bobcribb/Bobcribb.github.io`, branche `main`, après lecture effective de `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`. Commit de départ : `3a6bb0b9c31c283806343391162812dff35d13a6`. Aucun numéro n'est déduit de cet historique ; seule l'attribution atomique GitHub Actions fait foi.

L'inventaire réalisé sur la branche de départ compte **239 fichiers dans `editorial/inbox/`**, **232 reçus** dans `editorial/numbering.json` (42 Origines du sacré, 53 Encyclopédie, 31 Comédies, 33 Tragédies, 73 Comparatif), **5 retenues documentées** dans `editorial/holds.json`, **2 manuscrits en attente de reçu**. Ces deux demandes contiennent des études publiques complètes avec sources et bibliographies :
- `a6d8e75b-69f3-4e0b-8a58-0ad49573c053.json` : `comparatif`, MC-053, « Soigner, guérir, échouer », 98 192 caractères Markdown ;
- `f3c8ab61-4a57-42cc-b809-23eda917500d.json` : `comedies`, Nicocharès, *Galateia*, 50 495 caractères Markdown.

Elles ont **déjà leur UUID stable** et ne sont **ni resoumises, ni numérotées, ni annoncées comme déployées** ici. Une recherche ciblée dans la bibliothèque des fichiers antérieurs n'a trouvé qu'un index éditorial 216–224 — celui-ci déclare expressément ne pas constituer la sauvegarde intégrale des chapitres. Les tomes intégrés des *Origines du sacré* sont des publications déjà conservées, non des inédits à recréer. Les mentions historiques Chiron 118–133 et Nyx–Hypnos 218–224 ne valent donc pas, à elles seules, manuscrit intégral approuvé récupéré.

**Nouvel inédit intégral déposé lors de cette intervention : zéro.** Toute republication des deux manuscrits en attente ou d'une étude déjà attribuée créerait une concurrence ou un doublon. Aucun texte, source, bibliographie ou archive n'a été tronqué ni déplacé.

## Correction du rendu muséal

Une passe `scripts/apply_museum_design.py` ultérieure à la création des cartes des dernières études pouvait supprimer leurs photographies documentaires en cherchant à remplacer toutes les vignettes par les couvertures génériques. Cela laissait la légende `mythos-recent-caption` sans image. La correction préserve exclusivement les images des cartes de `#home-etudes-recentes` placées dans `.mythos-recent-illustration`, si leur fichier existe réellement dans `/media/` et porte une extension photographique autorisée (JPEG, PNG, WebP). Les SVG 2,5D exclus et les fichiers absents ne bénéficient d'aucune exception.

La charte noir/ivoire/or et le bandeau statue grecque/temple sont conservés, tout comme les sommaires, les renvois réciproques et les mises en page responsive existantes. Cette correction vise la **stabilité visuelle des reconstructions successives** : elle ne prétend ni ajouter une nouvelle image ni modifier l'iconographie d'un manuscrit.

Deux tests supplémentaires dans `tests/test_museum_recent_images.py` contrôlent : trois passes idempotentes conservant l'image, l'alternative textuelle et la légende, sans toucher au texte source ; refus des images absentes ou SVG anciens. Aucun fichier `chapitres/`, `editorial/numbering.json`, `editorial/holds.json`, workflow ou automatisation n'est modifié.

## Commits et vérifications

- `5be6813a4e72e0f9feab2d4fb56ba70c418c1bb3` : correction de `scripts/apply_museum_design.py` (13 lignes ajoutées).
- `74ec4f5c4b5b4af9d503178082cf652e5d2c54c7` : 2 tests de non-régression (76 lignes ajoutées).
- Comparaison GitHub avec la branche de départ : deux fichiers seulement modifiés/ajoutés, aucune suppression, avance de deux commits. Les deux fichiers ont été relus depuis `main` après écriture.

Les nouveaux tests et la publication doivent encore être validés par une exécution GitHub Actions couvrant le commit concerné. Au contrôle, le dernier workflow de publication visible portait sur un commit antérieur, `d3f2f5698db24638727382d4f35b0ceea11ee917`, et était `in_progress`. L'accès externe à `https://bobmythos.fr/` et `/catalog/publication-verification.json` a échoué dans le navigateur disponible. **Le déploiement public des deux commits de cette intervention n'est pas attesté.** Contrôles de sortie : `python -m unittest discover -s tests -v`, `python scripts/build_native.py`, `python scripts/verify_publication.py`, puis contrôle du panneau des dernières études et de la preuve de déploiement HTTPS.
