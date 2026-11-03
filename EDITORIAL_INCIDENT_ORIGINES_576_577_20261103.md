# MYTHOS — Origines du sacré : conflit éditorial 576–577 du 3 novembre 2026

## Mise à jour de réconciliation — 3 novembre 2026

**Le blocage de génération a été corrigé et un déploiement GitHub a réussi.** Le constat initial ci-dessous est conservé comme historique, et ne décrit plus à lui seul l'état courant.

La priorité chronologique est maintenue : le chapitre canonique 576 est `576-bacs-peages-offrandes-passage.md` ; le chapitre canonique 577 est `577-monnaies-funeraires-charon-preuves-archeologiques.md`. La version parallèle `576-payer-pour-passer-tarifs-bacs-offrandes.md` est conservée comme complément documentaire non numéroté, sans perte de son contenu.

Une autre exécution a entre-temps enregistré les chapitres 578 (étapes et hébergement), 579 (rampes et mobilité), puis repris intégralement l'étude des naufrages sous **580**, chemin `chapitres/origines-du-sacre/580-naufrages-secours-divins-survivants.md`. Le titre et la note initiale de ce fichier ont été relus. **Ne pas attribuer de nouveau 578, 579 ou 580 à cette étude et ne pas la compter deux fois.** L'ancien chemin `577-naufrages-secours-divins-survivants.md` est une version historique conservée ; ses anciens repères internes ne créent pas un autre chapitre 577.

Le module `scripts/origines_reconciliation.py` conserve les quatre manuscrits originaux byte pour byte, vérifie leurs SHA-256 pendant la construction, distingue explicitement les deux anciennes collisions et laisse le contrôle des autres doublons actif. Il complète le sommaire avec les chapitres 491 et suivants et produit `catalog/origines-continuity.json`. Le branchement dans `scripts/build_native.py` a été confirmé par le commit `171cbe298c154caabb04e6bbe400ebf745b176f6`.

**Validation constatée :** workflow de publication `41649996304`, terminé avec `conclusion: success` ; validation du générateur `41649996239`, succès ; audit `41649996336`, succès. Le fichier `catalog/origines-continuity.json` a ensuite été relu sur `main` : il recensait les numéros jusqu'à 580 avec les deux anciennes versions classées séparément. Le succès de ces contrôles ne remplace pas une vérification indépendante des URL publiques des nouvelles livraisons.

Après cette réconciliation, deux nouvelles études complètes ont été enregistrées :

- **581 — Les calendriers du départ : saisons de navigation, jours favorables et décisions rituelles** : `chapitres/origines-du-sacre/581-calendriers-depart-saisons-jours-favorables.md`, commit `ad2f672f7a59b84c02f741190469415ffd326ae9`.
- **582 — Attendre le signe : éclipses, sacrifices de départ et responsabilité de la décision** : `chapitres/origines-du-sacre/582-attendre-signe-eclipse-sacrifices-decision.md`, commit `51cfc919aec1b1b189d70a6b35bf2b91a7309547`.

**Suite annoncée :** 583, « Qui a le droit d'interpréter ? Désaccords entre devins, contrôle de l'expertise et choix collectifs ». Ce numéro doit encore être vérifié à la prochaine exécution, car plusieurs rédactions peuvent intervenir simultanément. Les quatre textes de l'incident n'ont été ni supprimés ni abrégés par cette correction.

---

## Constat initial conservé — état avant réconciliation

La production de cette exécution avait vérifié un dernier chapitre 575 avant rédaction. Deux rédactions parallèles ont ensuite créé des fichiers portant les mêmes numéros 576 et 577. Les quatre textes sont conservés intégralement. Aucun n'a été supprimé, écrasé ou fusionné pendant le constat. Les fichiers créés dans cette exécution ont été relus sur `main` après leurs commits.

Le déploiement de publication n° 41644763105, associé au commit `621a1dd97a3da077c28e940f97ecb89152b3b527`, a échoué. Le journal du job 125947100922 signale : `RuntimeError: Origines du sacré : doublon du chapitre 576`, dans `scripts/build_navigation.py`, fonction `create_origins`. Le contrôle est pertinent et ne doit pas être simplement supprimé pour masquer la collision.

## Chronologie vérifiée par l'API GitHub — heures UTC

