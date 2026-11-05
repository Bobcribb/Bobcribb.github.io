# MYTHOS — Égée du Bronze, cités grecques et Pergame
**Intervention : 5 novembre 2026.** Dépôt : `Bobcribb/Bobcribb.github.io`, branche `main`.

## 1. Contrôle éditorial préalable
Les gardes `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` ont été relues sur `main` avant l'intervention. Inventaire initial de la file : **318 JSON de soumission**, **313 attributions** dans `editorial/numbering.json`, **5 retenues explicites** dans `editorial/holds.json` et **aucune demande valide non attribuée**. Les cinq retenues contiennent des conflits documentaires détaillés et leurs manuscrits restent intacts.

Parmi les sources publiques vérifiées pour cette séance, aucun manuscrit universitaire intégral approuvé et absent à la fois du site et de la file de publication n'a été identifié. Aucun UUID, numéro, reçu ou fichier `chapitres/` n'a été ajouté, et aucun manuscrit privé n'a été publié.

## 2. Trois études intégrales retrouvées et nouvellement reliées au corpus grec
Les trois pages suivantes étaient **déjà publiées dans « Civilisations »**, mais absentes du groupe `RELATED` de l'encyclopédie grecque. Les textes ont été consultés dans leur intégralité HTML et contrôlés quant à la présence des sections, des références et des bibliographies. La nouveauté consiste en leur **rattachement au catalogue grec et aux dossiers thématiques** : il ne s'agit pas d'une première publication de leur contenu.

| Étude | Adresse existante | Contrôle initial |
| --- | --- | --- |
| Égée du Bronze : Minoens et Mycéniens | `/bibliotheque-mythologies-du-monde/civilisations-histoire-egee-bronze/` | 30 194 caractères HTML ; 18 sections de lecture ; blob source `366befdaf65d8504c90ce15ab8e0d0f225190e46`. Linéaire A, linéaire B, Pylos, tableau critique des sources. |
| Grèce antique : cités, démocratie et tragédie | `/bibliotheque-mythologies-du-monde/civilisations-histoire-grece-antique/` | 20 440 caractères HTML ; 18 sections ; blob source `988ee92112b388680e22d1abaad3fd683839a733`. Institutions, témoignages antiques et bibliographie. |
| Pergame : Attalides, Grand Autel et Gigantomachie | `/bibliotheque-mythologies-du-monde/civilisations-pergame-attalides-autel-zeus/` | 15 449 caractères HTML ; 8 sections ; blob source `3e4c42d7823a7a77443c923fe51406f94f464352`. Histoire dynastique, image monumentale et sources institutionnelles. |

Le dossier Égée du Bronze est classé dans **Sources anciennes → Égée du Bronze — archéologie, linéaire A et B** ; l'étude des cités sous **Sources anciennes → Histoire des cités grecques — institutions et témoignages** ; Pergame sous **Cultes et sanctuaires → Pergame — Grand Autel, Gigantomachie et royauté**.

Les études gardent leurs propres URL et leur catégorie Civilisations, sans copie, troncature, résumé substitutif ni numéro éditorial fictif.

## 3. Navigation, appareil critique et graphisme
Le générateur `scripts/build_greek_corpus.py` référence les trois textes dans la rubrique reliée « Philosophie, histoire et collections reliées ». `scripts/build_greek_folders.py` détermine pour chacun un **unique classement primaire**, un fil d'Ariane jusqu'au sous-dossier précis et un **encadré réciproque** de deux liens vers les autres textes, inséré hors de `article` et reconstruit sans doublon.

L'encadré explicite le décalage de dates, d'institutions et de types de sources entre administration mycénienne, cités classiques et Pergame hellénistique. Une mémoire mythique commune ne prouve pas une continuité institutionnelle.

Les panneaux utilisent `assets/mythos-museum.css` : accent doré sur fond anthracite, grille responsive déjà utilisée en dessous de 700 px, liens tactiles de 44 px, focus clavier visible et adaptation à 480 px. La bannière statue grecque à gauche / temple à droite, les autres cartes illustrées et les sources iconographiques sont conservées. Aucune figure 2,5D n'a été réintroduite.

## 4. Commits et contrôles
- `d971336be63db190ad6b6901406af0c3b56e13b7` — référencement des trois études intégrales dans le catalogue grec.
- `f0d7c378a2e0816fb573ab97c6789e01ac23eabb` — classement primaire, fil d'Ariane, lectures croisées et contrôles du générateur.
- `c9c24e8a226fa641fa4b52f115c1f0f7007c772e` — CSS muséal des panneaux historiques.
- `42f1839dece34abb7cb04940c21da3779cf3e467` — tests d'inventaire, sources, idempotence et conservation des articles.

Le test ajouté à `tests/test_greek_folders.py` contrôle les sources sur disque, leurs trois cotes documentaires, le rattachement au catalogue, les liens bidirectionnels, l'intégrité des balises `article` et deux reconstructions successives. Il contrôle aussi l'accessibilité des deux familles de dossiers concernées.

**État de validation lors de la rédaction du présent rapport :** les workflows GitHub Actions des dernières révisions étaient en attente ou en cours. Le déploiement public de ces changements sur `bobmythos.fr` n'est donc **pas encore confirmé** ; ne pas confondre commits dans `main` et réception sur le domaine. Le reçu public `/catalog/publication-verification.json` n'était pas accessible dans le navigateur d'audit à cet instant. Recontrôler les workflows, les trois panneaux sur les pages HTTPS, les dossiers Sources anciennes et Cultes et sanctuaires, et la provenance des sources avant toute annonce de mise en ligne.

Les registres et textes universitaires, les archives et les autres automatisations MYTHOS sont inchangés.
