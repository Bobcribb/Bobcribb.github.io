# Publication MYTHOS

Le dépôt de publication est `Bobcribb/Bobcribb.github.io`, branche `main`.
Lire `docs/PUBLICATION_CONCURRENTE.md` avant toute création d'un chapitre numéroté.

- Ne pas choisir le prochain numéro depuis une conversation, un sommaire HTML,
  une ancienne copie du dépôt ou une annonce « chapitre suivant ».
- Pour les collections `origines-du-sacre`, `encyclopedie`, `comedies`,
  `tragedies` et `comparatif`, déposer le texte intégral approuvé dans un fichier
  JSON à UUID unique sous `editorial/inbox/`. Utiliser `{{numero}}` (décimal) ou
  `{{volume}}` (romain) dans les emplacements du numéro éditorial. Ne pas créer
  directement un nouveau fichier numéroté dans `chapitres/`.
- GitHub Actions attribue le numéro, le manuscrit et son reçu dans le même
  commit, après relecture de `main`. Ne pas modifier manuellement le registre
  pour contourner un refus. Ne jamais forcer un push ni rebaser une attribution.
- En cas de réponse incertaine du connecteur, relire le même chemin UUID ;
  reprendre la même demande, jamais un nouvel UUID pour le même travail.
- Pour corriger une étude existante, modifier son chemin existant et conserver
  son numéro. Préserver intégralement les textes et les archives universitaires.
- Les exceptions historiques sont figées dans le registre. Les études 583
  restent à leurs deux adresses : chapitre canonique et complément intégral.
- Vérifier le workflow, les sommaires, les textes et le site public ; distinguer
  un enregistrement GitHub d'une publication effectivement déployée.
- Ne modifier aucune planification horaire sans demande explicite de l'utilisateur.
- Les anciennes illustrations vectorielles en perspective 2,5D sont retirées à la
  demande de l'utilisateur. Ne pas les réintroduire dans les fiches, les galeries,
  les catalogues d'images ou les fonds de page. Conserver les notices et sources
  archéologiques ainsi que les reconstitutions photoréalistes déjà publiées.

Contrôles : `python -m unittest discover -s tests -v`,
`python scripts/build_native.py`, `python scripts/verify_publication.py`.
`scripts/publish_site.py` utilise des worktrees temporaires isolés ; ne pas
réinitialiser un checkout contenant des modifications locales.
