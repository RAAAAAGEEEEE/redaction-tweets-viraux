# Utilisation

## Dans Claude Code

Le skill se charge seul pour une demande de tweet, de fil ou de post. On peut aussi le nommer : « avec le skill redaction-tweets-viraux, … ».

| Demande | Ce que fait Claude |
|---|---|
| « Écris un tweet sur … » | Brief (2 questions au plus), accroche, un post X, mesure de la longueur |
| « Fais-en un fil X » | Un post d'accroche, un post par idée, dernier post avec question |
| « Version Bluesky et Threads » | Refait le post pour chaque réseau, selon sa limite et son ton |
| « Réécris ce tweet » | Garde chaque fait, n'en ajoute aucun, ton direct |
| « Trouve-moi 5 accroches » | Cinq accroches, la plus directe en premier |
| « Relis ce fil » | Constats P0, P1, P2 cités, sans réécriture sauf demande |

### Ce que vous recevez

1. Le ou les posts, chacun dans un bloc à copier, avec sa longueur (`159/280`).
2. Au plus trois lignes : les `[[à confirmer : …]]` restants et les écarts assumés.

### Ce qu'il ne fait pas

- Publier, programmer ou répondre à votre place (règle dure).
- Inventer un chiffre, un prix, un témoignage : il vous demande le vrai fait ou laisse un `[[à confirmer]]`.

## Le vérificateur en ligne de commande

Fichier d'entrée : un post par bloc ; un fil sépare ses posts par une ligne contenant seulement `---`.

```bash
python scripts/verifier.py posts.txt --network x
python scripts/verifier.py fil.txt --network bluesky --json
python scripts/verifier.py - --network threads < posts.txt
```

Priorités :

- **P0** (bloquant, code de sortie 1) : longueur dépassée, tiret cadratin, placeholder oublié, plus de 5 liens sur Threads.
- **P1** : `[[à confirmer]]` restant, hashtags en trop, émoji, formule d'IA, espace manquante avant `? ! : ;`.
- **P2** : chiffres à rattacher au brief, dernier post sans question.

Options : [CONFIGURATION.md](CONFIGURATION.md).

## Rejouer les cas d'évaluation

Voir [../evals/README.md](../evals/README.md).

Voir aussi : [LIMITATIONS.md](LIMITATIONS.md).
