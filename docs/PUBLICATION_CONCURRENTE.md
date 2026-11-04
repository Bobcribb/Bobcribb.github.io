# Attribution atomique des numéros MYTHOS

## État et périmètre

La collision 583 était déjà réconciliée sur `main` au commit
`094401c4ec9e43de7636f919d0e901627c3b675b`. Le chapitre « Qui a le droit
d'interpréter ? » conserve 583. « Croire, prévoir, instituer : Xunzi, Cicéron et
Nietzsche » reste intégral, à son adresse historique, comme complément 583.
Les deux manuscrits sont inchangés. Leurs renvois historiques ne réservent pas
les prochains numéros ; le sommaire reconstruit fait autorité pour la lecture.

Le correctif de synchronisation concurrent `298b8cfcbee3b14efe4a4f54f1f2d450e4cb4980`
est conservé : les reconstructions restent isolées dans des worktrees temporaires.
Les chapitres 597 et 598 arrivés pendant cet audit sont inclus dans la photographie initiale.

Le correctif concurrent `2e8ec6fba2188c79047517b6dda47a0a2cfacfed` a réconcilié
les numéros des autres collections. Cette correction est conservée ; ses
redirections historiques restent dans `EDITORIAL_NUMBERING.json`. Le registre
`editorial/numbering.json` photographie les chemins après cette correction et
conserve les reçus des nouvelles attributions. Le premier décrit les corrections
historiques, le second les transactions de publication ; aucun compteur séparé
ne remplace la lecture des manuscrits réels. Les exceptions documentées de 583
restent chapitre canonique et complément. Les tomes d'archives et manuscrits
assemblés ont un ordre distinct.

## Envoyer une nouvelle étude approuvée

Préparer le texte intégral sans numéro définitif : `{{numero}}` pour le numéro
décimal, `{{volume}}` pour un volume romain. Employer ces variables uniquement
dans les titres, sous-sections et liens qui dépendent du nouveau numéro. Les
références antiques, dates et numéros des chapitres antérieurs restent littéraux.
Ne pas promettre le numéro du chapitre suivant dans le texte.

```bash
python scripts/editorial_queue.py enqueue --collection origines-du-sacre \
  --slug titre-court --source /chemin/etude-approuvee.md
```

Le programme écrit `editorial/inbox/<uuid>.json`. Enregistrer uniquement ce
fichier sur `main` par commit normal ou par `create_file` du connecteur GitHub.
Un agent sans terminal peut créer directement le même objet JSON :

```json
{
  "version": 1,
  "collection": "origines-du-sacre",
  "slug": "titre-court",
  "markdown": "# Chapitre {{numero}}\n## Titre de l'étude\n\nTexte intégral approuvé...\n"
}
```

Ce dépôt est public : la file reçoit exclusivement des manuscrits approuvés pour
publication, jamais les brouillons privés. Garder le même UUID lors d'une reprise.
Si une création est incertaine, relire son chemin avant de recommencer. Les
demandes publiées sont immuables et conservées ; leur hash empêche de réutiliser
un UUID pour un autre texte. Le slug ne doit pas être déjà utilisé dans la série.
Les corrections ultérieures se font dans le manuscrit publié, à numéro constant.

## Transaction et concurrence

Le workflow existant conserve son groupe de concurrence et ne change aucune
planification. Il traite toutes les demandes persistantes trouvées sur `main`,
même si GitHub remplace une exécution en attente par une plus récente.

1. Relire `origin/main` et créer un worktree temporaire depuis cet état.
2. Contrôler les fichiers réellement présents contre le registre.
3. Pour chaque demande non traitée, attribuer `maximum présent + 1` dans sa
   collection ; produire le manuscrit et le reçu ensemble. Le numéro n'est
   réservé ni par une lecture ni par une écriture séparée dans un compteur.
4. Reconstruire le site, vérifier les textes réconciliés, les sommaires, la
   recherche, le sitemap, les 27 tomes et les 110 médias avant tout push.
5. Commiter les sources, attributions et rendus ensemble, puis pousser sans force.
6. Si une source, un média, un générateur, un registre ou une demande existante a
   changé, abandonner le résultat local, relire `main` et refaire l'attribution.
   Aucun rebase de numéro. Si les seules différences sont de nouvelles demandes
   valides sous `editorial/inbox/` ou le journal `EDITORIAL_CONTINUITY.md`, les
   conserver par fusion sans modifier les sources ni attributions déjà validées.
   Ces nouvelles demandes restent sans numéro jusqu'à l'exécution suivante.
   Cette exception évite que les arrivées horaires bloquent indéfiniment un rendu
   valide. Elle n'autorise ni fusion de rendus concurrents ni modification d'un
   manuscrit publié. Après cinq échecs, arrêter sans perdre les demandes déjà
   enregistrées ; une nouvelle exécution reprend ces UUID.

Le reçu est la preuve d'attribution. Sa présence rend une reprise inoffensive,
y compris lorsque le serveur a accepté un push mais que sa réponse s'est perdue.
Un JSON invalide provoque un arrêt avant écriture du lot ; corriger uniquement
la demande non publiée avant de relancer.

## Contrôles et limite d'administration

Le générateur refuse désormais les nouveaux fichiers numérotés non attribués,
avant de toucher `_site`. La CI vérifie aussi les pull requests. Les ajouts
directs contournant la file ne doivent pas être utilisés par les rédacteurs.

La branche n'était pas protégée lors du contrôle initial. Ce changement ne crée
pas une protection administrative GitHub et n'en revendique pas l'effet : un
acteur disposant d'un accès direct peut toujours pousser des sources invalides,
mais elles sont refusées avant déploiement. La prévention transactionnelle des
collisions s'applique au circuit de publication décrit ici. Imposer ce circuit
à tous les acteurs nécessiterait en plus des règles GitHub administrateur.

La vérification publique est exposée dans
`/catalog/publication-verification.json` (commit source, exécution Actions,
empreintes des textes, registre et compteurs). Sa présence ne dispense pas de
vérifier le résultat du workflow et les pages HTTPS correspondantes.

## Collision arrivée pendant la mise en place

Le commit `501cbbc19396b423e2edb0e3884ca8b9391b6cb0` a ajouté Protésilas sous
CLXXXVIII (188), alors que le correctif historique précédent avait déjà attribué
188 à Lycurgue d'Eschyle. Protésilas reçoit CCI (201), premier numéro libre sur
la branche contrôlée. L'ancienne URL redirige vers la nouvelle. Les sections
scientifiques, fragments et bibliographie sont conservés ; seules les mentions
de numérotation et de continuité éditoriale sont rectifiées. Les empreintes des
deux états sont inscrites dans `EDITORIAL_NUMBERING.json` ; le manuscrit original
reste disponible dans son commit de création. Le nouveau volume de comédie 58
est également conservé dans la photographie de départ.

Le dossier Talal Asad, ajouté par `8622c909583e7745be355c96cd43927ea1656534`
sous CXXXIX (139), entrait à son tour en collision avec Hannah Arendt. Il reçoit
CLVIII (158), premier numéro libre du cycle comparatif au contrôle. Seules les
trois mentions de son propre numéro et l'annonce d'un numéro futur sont
rectifiées ; le texte scientifique est conservé. L'ancienne adresse redirige.
