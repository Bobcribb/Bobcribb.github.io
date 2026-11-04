# MYTHOS — Unification canonique du corpus grec, 4 novembre 2026

## Situation initiale
Dépôt canonique `Bobcribb/Bobcribb.github.io`, branche `main`.
`AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été lus.
Le menu « Grande encyclopédie » avait déjà été retiré par l'exécution
concurrente antérieure ; ne pas réappliquer ni annuler ce correctif.

Le générateur `scripts/build_greek_corpus.py` produisait quatre pages du même
catalogue intégral, sous `/mythologie-grecque/`, son alias `.html`, ainsi que
`/grande-encyclopedie/` et son alias `.html`. Chaque ancienne adresse
possédait une balise canonical distincte, ce qui pouvait disperser les signaux
de référencement d'un même contenu.

## Intervention
- Conserver intégralement les quatre pages et les liens des archives ; ne
  supprimer ni chapitre, ni numéro, ni bibliographie, ni source.
- Utiliser une seule URL canonical pour les quatre : `/mythologie-grecque/`.
- Signaler « Encyclopédie grecque » comme entrée de navigation active
  depuis l'adresse historique `/grande-encyclopedie/`, tout en conservant
  l'ancien sommaire accessible.
- Préserver le lien distinct vers `/grande-encyclopedie/registre-integral/`,
  registre transversal des six collections ; ce lien est déjà fourni par
  `build_greek_corpus.py` dans les ressources reliées.
- Ajouter des tests de non-régression de la canonicalisation, de la présence
  du registre transversal, et de l'état actif des menus.

## Manuscrits et déploiement
Lors du premier contrôle, la file contenait 109 manuscrits JSON, dont huit
sans reçu dans le registre `editorial/numbering.json` à cet instant.
Ils ont chacun un UUID persistant : aucune soumission nouvelle, renumérotation
ou création directe dans `chapitres/` n'est justifiée. Une autre exécution
concurrente peut les attribuer ; consulter le reçu avant toute annonce.
**Études intégrales nouvelles soumises par ce correctif : 0.**
Aucune planification MYTHOS, aucun workflow et aucune collection numérotée
n'ont été modifiés.

Contrôles prévus : tests unitaires de l'index grec et de la navigation, puis
workflow GitHub Actions et `/catalog/publication-verification.json`.
La confirmation d'un commit ne vaut pas confirmation du déploiement public.
