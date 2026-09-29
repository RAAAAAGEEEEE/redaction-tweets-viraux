# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/). Versions selon [SemVer](https://semver.org/lang/fr/).

## [1.2.0] - 2026-09-29

### Ajouté
- Règles par réseau : X (280), Bluesky (300 graphèmes), Threads (500), avec sources et dates dans `references/reseaux.md`.
- `references/accroches.md` : sept formes d'accroche, ce qu'il faut éviter, exemples complets (post simple, fil, adaptation Bluesky et Threads).
- `scripts/verifier.py` : longueur par réseau, cadratin, placeholders, hashtags, émojis, chiffres à sourcer, question finale ; 32 tests.
- `evals/` : 7 cas d'évaluation fictifs et `tests/test_evals.py`.
- Règle dure : pas de promesse trompeuse (fausse urgence, appât à interaction).
- Documentation complète (`docs/`, `CONTRIBUTING.md`, `SECURITY.md`) et front-matter portable (`license`, `compatibility`, `metadata`, `allowed-tools`).

### Modifié
- Le style direct devient un réglage par défaut, remplaçable par un échantillon de l'utilisateur ; les règles dures priment.
- Publication : les références à un utilisateur ou à un projet précis sont retirées ; `LICENSE` porte le nom complet du titulaire du droit d'auteur.

## [1.1.0] - 2026-09-28

### Ajouté
- Règles dures : rien d'inventé, pas de tiret cadratin, pas d'émoji par défaut, rien n'est publié.
- Renvoi vers le skill `redaction` pour la langue et la relecture des tweets en français.

### Modifié
- Le workflow ne demande plus d'expliquer en quoi le tweet respecte les préférences : le tweet est rendu seul.

## [1.0.0] - 2026-07-18

Première version.
