# MYTHOS — Mise à jour de continuité : chapitres 582–584 et compléments intégraux

**État établi le 3 novembre 2026, après le correctif `3f5174598ede60f41d0623c28ef9ef083b579c3b`.** Cette note complète et, pour les attributions 583/584 et les annonces de suite, rectifie les états intermédiaires de `EDITORIAL_INCIDENT_ORIGINES_576_577_20261103.md`. Aucun manuscrit original n'est supprimé, abrégé ou réécrit par cette réconciliation.

## Règle appliquée

Le premier commit confirmé d'un numéro conserve sa priorité. Les études parallèles postérieures restent intégralement disponibles comme compléments, sans compter deux fois le numéro et sans être déplacées vers un numéro déjà attribué. Le contrôle des doublons inconnus reste actif : on ne désactive pas cette protection pour faire passer un déploiement.

## Chapitres canoniques et compléments

### Chapitre 582

- Canonique : `chapitres/origines-du-sacre/582-attendre-signe-eclipse-sacrifices-decision.md`, commit `51cfc919aec1b1b189d70a6b35bf2b91a7309547`, création **14:16:21 UTC**, vérifiée par l'API Git.
- Complément intégral : `chapitres/origines-du-sacre/582-presages-depart-autorite-deliberation.md`, étude « Partir malgré les signes ? Devins, commandement et délibération collective », commit `8dd05e09e0432d18de687839eacda9b9300536aa`, création **14:25:03 UTC**, blob relu `34d18cdd68b3fb26850cf7e9b832e59f3c86c28e`.

### Chapitre 583

- Canonique : `chapitres/origines-du-sacre/583-interpreter-oracles-expertise-controverse.md`, commit `01a8e2953c9bce78fc01b1104374eb0ac42cf94b`, création **14:23:22 UTC**. L'historique du chemin retournait ce seul commit lors du contrôle. Blob constaté : `0bca055c0064b17dcce55c6cecf8c69be611413c`.
- Complément intégral : `chapitres/origines-du-sacre/583-croire-prevoir-instituer-xunzi-ciceron-nietzsche.md`, étude « Croire, prévoir, instituer : Xunzi, Cicéron et Nietzsche devant les rites et les signes », commit `12016f45dbf367e70792fc04da7e61ab4412d0eb`, création **14:32:20 UTC**, blob relu `14b9fa0a48f75292b895b9e9ea4fa0597477f322`.

Les deux compléments comprennent chacun dix-sept sections développées, les sources primaires précises et une bibliographie assortie de limites de consultation. Ils constituent deux études nouvelles conservées, **pas deux numéros canoniques supplémentaires**. Leur texte Markdown garde sa provenance ; le rendu du site et le catalogue affichent explicitement leur statut de complément. Les anciens renvois de suite dans ces manuscrits reflètent l'état de rédaction et ne doivent pas supplanter la présente réconciliation.

### Chapitre 584 déjà présent

`chapitres/origines-du-sacre/584-archives-presage-lamelles-os-argile.md` : **Les archives du présage : lamelles, os, argile et mémoire matérielle de l'incertitude**, tome XLVI. Titre et ouverture relus sur `main`, blob `638cdf41eda695b78925557ae1dff5c5000b2149`, taille constatée 28 712 octets.

Ce numéro ne doit donc pas être réattribué au sujet « Cartes, itinéraires et savoirs du passage », annoncé antérieurement. Ce sujet reste une proposition de travail, **sans réservation de numéro**. Avant toute suite, inspecter de nouveau les fichiers de la série : d'autres exécutions peuvent avoir progressé.

## Correction du constructeur

Le commit `3f5174598ede60f41d0623c28ef9ef083b579c3b` de `scripts/origines_reconciliation.py` ajoute explicitement la collision connue de 583 aux collisions 576, 577 et 582 déjà documentées. Il ne modifie aucun texte source. Il :

- maintient un seul fichier canonique par numéro connu ;
- conserve les deux études complémentaires en intégralité à leur adresse, **sans redirection forcée vers un texte différent** ;
- ajoute les liens des compléments au portail et depuis le chapitre canonique ;
- contrôle dix fichiers sources par SHA-256 avant et après la génération ;
- laisse échouer tout nouveau doublon non explicitement réconcilié ;
- maintient les deux redirections historiques vers l'annexe de 576 et la reprise des naufrages en 580.

Six contrôles locaux ont réussi sur le module : conservation des dix sources de test ; unicité canonique ; redirections locales et conservation du corps HTML historique ; affichage intégral et liens des deux compléments ; refus d'un doublon inconnu ; détection d'une modification de manuscrit et refus d'un registre de redirections inattendu. Ces tests utilisent des données de test et **ne sont pas une preuve d'un déploiement réel**.

## Publication : faits confirmés et limite

Le workflow `41655529519` a échoué dans le job `125984676037`. Les journaux ont été lus via `fetch_workflow_job_logs` et identifient précisément `RuntimeError: Origines du sacré : doublon du chapitre 583`. Cette exécution précède le correctif `3f5174598ede60f41d0623c28ef9ef083b579c3b`.

Le workflow surveille désormais les modifications de `scripts/origines_reconciliation.py` et de `EDITORIAL_REDIRECTS.json`, grâce au commit `a12837b0d6e8621fe4cccdf7c688760ea26d2e1d`. Le correctif suivant doit donc provoquer une nouvelle construction. Il faut en lire le résultat et vérifier `catalog/origines-continuity.json`, les pages générées, puis les URL HTTPS avant d'affirmer la publication publique.

**À la création de cette note : fichiers intégraux enregistrés et relus ; correction enregistrée ; publication publique des compléments non encore confirmée.** Aucun succès antérieur, aucune présence d'un ancien HTML et aucun test local ne doit être présenté comme cette confirmation.
