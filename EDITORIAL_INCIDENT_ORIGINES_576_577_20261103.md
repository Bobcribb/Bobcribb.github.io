# MYTHOS — Origines du sacré : conflits éditoriaux et réconciliation du 3 novembre 2026

## Actualisation prioritaire — continuité jusqu'au chapitre 583

Cette section complète les états historiques conservés plus bas. La priorité du premier commit confirmé est appliquée aux numéros déjà attribués. Aucun manuscrit original des collisions n'a été supprimé ou abrégé.

- **576 canonique** : `576-bacs-peages-offrandes-passage.md`. La version parallèle `576-payer-pour-passer-tarifs-bacs-offrandes.md` demeure intacte et a été copiée intégralement dans `annexe-576-payer-pour-passer-variante.md`, commit `62f073574ca4fc324b8a13ac7fb2b18198a694ab`. Elle n'est pas comptée comme un autre chapitre.
- **577 canonique** : `577-monnaies-funeraires-charon-preuves-archeologiques.md`.
- **578 et 579** : les études sur l'hébergement et les rampes conservent leurs numéros et leur texte.
- **580** : reprise intégrale du dossier des naufrages, `580-naufrages-secours-divins-survivants.md`, commit `afa16665033925d4c89c4f449bef8233969e604c`, blob relu `659fbcb2865c9150be284c4f130465643a744dc6`. Cette reprise n'est pas une nouvelle rédaction à compter deux fois.
- **581** : `581-calendriers-depart-saisons-jours-favorables.md`, commit `ad2f672f7a59b84c02f741190469415ffd326ae9`, blob relu `4a3d1d6e2f96eae7942bab776d19115c54560fb7`. Une tentative concurrente de création au même chemin a échoué sans écrasement ; la première version a été conservée.
- **582 canonique** : `582-attendre-signe-eclipse-sacrifices-decision.md`, commit `51cfc919aec1b1b189d70a6b35bf2b91a7309547`, daté par l'API Git de **14:16:21 UTC**.
- **Complément intégral de 582** : `582-presages-depart-autorite-deliberation.md`, commit `8dd05e09e0432d18de687839eacda9b9300536aa`, daté de **14:25:03 UTC**, blob relu `34d18cdd68b3fb26850cf7e9b832e59f3c86c28e`. Son ancien numéro dans le manuscrit ne constitue pas une seconde attribution. Le constructeur l'affiche comme « Complément du chapitre 582 — Devins, commandement et délibération collective », conserve son corps intégral à son adresse et l'exclut uniquement du comptage canonique. Il reste accessible dans le portail et depuis le premier 582 ; il n'est pas redirigé de force vers un autre texte.
- **583** : `583-croire-prevoir-instituer-xunzi-ciceron-nietzsche.md`, nouvelle étude « Croire, prévoir, instituer : Xunzi, Cicéron et Nietzsche devant les rites et les signes », commit `12016f45dbf367e70792fc04da7e61ab4412d0eb`, blob relu `14b9fa0a48f75292b895b9e9ea4fa0597477f322`.

Le registre `EDITORIAL_REDIRECTS.json`, commit `86c1ddd9e7f1e15cd6c68e6368b9a962c502d387`, conserve les deux redirections des anciennes adresses 576/577 vers l'annexe 576 et le chapitre 580. Le correctif `scripts/origines_reconciliation.py`, commit `c7c35072b468cdbfd2ab39a241ff2b81c246e6ab`, ajoute uniquement la collision connue de 582 à la réconciliation. Le contrôle des autres doublons reste actif. Huit sources intégrales sont contrôlées par SHA-256 avant et après la génération ; le rapport `catalog/origines-continuity.json` doit être vérifié après le prochain déploiement réussi.

**Tests locaux réalisés sur le module :** conservation des huit sources ; unicité des numéros canoniques ; redirections locales 576/577 ; affichage intégral du complément 582 sans redirection ; rejet des doublons inconnus ; détection d'une modification de source ; rejet d'un registre de redirection inattendu. Ces tests ne sont pas une preuve de déploiement public.

**État de publication au moment de cette note :** les commits et les lectures des nouveaux fichiers sont confirmés. Le workflow `41654672558`, associé au commit 583 antérieur à la correction de la collision 582, a échoué. Son résultat ne permet pas de conclure sur le correctif ultérieur `c7c35072b468cdbfd2ab39a241ff2b81c246e6ab`. Un succès ancien ou local ne doit pas être présenté comme la publication HTTPS des derniers textes.

