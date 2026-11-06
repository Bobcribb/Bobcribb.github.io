# MYTHOS — Refonte du Théâtre grec : neuf manuscrits sources en lecture HTML

**Contrôle : 6 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`. Site public : `https://bobmythos.fr`. Règles relues sur la branche actuelle : `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md`.

## 1. Statut scientifique et garde de numérotation

La relecture initiale de `main`, de l'arbre Git et de la file éditoriale n'a identifié aucun nouveau manuscrit universitaire **public, intégral, approuvé et absent de toutes les publications**, susceptible d'être intégré sans doublon. Les études sous `chapitres/` disposaient d'un lecteur HTML à leur chemin canonique. Les autres manuscrits non attribués figuraient déjà sous `editorial/inbox/` ou en retenue. Les brouillons privés Google Drive ne sont pas réputés approuvés.

**Nouvelles premières publications scientifiques imputables à cette séance : 0.** Le présent chantier apporte neuf **nouvelles éditions de lecture HTML des sources intégrales déjà publiées en Markdown**, sans les présenter comme neuf manuscrits inédits, sans réattribution ni numéro nouveau. Les sources d'origine et les lecteurs critiques anciens restent intacts.

État récent particulier : MC-096 « Les ombres du divin » a bien reçu la cote canonique **CCXCIV (294)**, via la transaction du registre sous son UUID historique `9b4d6a70-8ef2-4b8c-a4d3-202611060755`, mais son lecteur était **404 en HTTPS** au contrôle du présent audit. Une seconde demande MC-096 distincte, « Les mains du divin », a reçu une **retenue documentaire** `4f96a7d1-7cde-4b95-ae63-202611060096` sur `main`, sans attribution parallèle. Elle doit être réconciliée avant une cote historique autonome ; aucune action de cette séance ne l'a modifiée.

## 2. Lacune concrète : neuf sources disponibles seulement en Markdown brut

Les neuf manuscrits `corpus/theatre-grec/comedies/<slug>-source.md` étaient consultables publiquement sous leur URL Markdown. Les lecteurs `polyidos-source.html` et `kokalos-source.html` ont été ouverts sur bobmythos.fr **avant** intervention : tous deux renvoyaient une erreur **404**. Le module historique `theatre_fragment_index.py` reliait déjà deux lecteurs distincts (étude critique et scènes modernes) ; les sources originales ne disposaient pas de lecteurs HTML autonomes.

Les neuf dossiers contrôlés, avec leur triple patrimoine déjà existant (source Markdown, étude critique HTML, scènes modernes HTML), sont :
- `polyidos` — *Polyidos* ;
- `daidalos` — *Daidalos* ;
- `kokalos` — *Kôkalos* ;
- `aiolosikon` — *Aiolosikōn* ;
- `holkades` — *Holkades* ;
- `lemniai` — *Lemniai* ;
- `geras` — *Géras* ;
- `ploutos-protos` — *Ploutos I* ;
- `triphales` — *Triphalès*.

## 3. Modifications du code et parcours de lecture

1. `scripts/theatre_source_readers.py` — nouveau générateur de neuf pages `/corpus/theatre-grec/comedies/<slug>-source.html` : rendu HTML de la **source Markdown complète**, avec sections d'origine, sommaire des titres, métadonnées conservées, liens de navigation, accès direct au fichier Markdown, hash SHA-256 calculé sur les octets originaux, et bibliographie. Le processus valide toutes les sources **avant** d'écrire les lecteurs. Les renvois historiques vers des destinations inexistantes deviennent des annotations signalées (texte lisible préservé) ; les renvois vers d'autres manuscrits de la même série rejoignent leurs nouvelles pages HTML.
2. `scripts/theatre_fragment_index.py` — le portail `/theatre/#theatre-comedies-editions` pointe vers le nouveau lecteur HTML et conserve le lien Markdown original ; les dix-huit lecteurs existants reçoivent un quatrième renvoi vers l'édition source HTML. Leur prose scientifique et les scènes modernes sont inchangées.
3. `assets/mythos-theatre-archive.css` — fond noir/anthracite, texte ivoire et or, bannière avec statue à gauche et temple à droite préservée, largeur de lecture contrôlée, sommaire à deux colonnes sur grand écran puis une colonne sur mobile, zones tactiles et focus clavier, impression A4 et préférences d'accessibilité. Pas de retour des dessins 2,5D.
4. `tests/test_theatre_archives_navigation_20261106.py` — contrôle des neuf nouvelles URLs et des quatre liaisons réciproques, avec fixture scientifique vérifiable.
5. `tests/test_theatre_source_readers_20261106.py` — contrôle intégral des neuf sources réelles, de l'absence de troncature et de perte de paragraphes, des empreintes SHA, de l'idempotence des deux générations, et refus d'écraser une source publique divergente.

Les sources ne sont pas modifiées dans `corpus/` ; aucun nouveau fichier numéroté n'est créé dans `chapitres/`. Les pages HTML sont **générées** par la reconstruction du site ; elles ne doivent pas être déclarées publiées sans contrôle GitHub Actions + HTTPS.

## 4. Commits confirmés sur `main`

- `19bbae0cf976fb8e6e381bdfb007298fce574849` — création du moteur HTML des sources.
- `aed9ffb475a1ef791c9b76012dc8785c79e4d5e5` — compatibilité des tests de sources courtes documentées.
- `7c2848a25054c31bc1b82249f6cc5237144bfda3` — raccordement au portail et liens croisés.
- `2ac523a13b35136d56928a96afb0918ecdb8fafb` — style muséal responsive.
- `fa3f468754d06af4e3942d363a9285b4d1e44ac0` — mise à jour des tests historiques.
- `48324ad9de7631f9186450a00e0f911ba52daed1` — tests nouveaux des neuf lecteurs.
- `dbe9286edeb31d9085b3659d2b6147d887c0084e` — correction du test de sommaire.
- `2085b49a23a3391fb265f8d3f63de6e06464bd7d` — contrôle de tous les paragraphes et références.

## 5. Validations et blocages restant à confirmer

Des tests anciens ont **échoué avant** la mise à jour de leur fixture car celle-ci ne fournissait qu'un seul titre H2, insuffisant pour le nouveau lecteur intégral ; la fixture a été corrigée dans `fa3f468`. À la dernière vérification, les validations `42185467387` et `42185690022` étaient toujours à l'étape de génération complète, après succès des étapes de tests unitaires. Les nouvelles modifications `2085b49` nécessitent une validation finale de leur propre workflow. Une autre exécution de publication avait échoué sur la collision historique MC-096 avant sa mise en retenue, par un processus éditorial distinct.

**Preuve publique encore manquante :** le manifeste `https://bobmythos.fr/catalog/publication-verification.json` présentait encore `source_commit=db016f6cbc0bec783e369a1e2874f0c6a1883aa6`, exécution `42175517252`, 1 604 documents indexés, 27 archives et 110 médias lors de la dernière consultation. Les nouveaux lecteurs n'étaient alors pas en ligne. Conditions de validation finale : tests unitaires et publication complets, reçu non ambigu, manifeste public postérieur au correctif, HTTP 200 pour les neuf nouvelles pages, comparaisons des textes et bibliographies, tests 360 px et liens réciproques.

**Intégrité :** aucune modification de `editorial/numbering.json`, `editorial/holds.json`, `editorial/inbox/`, des archives, des sources d'articles, des images WebP, des workflows GitHub ou des autres planifications horaires MYTHOS n'a été réalisée dans cette séance.
