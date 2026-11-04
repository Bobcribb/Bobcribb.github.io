# MYTHOS — Archives grecques autonomes et liens médias locaux (4 novembre 2026)

## Source et statut
Dépôt de vérité `Bobcribb/Bobcribb.github.io`, branche `main`.
`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relus.
L'ancien dépôt public `Bobcribb/Mythos` et le dépôt actif ont été consultés :
les manuscrits universitaires présents dans l'ancien dépôt sont déjà copiés
dans le nouveau ; aucun nouveau texte distinct, intégral et approuvé n'a été
identifié. Les demandes en attente dans `editorial/inbox/` restent à leurs UUID.

## Anomalie précise constatée
L'annexe interactive
`corpus/mythologie-grecque/archives/MYTHOS_bibliotheque_navigable.html`
conservait **12 références à la médiathèque de WordPress**, correspondant à
**9 photographies distinctes** déjà archivées sous le même nom dans
`media/2026/10/`. Certaines URL figurent dans du JavaScript intégré plutôt
que dans des attributs HTML : un simple contrôle des balises `img` manque
ces dépendances.

Treize autres HTML de `corpus/mythologie-grecque/archives/` contenaient un
appel relatif à `assets/app.js`, **fichier absent dans les deux dépôts**.
L'appel renvoyait 404, même si le site dispose désormais des outils modernes
`/assets/mythos-reading.js`.

## Correction intégrée dans la génération
`scripts/build_native.py` réécrit **sur la copie publique seulement**
les URL WordPress des images de l'archive grecque, et uniquement lorsque
le fichier correspondant existe déjà sous `_site/media/2026/10/`.
Cette correction conserve la photographie originale, son nom et le
contexte de sa notice ; aucun visuel générique ni 2,5D n'est substitué.
Les images manquantes restent signalables : pas de reconstitution inventée.

Les appels à `assets/app.js` sont retirés des copies publiques uniquement
si leur script est introuvable. Les scripts et instruments de lecture existants
restent conservés. Les liens bibliographiques, titres, paragraphes et
ancres historiques ne sont pas modifiés.

`tests/test_site_audit_fixes.py` contrôle les URL dans `img` et JS intégré,
la préservation des liens et des octets sources, ainsi que le non-retrait
d'un script quand le fichier existe effectivement.

## Garanties et limites
- **Nouvelles études universitaires soumises ici : zéro** ; aucune source
  intégrale approuvée et absente du nouveau dépôt n'a été identifiée.
- Aucune modification de `chapitres/`, de la numérotation, de la file
  `editorial/inbox`, des archives sources ou des médias binaires.
- Aucune planification MYTHOS ni aucun workflow GitHub Actions modifié.
- Contrôles attendus avant annonce de publication : suite Python complète,
  génération `build_native.py`, `verify_publication.py`, workflow de
  déploiement et preuve HTTPS `/catalog/publication-verification.json`.
