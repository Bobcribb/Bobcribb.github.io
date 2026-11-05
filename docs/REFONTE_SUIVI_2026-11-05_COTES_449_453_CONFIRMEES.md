# MYTHOS — Cotes 449–453 et conservation des études intégrales

**5 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche
`main`. `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` consultés
avant les modifications.

## Première publication universitaire désormais confirmée

Le workflow GitHub Actions **42052421794** a réussi. Le reçu public
`https://bobmythos.fr/catalog/publication-verification.json` indique
**1 565 documents**, **27 archives** et **110 médias** ; sa source est
`bd79dae1a0d6a1140f9d1d80e1fe1ad0defb4fb6`.

Entre le contrôle précédent et cette publication, **26 manuscrits déjà
soumis** ont reçu une attribution transactionnelle, sans création d'UUID
par le présent chantier : **9 Origines du sacré** (698–706), **5 études de
l'encyclopédie grecque** (449–453), **4 comédies** (118–121) et
**8 comparatifs** (268–275). Les premières publications de chapitres
449–453 ont été consultées individuellement en HTTPS : tous possèdent
leur texte long et leur bibliographie.

## Correction de notices de statut devenues périmées

Les cinq manuscrits Markdown (449 Athéna Chalkioikos, 450 Trophonios,
451 Apollon Isménios, 452 Hélène et Ménélas au Ménélaion, 453 Apollon
Amyklaios) contenaient encore des phrases rédigées avant attribution,
par exemple « variable éditoriale » ou « sans numéro canonique ».
Ces indications sont remplacées par les **cotes effectivement enregistrées
dans `editorial/numbering.json`**. Les historiques de demande restent
présents dans `editorial/inbox/`.

Les cinq sources ont été comparées à leurs demandes JSON d'origine
après substitution régulière des variables ; elles étaient initialement
identiques. La correction a changé exactement **9 lignes de notices**
sur les cinq sources, sans ajout ni suppression de ligne :
449 (5, 336), 450 (7, 595), 451 (7, 513), 452 (5, 318), 453 (5).
**Toutes les autres lignes, y compris l'intégralité des analyses,
sources primaires et bibliographies, demeurent strictement inchangées.**

Le contrôle permanent
`tests/test_greek_canonical_notices_449_453_20261105.py`
vérifie les UUID, les empreintes SHA-256 des demandes et des sources
initiales, les reçus, les fichiers HTML et les 9 seules lignes
autorisées à changer. Aucun registre, manuscrit original, archive,
workflow, domaine ou automatisation horaire n'est modifié.

La réussite de la **publication initiale des 26 chapitres** ne doit
pas être confondue avec le déploiement ultérieur de ces corrections.
Le commit qui contient les notices corrigées doit encore passer les
tests puis être constaté sur le domaine HTTPS.
