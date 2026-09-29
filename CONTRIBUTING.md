# Contribuer

Issues et pull requests bienvenues.

## Avant d'ouvrir une pull request

1. `python -m unittest discover -s tests` passe. À la version 1.2.0, 32 tests hors ligne passent.
2. Toute règle ajoutée à `scripts/verifier.py` a un test dans `tests/test_verifier.py`.
3. Toute limite de réseau modifiée ou ajoutée dans `references/reseaux.md` porte sa source officielle et la date de vérification, et met à jour la table `NETWORKS` du vérificateur, `SKILL.md` et `CHANGELOG.md` dans le même commit.
4. Un changement de comportement du skill ajoute ou met à jour un cas de `evals/evals.json` ([evals/README.md](evals/README.md)).
5. Aucune donnée réelle (nom de client, e-mail, chiffre d'entreprise) dans les exemples, fixtures et evals : noms et chiffres fictifs, et dites-le.
6. Aucun tiret cadratin dans les fichiers du dépôt, sauf pour le citer comme caractère.
7. La documentation change **dans le même commit** que le comportement.

## Style

- Documentation en français ; code et noms de variables en anglais.
- Python 3.10+, bibliothèque standard uniquement.
- Toute commande documentée a été exécutée.
