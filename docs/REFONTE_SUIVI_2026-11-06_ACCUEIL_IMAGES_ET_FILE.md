# MYTHOS — Refonte : pertinence iconographique de l’accueil et continuité des manuscrits

**Séance du 6 novembre 2026**, dépôt `Bobcribb/Bobcribb.github.io`, branche `main`, site `https://bobmythos.fr`.

## A. Lecture des règles et inventaire, avant toute écriture

État initial relu sur `main` : `0ca6601b56cc8eefb887e53a28e7bdadcfee6224`. Fichiers lus : `AGENTS.md`, `docs/PUBLICATION_CONCURRENTE.md`, `editorial/numbering.json`, `editorial/holds.json`, `scripts/recent_studies.py`, les sources scientifiques récentes, le générateur du site et le catalogue `scripts/editorial_media.json`. L'arbre du dépôt contenait 5 563 entrées à cet instant.

L'inspection exhaustive des sources Markdown sous `chapitres/` n'a identifié **aucun manuscrit numéroté sans lecteur HTML correspondant dans le dépôt**. Les 18 sources originales de l'Énéide, précédemment mal distribuées, sont désormais accessibles sur HTTPS : `/corpus/philosophie/eneide/00-introduction.md`, `/corpus/philosophie/eneide/17-reperes-et-sources.md` et `/philosophie-eneide.html` ont été effectivement ouverts et contrôlés ; sources, bibliographie et lecteur long présents.

Au contrôle éditorial précis, la file présentait **503 JSON** sous `editorial/inbox/`, **478 allocations reçues** et **23 demandes en retenue**. Deux fichiers n'avaient ni reçu ni retenue :
- `9b4d6a70-8ef2-4b8c-a4d3-202611060755.json` : étude intégrale MC-096, **58 497 caractères Markdown**, collection `comparatif`, sur les ombres du divin (Égypte, Mésopotamie, Israël, Grèce et Inde), avec sources et bibliographie, correctement déposée sous un UUID fixe mais **non attribuée à cet instant**. Ne pas lui attribuer manuellement de numéro ni créer une seconde demande.
- `20261105-mc-069-souffle-vent-vie-philologie.json` : manuscrit MC-069 intégral à identifiant historique non standard, toujours sans reçu, nécessitant la réconciliation du circuit transactionnel, et non un nouveau numéro présumé.

Les autres manuscrits intégrals accessibles ont déjà une attribution ou une retenue ; les anciens brouillons Drive privés ne sont pas autorisés à un transfert automatique. **Aucune première publication universitaire ne peut être attribuée à cette séance avant reçu GitHub Actions et déploiement.** La demande MC-096 est déjà enregistrée dans la file : les commits de refonte déclenchent le pipeline existant, sans duplication, mais ne constituent pas une preuve de publication.

## A bis. Cinq textes intégrals désormais attribués et accessibles en HTTPS

La relecture des reçus `editorial/numbering.json` et l'ouverture directe des cinq lecteurs ont permis de **confirmer leur publication effective**, alors qu'ils figuraient encore parmi les demandes à traiter dans l'état de suivi précédent :

