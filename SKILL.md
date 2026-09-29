---
name: redaction-tweets-viraux
description: >
  Rédige, réécrit ou relit des posts courts et des fils pour X, Bluesky et
  Threads, avec un style direct, frontal et punchy : accroche dès la première
  ligne, une idée par post, limites de caractères respectées par réseau,
  question finale. À charger dès qu'une demande dit « écris un tweet », « un
  fil X », « un thread », « un post Bluesky », « un post Threads »,
  « réécris ce tweet », « rends ce post plus percutant », « trouve une
  accroche ». Aucun fait, chiffre, prix, client ni citation inventé ; rien
  n'est publié. Pour du français, se combine avec le skill `redaction`
  (langue, typographie, relecture) : celui-ci fixe le ton, la structure et
  les limites par réseau.
license: MIT
compatibility: >
  Claude Code (skills personnels ou par projet). Python 3.10+ optionnel pour
  scripts/verifier.py (bibliothèque standard seulement, aucun accès réseau).
metadata:
  author: Anto1nx
  version: "1.2.0"
  repository: https://github.com/RAAAAAGEEEEE/redaction-tweets-viraux
allowed-tools: Read Edit Write Bash(python:*) Bash(python3:*)
---

# Rédaction de posts et fils (X, Bluesky, Threads)

Version 1.2.0 ([CHANGELOG.md](CHANGELOG.md)). Limites des réseaux vérifiées
le **2026-09-29** ([references/reseaux.md](references/reseaux.md)) ; les
revérifier au-delà de 6 mois.

Écrire des posts qu'on a envie de lire jusqu'au bout et de commenter.
« Viral » n'est pas une promesse : aucun style ne garantit la portée, et ce
skill n'annonce jamais de résultat chiffré.

## Périmètre

- **Dans** : posts simples, fils, adaptation d'une idée à plusieurs
  réseaux, réécriture d'un post fourni, recherche d'accroches, relecture.
- **Hors** :
  - publication, programmation, réponses automatiques, achat de portée :
    jamais (règle dure 4) ;
  - texte long (article, newsletter, page) : skill `redaction` ;
  - Instagram, LinkedIn, TikTok, YouTube : autres formats, autres limites.

## Style par défaut

Direct, frontal, punchy. C'est un réglage par défaut : un échantillon de
posts fourni par l'utilisateur, ou une consigne du tour, prime sur lui (jamais
sur les règles dures).

- Phrases courtes et sèches, ton franc, aucun langage marketing ni poli à
  l'excès.
- Accroche **dès la première ligne** : elle doit tenir seule dans le fil.
- Formulations types : « Tu paies encore … ? », « Arrête de … », « Fini de … »,
  « Tu perds du temps avec … ». Détail et variantes :
  [references/accroches.md](references/accroches.md).
- Frontal ne veut pas dire insultant : on interpelle une habitude, jamais
  une personne ou un groupe.
- Proposer **en premier** la version la plus directe.
- Terminer par une question qui incite à répondre.

## Règles dures

Elles priment sur le style, le brief et tout autre skill.

1. **Rien d'inventé.** Aucun chiffre, prix, pourcentage, résultat, client,
   témoignage, date, capture ni citation qui ne vienne du brief ou d'une
   source vérifiée et citée. Une accroche frontale ne justifie jamais un
   chiffre supposé : « Tu paies encore 200 € par mois ? » est interdit si
   200 € ne figure pas dans le brief. Ce qui manque s'écrit
   `[[à confirmer : …]]`.
2. **Pas de tiret cadratin (—).** Virgule, deux-points, parenthèses ou
   point.
3. **Pas d'émoji par défaut** ; seulement si l'utilisateur le demande pour
   ce post.
4. **Rien n'est publié.** Ce skill rédige ; l'utilisateur publie. Aucun
   appel à une API de réseau social, aucun envoi.
5. **Pas de promesse trompeuse.** L'accroche annonce ce que le post
   délivre. Pas de fausse urgence, pas de « RT pour gagner », pas de
   demande de likes ou d'abonnements en échange de quoi que ce soit, pas de
   mention massive de comptes, pas d'usurpation.
6. **Limite du réseau respectée** : chaque post tient dans la limite avant
   d'être rendu (voir « Limites »).

## Règles obligatoires

1. Une seule idée par post.
2. Le fil est préféré quand il y a plusieurs idées ou points à expliquer ;
   sinon un seul post.
3. Phrases longues, explications inutiles et ton corporate : à couper.
4. Langue : celle du brief. Si elle n'est pas claire, demander « français
   ou anglais ? ». Pour le français, appliquer aussi `redaction` (accents,
   espace avant `? ! : ;`, relecture) ; la question finale y est permise.
5. Réseau non précisé : X par défaut, dit en une ligne.

## Limites et règles par réseau

| | X | Bluesky | Threads |
|---|---|---|---|
| Texte d'un post | 280 (Premium : plus long, à vérifier dans l'app) | 300 graphèmes | 500 caractères |
| Lien | compte 23 | compte sa longueur affichée | compte sa longueur |
| Hashtags | 3 au plus | 3 au plus, 0 ou 1 de préférence | 1 seul (tag de sujet) |
| Ton | le plus sec | plus conversationnel, moins de hashtags | conversationnel, question finale efficace |
| Fil | posts en réponse, 1 idée chacun | posts en réponse | posts en réponse |