**Déclenchement corrigé :** le workflow de publication ne surveillait pas le nouveau module de réconciliation. Le commit `a12837b0d6e8621fe4cccdf7c688760ea26d2e1d` ajoute `scripts/origines_reconciliation.py` et `EDITORIAL_REDIRECTS.json` aux chemins déclencheurs, sans changer les autres contrôles. La nouvelle exécution `41655529519` a effectivement commencé ; son état était `in_progress` lors du contrôle. Les tentatives d'ouverture HTTPS des deux nouvelles pages n'ont pas permis à l'outil web d'en lire le contenu ; cela ne constitue pas à soi seul une preuve de leur absence.

**Prochain sujet : 584 — Cartes, itinéraires et savoirs du passage : représenter une route sans la parcourir.** Vérifier à nouveau le dépôt avant toute création : une attribution annoncée ne constitue pas une réservation atomique. Ne pas recréer les numéros 580–583 ni traiter le complément de 582 comme un nouveau numéro. Les annonces de suite 583 conservées dans les états intermédiaires ci-dessous sont historiques.

---

## État intermédiaire de réconciliation — 3 novembre 2026

**Le blocage de génération initial avait été corrigé et un déploiement GitHub avait réussi.** Le constat initial ci-dessous est conservé comme historique ; les vérifications de cet état intermédiaire ne décrivent pas à elles seules les derniers commits.

La priorité chronologique est maintenue : le chapitre canonique 576 est `576-bacs-peages-offrandes-passage.md` ; le chapitre canonique 577 est `577-monnaies-funeraires-charon-preuves-archeologiques.md`. La version parallèle `576-payer-pour-passer-tarifs-bacs-offrandes.md` est conservée comme complément documentaire non numéroté, sans perte de son contenu.

Une autre exécution a entre-temps enregistré les chapitres 578 (étapes et hébergement), 579 (rampes et mobilité), puis repris intégralement l'étude des naufrages sous **580**, chemin `chapitres/origines-du-sacre/580-naufrages-secours-divins-survivants.md`. Le titre et la note initiale de ce fichier ont été relus. **Ne pas attribuer de nouveau 578, 579 ou 580 à cette étude et ne pas la compter deux fois.** L'ancien chemin `577-naufrages-secours-divins-survivants.md` est une version historique conservée ; ses anciens repères internes ne créent pas un autre chapitre 577.

Le module `scripts/origines_reconciliation.py` conserve les quatre manuscrits originaux byte pour byte, vérifie leurs SHA-256 pendant la construction, distingue explicitement les deux anciennes collisions et laisse le contrôle des autres doublons actif. Il complète le sommaire avec les chapitres 491 et suivants et produit `catalog/origines-continuity.json`. Le branchement dans `scripts/build_native.py` a été confirmé par le commit `171cbe298c154caabb04e6bbe400ebf745b176f6`.

**Validation constatée à cet état intermédiaire :** workflow de publication `41649996304`, terminé avec `conclusion: success` ; validation du générateur `41649996239`, succès ; audit `41649996336`, succès. Le fichier `catalog/origines-continuity.json` a ensuite été relu sur `main` : il recensait les numéros jusqu'à 580 avec les deux anciennes versions classées séparément. Le succès de ces contrôles ne remplace pas une vérification indépendante des URL publiques des nouvelles livraisons.

Après cette réconciliation, deux nouvelles études complètes ont été enregistrées :

- **581 — Les calendriers du départ : saisons de navigation, jours favorables et décisions rituelles** : `chapitres/origines-du-sacre/581-calendriers-depart-saisons-jours-favorables.md`, commit `ad2f672f7a59b84c02f741190469415ffd326ae9`.
- **582 — Attendre le signe : éclipses, sacrifices de départ et responsabilité de la décision** : `chapitres/origines-du-sacre/582-attendre-signe-eclipse-sacrifices-decision.md`, commit `51cfc919aec1b1b189d70a6b35bf2b91a7309547`.

**Suite annoncée à cet état intermédiaire :** 583, « Qui a le droit d'interpréter ? Désaccords entre devins, contrôle de l'expertise et choix collectifs ». Ce numéro devait encore être vérifié à l'exécution suivante, plusieurs rédactions pouvant intervenir simultanément. Il est désormais attribué au dossier comparatif indiqué en tête de cette note. Les quatre textes de l'incident n'ont été ni supprimés ni abrégés par la correction.

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
