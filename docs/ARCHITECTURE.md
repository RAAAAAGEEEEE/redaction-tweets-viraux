# Architecture

## Principe : divulgation progressive

Claude lit `SKILL.md` à chaque déclenchement : il porte le style, les règles dures, la table des limites et la procédure. Les références ne sont lues qu'à l'étape qui en a besoin.

```
redaction-tweets-viraux/
├── SKILL.md                    style, règles dures, limites, procédure
├── references/
│   ├── reseaux.md              limites et règles par réseau, sources datées
│   └── accroches.md            formes d'accroche, pièges, exemples complets
├── scripts/verifier.py         contrôle mécanique, hors ligne
├── tests/                      tests du vérificateur et des evals
├── evals/                      cas d'évaluation fictifs (evals.json, fixtures)
└── docs/                       documentation humaine
```

## Déroulé

1. **Brief** : sujet, but, réseau, langue, faits sourcés.
2. **Accroche** : trois candidates, la plus directe retenue.
3. **Rédaction** : post simple ou fil, un post par réseau demandé.
4. **Contrôle** : `verifier.py` mesure chaque post ; les P0 sont corrigés.
5. **Relecture** (français) : passe du skill `redaction` si disponible.
6. **Sortie** : posts dans des blocs à copier, longueur affichée.

## Pourquoi un vérificateur en plus du prompt

Un modèle compte mal les caractères et remet un cadratin malgré l'interdiction. Le vérificateur transforme ces règles en contrôle qui échoue (code de sortie 1). Il ne juge ni le fond ni les faits.

## Liens avec d'autres skills

| Skill | Relation |
|---|---|
| [redaction](https://github.com/RAAAAAGEEEEE/claude-skill-redaction) | Langue française, typographie, relecture séparée |
| blader/humanizer | Version anglaise des tics d'écriture d'IA |

Voir aussi : [USAGE.md](USAGE.md), [LIMITATIONS.md](LIMITATIONS.md).
