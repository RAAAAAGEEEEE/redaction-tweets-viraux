# Configuration

Le skill n'a ni variable d'environnement, ni clé, ni fichier de réglages. Il n'y a donc pas de `.env.example`.

## Options du vérificateur

| Option | Effet | Défaut |
|---|---|---|
| `fichier` | Chemin du texte en UTF-8, ou `-` pour l'entrée standard | requis |
| `--network` | `x`, `bluesky` ou `threads` | `x` |
| `--limit N` | Remplace la limite du réseau (compte X avec posts longs, par exemple) | limite du réseau |
| `--allow-emoji` | Ne signale plus les émojis | désactivé |
| `--json` | Sortie JSON : `network`, `limit`, `lengths`, `findings` | texte |

## Réglages internes (dans `scripts/verifier.py`)

À modifier dans le code, avec un test (voir [../CONTRIBUTING.md](../CONTRIBUTING.md)) :

| Réglage | Valeur | Où |
|---|---|---|
| Limite de longueur | X 280, Bluesky 300, Threads 500 | `NETWORKS` |
| Hashtags au plus | X 3, Bluesky 3, Threads 1 | `NETWORKS` |
| Liens au plus | Threads 5 | `NETWORKS` |
| Longueur d'un lien sur X | 23 | `X_URL_LENGTH` |
| Poids des caractères sur X | 1 pour quatre plages Unicode, 2 sinon | `X_LIGHT_RANGES` |
| Formules d'IA | liste de motifs | `AI_TICS` |

Les sources des limites sont dans [../references/reseaux.md](../references/reseaux.md).

## Style par défaut

Le style direct et frontal se règle dans [../SKILL.md](../SKILL.md) (section « Style par défaut »). Un échantillon de vos posts, donné dans la conversation, le remplace.

Voir aussi : [USAGE.md](USAGE.md).