| Série et cote confirmée | Sujet intégral | Texte public contrôlé |
| --- | --- | --- |
| Origines du sacré, chap. **718** | Nabta Playa : sépultures bovines et paysage rituel du Sahara | [Lecteur 718](https://bobmythos.fr/chapitres/origines-du-sacre/718-nabta-playa-cercles-pierres-bovins-calendrier-pastoralisme-sahara-neolithique/), environ 36 200 caractères extraits, bibliographie présente |
| Origines du sacré, chap. **719** | Gebel Ramlah : nécropoles, nourrissons, ocre et feu | [Lecteur 719](https://bobmythos.fr/chapitres/origines-du-sacre/719-gebel-ramlah-necropoles-nourrissons-ocre-feu-pastoralisme-neolithique-sahara/), environ 41 200 caractères, bibliographie présente |
| Tragédies, vol. **CCLXII (262)** | Achéos d’Érétrie, *Aithon* satyrique | [Lecteur 262](https://bobmythos.fr/chapitres/tragedies/volume-cclxii-acheos-eretrie-aithon-satyrique-faim-vin-odyssee-erysichthon/), environ 59 200 caractères, bibliographie présente |
| Comparatif, vol. **CCLXXXVIII (288)** | *Lysistrata* : les deux chœurs, eau, feu, antagonisme et réconciliation | [Lecteur 288](https://bobmythos.fr/chapitres/comparatif/volume-cclxxxviii-lysistrata-deux-choeurs-eau-feu-antagonisme-reconciliation-411/), environ 95 300 caractères, bibliographie présente |
| Comparatif, vol. **CCXC (290)** | MC-094 : les clefs du sacré, Inanna, Hécate, Janus | [Lecteur 290](https://bobmythos.fr/chapitres/comparatif/volume-ccxc-mc-094-clefs-du-sacre-inanna-hecate-lagina-janus-isaie-apocalypse/), environ 47 500 caractères, bibliographie présente |

Ces cinq premières publications ont été **réalisées par le système éditorial GitHub Actions**, pas par les commits graphiques de cette séance. Elles sont désormais confirmées dans le registre et sur le site public ; les longueurs ci-dessus sont les textes extraits du lecteur HTTPS, pas les octets des sources Markdown. Les numéros ont été attribués automatiquement et leurs études intégrales ne sont pas redéposées.

## B. Anomalie de présentation démontrée

Le panneau public `/#home-etudes-recentes` affichait cinq photographies de collection génériques, notamment une chambre funéraire d'Ounas devant la dernière étude du Sahara (Tadrart Acacus) et une tablette de l'`Enūma eliš` devant un volume comparatif sur les *Oiseaux* d'Aristophane. Les légendes préviennent qu'il s'agit de repères généraux, mais l'effet visuel entretient une association indue entre photographie et sujet de l'étude.

## C. Corrections pérennes enregistrées

- **`scripts/recent_study_media.py`** : module de sélection restrictive par titre/slug, à partir des notices, chemins et crédits déjà inscrits dans `scripts/editorial_media.json`. Les documents ne sont utilisés que dans leur périmètre exact ; lorsqu'aucune illustration suffisamment pertinente n'est disponible, la carte reste **sans image**, sans masquer le texte.
- **`scripts/recent_studies.py`** : le générateur de l'accueil utilise ces résultats, conserve les cinq URL canoniques et les backlinks réciproques, et ajoute des crédits documentaires en dehors des liens de cartes afin d'éviter les liens HTML imbriqués. Les sources et datations des objets sont consultables depuis le sommaire.
- **`assets/mythos-museum.css`** : encart de crédits anthracite / ivoire / or, focus clavier, cartes sans image au bord supérieur doré, grille deux colonnes puis une seule sur mobile ; bannière statue grecque à gauche et temple à droite inchangée.
- **`tests/test_recent_studies.py`** : ancien test de photo générique corrigé : une tragédie sur Triptolème ne doit pas automatiquement recevoir le théâtre d'Épidaure.
- **`tests/test_recent_study_media_20261106.py`** : vérification des médias sourcés (Athéna, Delphes, comédie ancienne), de l'abstention pour les sujets sans média, des cinq collections, de l'absence de doublons dans les renvois, de l'idempotence et de la préservation des Markdown.

**Cas concrets :** le chapitre ODS 721 (Tadrart Acacus) cesse d'utiliser l'image funéraire égyptienne ; le chapitre grec 454 (Athéna Chalkioikos) peut montrer un vase grec représentant Athéna, avec avertissement de ne pas le confondre avec le culte spartiate ; le volume tragique 263 utilise un document du sanctuaire de Delphes ; le volume comparatif 291 sur les *Oiseaux* utilise des figurines d'acteurs comiques comme document de contexte **non représentatif de cette scène**.

## D. Commits de la séance

1. `1e23a0806603db1cd8d19803510a46f6b7cd46fa` — module d'images contextualisées.
2. `6f5298a6566b7b9af444d3155271b11a6dafdb11` — raccordement au panneau des études récentes et crédits.
3. `2bf0c892077f86f506466a64ad2a71c1899a377a` — test mis à jour pour refuser l'iconographie générique.
4. `40d19d96f004e6c5feea9d7d51d00eef3b0f6ee2` — carte sans image de remplissage.
5. `6a5ee735b2fff1d622352921e5fd63a065735355` — CSS responsive et crédits d'objets.
6. `a0cfd2113a2dc806cf6add5807e681e80ed53275` — tests additionnels de pertinence et conservation.

## E. Vérifications et limites

La validation GitHub Actions `42180286936` a d'abord échoué sur le **test historique attendant encore l'ancienne photo générique**. Ce test a été corrigé par le commit `2bf0c892`. Une exécution ultérieure, `42180649903`, avait déjà réussi **les tests unitaires et le contrôle iconographique**, tandis que la reconstruction complète restait en cours au dernier contrôle de cette séance. La publication liée au commit `6a5ee735` (`42180486601`) était également en cours. Les autres automatisations horaires poursuivent leurs propres commits.

**Dernière vérification HTTPS :** le manifeste public `/catalog/publication-verification.json` indiquait encore `source_commit=db016f6cbc0bec783e369a1e2874f0c6a1883aa6`, `github_run_id=42175517252`, 1 604 documents, 27 archives et 110 médias. Le HTML public des cartes montrait encore les cinq photographies génériques, sans panneau de crédits. Ce n'est **pas** une confirmation de déploiement des changements décrits ici.

Pour clore, vérifier une publication réussie ultérieure, comparer son `source_commit` au commit qui contient ces modifications, puis vérifier `/#home-etudes-recentes` (cartes et crédits), navigation à 320 px, accessibilité clavier et URLs des monographies. Ne pas déclarer une première publication de MC-096 sans reçu, lecteur et contrôle HTTPS.

**Conservation :** aucune source universitaire, fichier d'archive, numéro, reçu, demande `editorial/inbox/`, retenue, définition de workflow ou planification horaire MYTHOS n'a été modifié durant cette séance.