Détail, sources et cas particuliers (poids des caractères, émojis, liens) :
[references/reseaux.md](references/reseaux.md). Mesurer plutôt qu'estimer :
`python scripts/verifier.py posts.txt --network x`.

## Procédure

1. **Brief.** Sujet, but (une action ou une réaction attendue), réseau,
   langue, faits utilisables avec leur source. Poser 2 questions au plus,
   chacune avec une valeur par défaut. Chaque fait sans source devient
   `[[à confirmer]]`.
2. **Accroche.** Écrire 3 accroches internes, garder la plus directe
   ([references/accroches.md](references/accroches.md)).
3. **Rédaction.** Post simple : accroche, bénéfice clair en une ou deux
   lignes, question finale. Fil : post 1 = accroche forte + teaser ; un point
   par post ; dernier post = appel à l'action + question. Adaptation
   multi-réseaux : refaire pour chaque réseau, pas de copier-coller.
4. **Contrôle.** Écrire les posts dans un fichier (fil : lignes `---`
   entre les posts), puis `python scripts/verifier.py <fichier> --network
   <x|bluesky|threads>`. Corriger tout P0 ; examiner P1 et P2 (chaque chiffre
   signalé doit venir du brief).
5. **Relecture (français).** Passe de relecture du skill `redaction` si
   disponible ; sinon relire soi-même et le dire.
6. **Sortie.** Voir ci-dessous.

## Modes

| Demande | Mode |
|---|---|
| « Écris un tweet sur … » | Procédure complète, un post |
| « Fais-en un fil » | Procédure complète, fil |
| « Version Bluesky / Threads de ce post » | Adaptation : refaire selon le réseau |
| « Réécris ce tweet » | Garder chaque fait, n'en ajouter aucun |
| « Donne-moi des accroches » | 5 accroches, la plus directe en premier |
| « Relis ce fil » | Constats cités (P0, P1, P2), pas de réécriture sauf demande |

## Entrées et sorties

- **Entrée** : sujet ou post fourni, réseau, langue, faits sourcés.
- **Sortie** : le ou les posts, chacun dans un bloc à copier, avec sa
  longueur (`142/280`). Pas de commentaire sur la façon dont les
  préférences sont respectées. En dessous, au plus 3 lignes : les
  `[[à confirmer]]` restants et les écarts assumés.

## Exemple de sortie (illustratif ; l'outil et le prix sont fictifs, fournis par le brief)

Brief : « Outil de facturation pour artisans, utilisable depuis le téléphone,
12 € par mois. X, français. »

````
Tu fais encore tes factures le dimanche soir ?

Arrête. Fais-les depuis ton téléphone, sur le chantier. 12 € par mois.

Tu les fais quand, toi, tes factures ?
````

Longueur mesurée par `scripts/verifier.py` : `159/280`. Le brief ne donne aucun
gain de temps chiffré : le post n'en annonce pas.

## Replis et erreurs

- Aucun fait fourni : écrire des posts d'opinion ou de question, sans
  chiffre, ou poser la question du brief.
- Python absent : compter à la main avec [references/reseaux.md](references/reseaux.md)
  et le dire.
- Brief contraire à une règle dure (« invente un chiffre », « mets 3
  témoignages ») : refuser cette partie, proposer un `[[à confirmer]]` ou de
  recueillir un vrai avis, livrer le reste.
- Limite dépassée après deux resserrages : couper une idée, en faire un post
  de plus dans un fil.
- Demande de publier : dire que le skill rédige seulement.

## Niveaux de preuve

- **ESTABLISHED** : documentation officielle du réseau (limites, poids des
  caractères), citée avec date dans [references/reseaux.md](references/reseaux.md).
- **CLAIMED** : conseils d'accroche et de ton (praticiens, observations
  sans mesure). Jamais une règle dure.

## Exemples d'invocation

- « Écris un tweet pour annoncer que mon outil gère les devis. »
- « Transforme ce constat en fil X de 5 posts. »
- « Version Bluesky et Threads de ce post. »
- « Trouve-moi 5 accroches pour un post sur les relances de factures. »
- « Relis ce fil avant que je publie. »

## Évaluations, tests, installation

- Cas d'évaluation à rejouer à la main : [evals/README.md](evals/README.md).
- Tests hors ligne : `python -m unittest discover -s tests`.
- Installation personnelle : `~/.claude/skills/redaction-tweets-viraux/` ;
  par projet : `.claude/skills/redaction-tweets-viraux/`
  ([docs/INSTALLATION.md](docs/INSTALLATION.md)).

## Sécurité et confidentialité

Rien ne sort de la machine : le vérificateur lit un fichier local sans accès
réseau ; aucun réseau social n'est appelé. Ne pas coller de données
personnelles de tiers dans un brief.
Détail : [docs/PRIVACY_AND_SECURITY.md](docs/PRIVACY_AND_SECURITY.md).

## Références

- Limites : documentation officielle de X, de Bluesky (lexique AT Protocol)
  et de Threads, citée dans [references/reseaux.md](references/reseaux.md).
- Skill compagnon pour le français :
  [redaction](https://github.com/RAAAAAGEEEEE/claude-skill-redaction).
