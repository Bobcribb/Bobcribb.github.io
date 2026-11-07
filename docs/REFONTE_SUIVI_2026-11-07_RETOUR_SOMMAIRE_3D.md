# MYTHOS — navigation réciproque dans la galerie 3D

**Contrôle : 7 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`. Site : https://bobmythos.fr.

## Vérifications préalables

- La galerie photoréaliste intégrée à `main` compte **90 sections scientifiques**. Son sommaire comporte 90 liens distincts vers leurs identifiants, sans section manquante ni lien dupliqué.
- Le manifeste HTTPS public `/catalog/publication-verification.json` indiquait, au contrôle, le commit source `407ebf859727172ce6fef54ce1b8718bcc92c22b`, le workflow `42355074478` et **1 817 documents indexés**. Ces chiffres sont des photographies de contrôle, pas un état garanti pour la suite.
- Les anciens échecs provoqués par un sommaire source décalé lors d'ajouts parallèles de reconstitutions sont déjà protégés par la régénération du sommaire dans `scripts/improve_reading.py`. Ne pas rouvrir les fichiers de manuscrits pour les résoudre.

## Amélioration effectuée dans le générateur

La galerie rassemble 90 notices et leurs appareils scientifiques. Revenir au sommaire depuis la fin d'une notice nécessite auparavant un long déplacement vertical sur smartphone.

Le lecteur de `scripts/improve_reading.py` reçoit exclusivement pour les galeries 3D :

- une cible stable `#sommaire-reconstitutions` sur son sommaire généré ;
- un lien « Revenir au sommaire des reconstitutions » **en fin de chaque notice scientifique** ;
- un marquage `data-reading-owned="true"` signalant qu'il s'agit d'un élément de navigation reconstruit, non du texte de l'auteur ;
- la reconstruction idempotente : à chaque passe, les anciens éléments du lecteur sont éliminés avant de créer les nouveaux. Aucun texte source, numéro ou fichier d'image n'est réécrit.

Le style est défini dans `assets/mythos-discovery.css` : noir/ivoire/or, cible tactile d'au moins 44 px, focus clavier visible, bouton pleine largeur sur téléphone, exclusion de l'impression et positionnement d'ancre compatible avec l'en-tête.

## Contrôles de conservation

`tests/test_gallery_toc_anchor_20261106.py` est enrichi pour comparer avant et après :

- la totalité des paragraphes scientifiques des notices ;
- les chemins et les alternatives textuelles des images ;
- les renvois individuels et l'absence de doublons après deux générations ;
- la présence d'un seul sommaire identifié ;
- l'absence de ces liens sur les lecteurs génériques hors galerie.

Les tests précédents sur les ancres Métaponte/Akragas, les doublons d'identifiants et les ajouts concurrents restent actifs.

## Limites et confirmation

Le dépôt peut contenir les modifications sans que le site public serve encore leur nouveau HTML et CSS. Vérifier les tests GitHub Actions, le rendu généré, le déploiement Pages et les retours visibles sur https://bobmythos.fr/reconstitutions-photorealistes.html avant toute annonce de publication.

**Conservation stricte :** pas de modifications de `editorial/numbering.json`, `editorial/inbox/`, des manuscrits, notices scientifiques, images WebP ou archives. Aucune planification horaire n'est activée, déplacée ni modifiée.
