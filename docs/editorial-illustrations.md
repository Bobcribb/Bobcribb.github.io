# Illustrations éditoriales — correction du 4 novembre 2026

## Règle de publication

Les deux distributeurs automatiques de `build_native.py` et de
`build_navigation.py` sont remplacés par `scripts/editorial_illustrations.py`.
Toutes les collections partagent la même règle : seul un sujet explicite du
titre du chapitre ou de son propre slug permet de choisir un média. Les noms
des collections, les menus, les paragraphes comparatifs et les anciennes
galeries ne servent pas de critères. Il n'y a plus de rotation par chemin ni
de collection grecque par défaut.

`scripts/editorial_media.json` référence 56 médias locaux et les notices
documentées déjà présentes dans les articles du dépôt. Chaque entrée conserve
son texte alternatif, sa légende, ses crédits, les liens de provenance et de
droits, et la page d'où la notice a été reprise. Le commit d'origine est
enregistré dans le catalogue. La sélection conserve les réserves des notices
(réception moderne, identification discutée, photographie de vestiges, etc.).

Une notice ne s'applique pas à toute une civilisation. Ainsi, le papyrus de
Derveni est sélectionnable pour Derveni, le relief de Behistun pour Behistun,
et l'hydrie de Médée pour Médée. Le Mithras romain n'est pas automatiquement
assimilé au Mithra iranien. Une image manquante est omise sans remplacement.

## Cas signalés et conservation

- **471 — Inde, yuga et calendriers** : aucune galerie automatique ; aucun
  document directement adapté n'est présent dans la sélection locale.
- **462 — Égypte, sistre et Hathor** : même traitement ; le papyrus d'Ani et
  la chambre d'Ounas ne sont pas des illustrations du sistre.
- Les anciennes galeries générées sont retirées du rendu, y compris celles
  recopiées dans les HTML historiques. Les figures, notes et études rédigées
  à l'intérieur des articles restent intactes.
- Au maximum deux documents sont ajoutés, sans répéter une image déjà dans
  l'article (y compris ses variantes avec paramètres ou adresses historiques).
- Les vignettes génériques des 27 tomes ont été retirées du portail des
  Origines du sacré. Une céramique grecque ne doit pas illustrer Hohle Fels,
  ni Mycènes la préhistoire du sacré. Les 27 titres et liens sont conservés.

## Vérifications

```sh
python -m unittest discover -s scripts -p 'test_editorial_illustrations.py' -v
python scripts/build_native.py
python scripts/validate_publication.py
python scripts/audit_integrity.py
```

Treize tests couvrent les deux signalements, les autres collections, les
titres Unicode, les limites de mots, la distinction Mithra/Mithras, les
médias absents, les doublons, les anciens HTML, l'idempotence et la
conservation des notes ainsi que du menu. Le nouveau graphisme conserve ses
couvertures décoratives uniquement pour une liste de portails nommés : une
carte de chapitre ne reçoit jamais leur image par héritage de collection ni
le cratère de Derveni par défaut.

Sur la reconstruction comparée du commit `871b5333c2faadcba16b97b1a3b6694482052449`,
1 062 corps d'articles restent identiques après sérialisation HTML. Seuls le
portail des Origines (vignettes retirées) et le catalogue théâtral généré
(contenu textuel inchangé) diffèrent. L'audit de cette reconstruction
vérifie 110 médias et 1 078 entrées, sans erreur ni avertissement.
Les chapitres 471, 462 et le volume CL sur Médée ont été contrôlés visuellement
dans le navigateur, avec chargement effectif de l'hydrie et affichage des crédits.

Les modifications du workflow portent sur les fichiers déclencheurs et les
tests de régression ; aucune planification horaire n'est modifiée.

## Ajouter une illustration

1. Vérifier le rapport précis entre le sujet et l'objet représenté.
2. Utiliser un fichier local et une notice de provenance vérifiable.
3. Ajouter une entrée au catalogue avec des sujets précis, sans catégorie
   générique telle que « sacré », « Égypte », « philosophie » ou « théâtre ».
4. Indiquer la page de provenance, la licence, l'auteur du cliché et les
   limites de l'identification ; ne pas transformer une hypothèse en fait.
5. Exécuter les tests et reconstruire. Ne pas imposer d'image à un chapitre
   pour atteindre un quota.


Les réconciliations de numérotation et la file éditoriale ajoutées en parallèle
sont conservées. Cette correction ne change aucun manuscrit ni aucun registre
de numérotation.
