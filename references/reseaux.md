# Limites et règles par réseau

Vérifié le **2026-09-29**. Au-delà de 6 mois, revérifier chaque ligne datée
avant de la ressortir : les réseaux changent leurs limites sans préavis.

Niveaux de preuve : **ESTABLISHED** = documentation officielle du réseau ;
**CLAIMED** = pratique ou observation de praticiens, sans mesure.

## X

| Règle | Valeur | Preuve |
|---|---|---|
| Longueur d'un post | 280 unités de poids | ESTABLISHED, [docs.x.com, comptage des caractères](https://docs.x.com/fundamentals/counting-characters) (2026-09-29) |
| Poids des caractères | Latin, ponctuation courante : 1 ; émojis : 2 chacun, quelle que soit leur complexité ; CJK : 2 | idem |
| Lien | compte 23 unités, quelle que soit sa longueur réelle (raccourci t.co) | idem |
| Posts plus longs (Premium) | jusqu'à 25 000 caractères, avec seulement les 280 premiers visibles dans le fil | CLAIMED : sources tierces, non confirmé par la page officielle citée ci-dessus ; à vérifier dans l'application |

Cas particuliers (poids selon la [configuration publique v3 de
`twitter-text`](https://github.com/twitter/twitter-text/blob/master/config/v3.json),
consultée le 2026-09-29, ESTABLISHED pour la bibliothèque, non confirmé pour
le compteur actuel de X : poids 1 pour U+0000 à U+10FF, U+2000 à U+200D,
U+2010 à U+201F et U+2032 à U+2037, poids 2 pour le reste) : le point de suspension `…`, le signe `€`,
l'espace fine insécable U+202F et les flèches comptent double. Pour le
français, préférer l'espace insécable ordinaire U+00A0 (poids 1) ou une
espace ordinaire à l'espace fine. Le vérificateur applique ce poids ; c'est
une approximation, pas le compteur officiel.

Conventions (CLAIMED) : ton le plus sec des trois ; 0 à 2 hashtags rendent
mieux que 3 ; un lien dans le premier post d'un fil réduit souvent la portée,
d'où le lien dans le dernier post. Aucune de ces conventions n'est mesurée
ici.

## Bluesky

| Règle | Valeur | Preuve |
|---|---|---|
| Longueur d'un post | 300 graphèmes, et 3 000 octets UTF-8 au plus | ESTABLISHED, [lexique `app.bsky.feed.post`](https://github.com/bluesky-social/atproto/blob/main/lexicons/app/bsky/feed/post.json) (2026-09-29) : `maxGraphemes` 300, `maxLength` 3000 |
| Étiquettes (`tags`) | 8 au plus, 64 graphèmes chacune | idem |
| Langues déclarées | 3 au plus | idem |
| Lien | le lien occupe sa longueur dans le texte ; les clients raccourcissent parfois l'affichage dans le texte lui-même | CLAIMED : à vérifier sur le client utilisé |

Un graphème est un caractère tel que l'œil le voit : `é`, `👍🏽` ou
`👨‍👩‍👧` comptent 1. Conventions (CLAIMED) : ton plus conversationnel qu'X,
hashtags rares (0 ou 1), texte alternatif sur toute image.

## Threads

| Règle | Valeur | Preuve |
|---|---|---|
| Longueur d'un post | 500 caractères | ESTABLISHED, [Meta, publier sur Threads](https://developers.facebook.com/docs/threads/posts) (2026-09-29) |
| Liens | 5 au plus par post (depuis le 2025-12-22) | idem |
| Tag de sujet (hashtag) | un seul par post, 1 à 50 caractères | idem |
| Carrousel | 2 à 20 médias | idem |

Convention (CLAIMED) : ton conversationnel, une question en fin de post
suscite des réponses. Cette page officielle ne précise pas la longueur des
pièces jointes de texte : ne pas s'y appuyer.

## Règles communes

- **Une idée par post.** Un fil sert à enchaîner des idées, pas à couper une
  phrase en deux.
- **Accroche d'abord** : sur les trois réseaux, seule la première ligne est
  certaine d'être lue.
- **Numérotation** (`1/5`) : facultative ; utile pour un fil de plus de trois
  posts ; elle consomme des caractères.
- **Texte alternatif** sur toute image ; ne jamais y mettre un fait absent
  du brief.
- **Aucune publication** par ce skill, quel que soit le réseau.
