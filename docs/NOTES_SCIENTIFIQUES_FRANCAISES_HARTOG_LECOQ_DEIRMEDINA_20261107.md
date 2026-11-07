# MYTHOS — Troisième lot de notes scientifiques françaises
**7 novembre 2026 — Nouvelle branche indépendante : `scientifique/auteurs-francais-hartog-lecoq-deirmedina-20261107`.**

## Objet et état

Ce lot enrichit **trois manuscrits existants** du corpus MYTHOS, en conservant leur numérotation, leur texte initial, leurs archives et toutes les reconstitutions. Il utilise des sources scientifiques publiées et des **notices institutionnelles** réellement consultées. Une référence à un ouvrage ne signifie pas qu'un auteur ou un organisme a évalué MYTHOS.

La branche part du commit `8f9366006b2b336db99f0c209e5a1ca717bbe73c` de `main`. Les PR antérieures [#159](https://github.com/Bobcribb/Bobcribb.github.io/pull/159) et [#212](https://github.com/Bobcribb/Bobcribb.github.io/pull/212) restent **distinctes** et ne sont ni réécrites ni fusionnées par ce lot.

| Corpus | Texte annoté | Publications contrôlées | Niveau de preuve et limites |
|---|---|---|---|
| Origines du sacré 685 — embaumement égyptien | `chapitres/origines-du-sacre/685-egypte-herodote-embaumement-saqqara-antiu-sefet-papyrus-rituel.md` | François Hartog, *Le Miroir d'Hérodote*, Gallimard, 1980 ; Mucem ; compte rendu *Revue des Études Grecques* (1981) | Cadre **historiographique** de la représentation de l'autre, non procédure d'embaumement attestée |
| Origines du sacré 689 — tombeaux achéménides | `chapitres/origines-du-sacre/689-cyrus-darius-tombeaux-pasargades-naqsh-rostam-magies-souverainete.md` | Pierre Lecoq, *Les Inscriptions de la Perse achéménide*, Gallimard, 1997 ; BnF ; *Encyclopaedia Iranica* ; UNESCO | Édition/traduction de la documentation royale ; distinguer DNa, DNb, matériaux et récits grecs |
| Comparatif MC-128 — peaux marquées | `chapitres/comparatif/volume-ccclv-mc-128-peaux-marquees-gebelein-deir-el-medina-herodote-pazyryk-otzi.md` | Guillemette Andreu-Lanoë et Dominique Valbelle, *Guide de Deir el-Médina*, IFAO, 2022 ; Dominique Valbelle, *Les Ouvriers de la tombe*, IFAO, 1985 ; IFAO, fouilles ; Austin et Gobeil, *BIFAO* 116 (2017) | **Ouvrages de contexte** social séparés de la **source archéologique** attestant des tatouages ; pas d'origine religieuse universelle démontrée |

## Sources institutionnelles et contrôles

1. François Hartog, *Le Miroir d'Hérodote. Essai sur la représentation de l'autre*, Gallimard, 1980 : [Mucem, notice d'exemplaire](https://mucem.org/notice/b/oai%3APMB%3A88642/) ; [Alain Le Boulluec, *REG* 94 (1981), 563–564, compte rendu sur Persée](https://www.persee.fr/doc/reg_0035-2039_1981_num_94_447_1302_t2_0563_0000_2). **Limite :** le compte rendu identifie l'orientation du livre, non le détail d'Hérodote II, 85–90 ; aucune page non consultée attribuée à Hartog.
2. Pierre Lecoq, *Les Inscriptions de la Perse achéménide*, Gallimard, 1997 : [éditeur Gallimard](https://www.cercle-enseignement.com/Ouvrages/Gallimard/L-aube-des-peuples/Les-Inscriptions-de-la-Perse-achemenide) ; [BnF](https://catalogue.bnf.fr/ark:/12148/cb35863815n). **Limite :** éditions et textes précis DNa/DNb à collationner avant toute nouvelle citation littérale.
3. [*Encyclopaedia Iranica* — Naqš-e Rostam](https://www.iranicaonline.org/articles/naqs-e-rostam/) ; [UNESCO — Pasargades](https://whc.unesco.org/en/list/1106). **Limite :** architecture et inscriptions de deux ensembles distincts, à ne pas fusionner.
4. Guillemette Andreu-Lanoë et Dominique Valbelle, *Guide de Deir el-Médina*, [IFAO, 2022](https://www.ifao.egnet.net/publications/catalogue/9782724708066/). **Limite :** guide institutionnel de site, non étude quantitative de tous les tatouages.
5. Dominique Valbelle, *Les Ouvriers de la tombe : Deir el-Médineh à l'époque ramesside*, [IFAO, 1985](https://www.ifao.egnet.net/publications/catalogue/9782724700183/). **Limite :** histoire sociale et des archives, non preuve de la signification de chaque marque corporelle.
6. [IFAO — Deir el-Médina, travaux de terrain et collections](https://www.ifao.egnet.net/archaeologie/deir-el-medina/) ; Anne Austin et Cédric Gobeil, « Embodying the Divine: A Tattooed Female Mummy from Deir el-Medina », *BIFAO* 116 (2017), p. 23–46, [IFAO, notice de publication](https://www.ifao.egnet.net/publications/catalogue/?nif=BIFAO116_art_03.pdf&nv=0). **Limite :** attestations de tatouages, interprétations religieuses soumises à discussion.

## Exigences préalables à toute fusion ou annonce publique

- Les liens, les années, les noms d'auteurs et les objets doivent être revérifiés dans la PR.
- S'assurer que le rendu Markdown des nouvelles notes ne brise ni les lecteurs HTML ni l'index.
- Respecter la charte graphique MYTHOS, la séparation des études philosophiques et des récits, les cas éditoriaux protégés, les identifiants et les médias.
- Contrôler les tests GitHub Actions, le générateur natif et le statut de publication publique HTTPS.
- Les sources de contexte **ne valent pas une collation intégrale** des ouvrages et les chercheurs ne sont pas présentés comme évaluateurs du site.
- **Aucune planification automatique ne doit être réactivée** ; exécution ponctuelle uniquement.

Programme général de révision : [issue n° 158](https://github.com/Bobcribb/Bobcribb.github.io/issues/158).
