# MYTHOS — Refonte : Ioulis, Apollon Ptoios et Héra Lakinia

**Date du contrôle : 5 novembre 2026**. Référence : `main` au commit `7b565bcd9ac56e954d13d0eeaa2c02cb374477cf` avant intervention.

## Contrôle des règles et de l'inventaire

Règles `AGENTS.md` et `docs/PUBLICATION_CONCURRENTE.md` relues avant toute modification. L'inventaire initial recensait 344 demandes, 331 attributions, cinq retenues, huit demandes restantes. Plusieurs soumissions sont en cours d'attribution concurrente par GitHub Actions : **ces chiffres sont un instantané, non un état permanent**.

Aucun nouveau numéro ni nouveau manuscrit n'a été fabriqué. Les études déjà soumises utilisent les variables `{{numero}}` et `{{volume}}` ; le générateur et la file attribuent seuls leurs cotes.

## Collision entre deux monographies existantes sur Ioulis

- Première demande (non modifiée) : `9a0873be-5f44-4d99-b4a3-4f890a026f71`, loi funéraire d'Ioulis de Céos, `ioulis-ceos-loi-funeraire-eau-mer-purification`, 28532 caractères Markdown.
- Seconde demande (non modifiée) : `d5cc1ed0-5698-4dbb-9115-29e948eb3874`, même inscription antique mais appareil critique distinct, `ioulis-ceos-loi-funeraire-eau-de-mer-souillure-maison`, 32857 caractères Markdown. Empreinte SHA-256 de la demande : `af5c6a2f62ad2fb459d3ada8c1a2acfb2143742ad257c5716b8bf5c0cfb49a71`.

La seconde soumission est inscrite dans `editorial/holds.json`, avec contrôle strict de son empreinte et motif. Cette retenue **n'efface pas** le texte et ne clôt pas la question philologique : il faut comparer les deux manuscrits avant toute éventuelle publication de la seconde étude comme complément non numéroté de la première. La première demande suit le circuit transactionnel habituel, sans numéro réservé ici.

## Deux nouveaux manuscrits complets déjà accessibles dans la file

- `83d14be7-6c2a-46de-83e1-4962a2d0be57` : **Apollon Ptoios, l'oracle béotien et le héros Ptoios** ; manuscrit de 51886 caractères.
- `d5a47e36-8b27-4cb2-a3d0-f18a7e2c9d64` : **Héra Lakinia et le sanctuaire de Crotone / Capo Colonna** ; manuscrit de 57169 caractères.

Ces textes sont déjà déposés sous leurs UUID officiels. `scripts/build_greek_folders.py` reçoit deux règles sémantiques de classement : **Cultes et sanctuaires → Béotie/Ptoion** et **Cultes et sanctuaires → Grande-Grèce/Crotone**. Ces règles produiront automatiquement un sommaire et des liens de retour vers les sous-dossiers lors de la génération **après attribution canonique**, sans nom de fichier numéroté inventé.

Les chapitres restent dans `editorial/inbox/` tant que GitHub Actions ne les attribue pas : la présence des règles ne prouve pas leur publication.

## Design et contrôles

La charte noir/anthracite, or et ivoire, la bannière statue grecque/temple, les illustrations déjà sourcées et les huit familles sont conservées. Les intitulés longs des sous-dossiers gagnent des règles tactiles sous 480 px, avec retour à la ligne et hyphénation.

Deux tests ont été ajoutés à `tests/test_greek_folders.py` : vérification des deux manuscrits et de leur classement sans préattribuer de numéro ; intégrité de la retenue SHA-256 d'Ioulis et absence de reçu pour la version concurrente.

**À confirmer après commit :** validation GitHub Actions, contrôle du registre, génération des pages et reçu public `/catalog/publication-verification.json`. Ne pas annoncer de déploiement tant que ce reçu et les pages HTTPS n'ont pas été inspectés. Aucune planification ou automatisation MYTHOS n'a été modifiée.