1. **13:24:39 — premier chapitre 576** : `chapitres/origines-du-sacre/576-bacs-peages-offrandes-passage.md` ; commit `d60e9ad69fc601054d5d08ca03925c6aabccaec9` ; blob constaté `e76d2173a4945356950bca8da81919e38f0b2a32`. Étude développée distinguant location journalière, péage, offrande et dépôt funéraire ; Hammurabi, Arthaśāstra, Manu, Aristophane et critique archéologique.
2. **13:27:10 — seconde version portant 576** : `chapitres/origines-du-sacre/576-payer-pour-passer-tarifs-bacs-offrandes.md` ; commit `d626e200d70c9d31728fa80fff5fb3be580f68bd` ; blob constaté `d77f816214658f55de0552780d7d6ab1439cdb83`. Variante sur un thème largement commun, avec développements complémentaires notamment sur Lucien, Strabon et Hérodote.
3. **13:27:13 — premier chapitre 577** : `chapitres/origines-du-sacre/577-monnaies-funeraires-charon-preuves-archeologiques.md` ; commit `dfdc11b96a9c31648e2b7c6f433f26ad213c91ad` ; blob constaté `6bb4226f9a9694b6110670ac92fd3c0ecc36540e`.
4. **13:29:20 — seconde étude portant 577, thème différent** : `chapitres/origines-du-sacre/577-naufrages-secours-divins-survivants.md` ; commit `621a1dd97a3da077c28e940f97ecb89152b3b527` ; blob constaté `2bafb933fc98157846fec27559a77cc0ededec09`. Étude des secours divins, de la responsabilité technique et de la sélection des récits de survivants ; Homère, Cicéron, Samothrace, Hammurabi, Manu, Jonas, récit égyptien du Naufragé et Nietzsche.

## Réconciliation à traiter avant de poursuivre la numérotation — plan initial archivé

Les opérations ci-dessous étaient un plan de correction, **pas des opérations déjà réalisées lors du constat initial**. Leur mise en œuvre et les changements intervenus depuis sont décrits en tête de ce fichier.

- Relire les quatre fichiers complets et l'état actuel de `main` : d'autres écritures peuvent avoir eu lieu depuis ce constat. Vérifier aussi `EDITORIAL_CONTINUITY.md`.
- Conserver la priorité chronologique du premier 576 et du premier 577, sauf décision éditoriale explicite déjà enregistrée ailleurs.
- Conserver intégralement la seconde version thématique de 576 dans une annexe ou une archive clairement identifiée, avec renvoi depuis le chapitre principal ; ne pas présenter deux traitements du même thème comme deux chapitres successifs artificiellement différents.
- Attribuer à l'étude distincte sur les naufrages le prochain numéro réellement libre après vérification. Le numéro 578 serait la suite logique de l'état constaté, mais **il n'est ni attribué ni réservé par ce document**.
- Avant tout déplacement impliquant une suppression d'ancien chemin, appliquer les conditions de sauvegarde de `EDITORIAL_CONTINUITY.md`, confirmer la nouvelle copie intégrale et conserver les anciennes références accessibles. Lire le SHA actuel avant chaque mise à jour ou suppression ; ne jamais utiliser les SHA ci-dessus sans contrôle de fraîcheur.
- Mettre à jour les titres, sous-sections, renvois précédent/suivant et éventuelles redirections de façon cohérente. Ne pas désactiver la protection contre les doublons dans le constructeur.
- Relancer et vérifier la construction, le catalogue, la recherche, le sitemap et le déploiement. Confirmer les URL HTTPS publiques avant d'affirmer la mise en ligne.

## Sujet préparé pour la suite — annonce initiale conservée

**Les calendriers du départ : saisons de navigation, jours favorables et décisions rituelles.** Son numéro devait être fixé après la réconciliation, pas déduit de l'ancien renvoi « chapitre 578 » qui subsiste dans le fichier sur les naufrages. Il est désormais enregistré comme chapitre 581, ainsi que documenté plus haut.

## Limites de l'exécution initiale — historique

L'archivage GitHub des deux études rédigées était confirmé. Le conflit de numérotation était diagnostiqué mais n'était pas encore corrigé dans les fichiers. Le déploiement associé avait échoué. Les deux URL publiques avaient été interrogées, mais l'outil web n'avait pas permis d'en vérifier le contenu ; cela ne prouvait pas à lui seul leur absence. Aucun succès de publication publique n'était affirmé lors de ce constat.
