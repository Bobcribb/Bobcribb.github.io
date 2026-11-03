# MYTHOS — Origines du sacré : conflit éditorial 576–577 du 3 novembre 2026

## État confirmé

La production de cette exécution avait vérifié un dernier chapitre 575 avant rédaction. Deux rédactions parallèles ont ensuite créé des fichiers portant les mêmes numéros 576 et 577. Les quatre textes sont conservés intégralement. Aucun n'a été supprimé, écrasé ou fusionné pendant le constat. Les fichiers créés dans cette exécution ont été relus sur `main` après leurs commits.

Le déploiement de publication n° 41644763105, associé au commit `621a1dd97a3da077c28e940f97ecb89152b3b527`, a échoué. Le journal du job 125947100922 signale : `RuntimeError: Origines du sacré : doublon du chapitre 576`, dans `scripts/build_navigation.py`, fonction `create_origins`. Le contrôle est pertinent et ne doit pas être simplement supprimé pour masquer la collision.

## Chronologie vérifiée par l'API GitHub — heures UTC

1. **13:24:39 — premier chapitre 576** : `chapitres/origines-du-sacre/576-bacs-peages-offrandes-passage.md` ; commit `d60e9ad69fc601054d5d08ca03925c6aabccaec9` ; blob constaté `e76d2173a4945356950bca8da81919e38f0b2a32`. Étude développée distinguant location journalière, péage, offrande et dépôt funéraire ; Hammurabi, Arthaśāstra, Manu, Aristophane et critique archéologique.
2. **13:27:10 — seconde version portant 576** : `chapitres/origines-du-sacre/576-payer-pour-passer-tarifs-bacs-offrandes.md` ; commit `d626e200d70c9d31728fa80fff5fb3be580f68bd` ; blob constaté `d77f816214658f55de0552780d7d6ab1439cdb83`. Variante sur un thème largement commun, avec développements complémentaires notamment sur Lucien, Strabon et Hérodote.
3. **13:27:13 — premier chapitre 577** : `chapitres/origines-du-sacre/577-monnaies-funeraires-charon-preuves-archeologiques.md` ; commit `dfdc11b96a9c31648e2b7c6f433f26ad213c91ad` ; blob constaté `6bb4226f9a9694b6110670ac92fd3c0ecc36540e`.
4. **13:29:20 — seconde étude portant 577, thème différent** : `chapitres/origines-du-sacre/577-naufrages-secours-divins-survivants.md` ; commit `621a1dd97a3da077c28e940f97ecb89152b3b527` ; blob constaté `2bafb933fc98157846fec27559a77cc0ededec09`. Étude des secours divins, de la responsabilité technique et de la sélection des récits de survivants ; Homère, Cicéron, Samothrace, Hammurabi, Manu, Jonas, récit égyptien du Naufragé et Nietzsche.

## Réconciliation à traiter avant de poursuivre la numérotation

Les opérations ci-dessous sont un plan de correction, **pas des opérations déjà réalisées**.

- Relire les quatre fichiers complets et l'état actuel de `main` : d'autres écritures peuvent avoir eu lieu depuis ce constat. Vérifier aussi `EDITORIAL_CONTINUITY.md`.
- Conserver la priorité chronologique du premier 576 et du premier 577, sauf décision éditoriale explicite déjà enregistrée ailleurs.
- Conserver intégralement la seconde version thématique de 576 dans une annexe ou une archive clairement identifiée, avec renvoi depuis le chapitre principal ; ne pas présenter deux traitements du même thème comme deux chapitres successifs artificiellement différents.
- Attribuer à l'étude distincte sur les naufrages le prochain numéro réellement libre après vérification. Le numéro 578 serait la suite logique de l'état constaté, mais **il n'est ni attribué ni réservé par ce document**.
- Avant tout déplacement impliquant une suppression d'ancien chemin, appliquer les conditions de sauvegarde de `EDITORIAL_CONTINUITY.md`, confirmer la nouvelle copie intégrale et conserver les anciennes références accessibles. Lire le SHA actuel avant chaque mise à jour ou suppression ; ne jamais utiliser les SHA ci-dessus sans contrôle de fraîcheur.
- Mettre à jour les titres, sous-sections, renvois précédent/suivant et éventuelles redirections de façon cohérente. Ne pas désactiver la protection contre les doublons dans le constructeur.
- Relancer et vérifier la construction, le catalogue, la recherche, le sitemap et le déploiement. Confirmer les URL HTTPS publiques avant d'affirmer la mise en ligne.

## Sujet préparé pour la suite

**Les calendriers du départ : saisons de navigation, jours favorables et décisions rituelles.** Son numéro doit être fixé après la réconciliation, pas déduit de l'ancien renvoi « chapitre 578 » qui subsiste dans le fichier sur les naufrages.

## Limites de la présente exécution

L'archivage GitHub des deux études rédigées est confirmé. Le conflit de numérotation est diagnostiqué mais n'est pas encore corrigé dans les fichiers. Le déploiement associé a échoué. Les deux URL publiques ont été interrogées, mais l'outil web n'a pas permis d'en vérifier le contenu ; cela ne prouve pas à lui seul leur absence. Aucun succès de publication publique n'est affirmé.
