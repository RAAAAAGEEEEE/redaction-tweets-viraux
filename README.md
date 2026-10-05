# redaction-tweets-viraux

Skill Claude Code qui rédige des posts et des fils pour **X, Bluesky et Threads** : style direct, frontal et punchy, accroche dès la première ligne, une idée par post, limites de caractères respectées, aucun fait inventé.

## Comment ça marche

Pour un débutant, trois gestes, et aucun copier-coller du dépôt dans la conversation :

1. **Installer le skill une fois** : `git clone https://github.com/RAAAAAGEEEEE/redaction-tweets-viraux ~/.claude/skills/redaction-tweets-viraux`
   (disponible dans tous vos projets), ou le même clone dans `.claude/skills/redaction-tweets-viraux` à la racine d'un
   projet (disponible dans ce projet seulement). Sous Windows PowerShell, remplacez `~` par
   `$env:USERPROFILE`. Détail : [docs/INSTALLATION.md](docs/INSTALLATION.md).
2. **Le demander** : dans n'importe quelle session Claude Code, écrivez simplement « écris un fil X sur… » ou « rends ce post plus percutant », ou tapez `/redaction-tweets-viraux`.
3. **Se laisser guider** : Claude charge le skill d'après sa description et rend des posts dans les limites de chaque réseau, sans fait inventé et sans rien publier.

C'est le fonctionnement de tous les skills Claude Code : un dossier avec un `SKILL.md` placé dans
`~/.claude/skills/<nom>/` (personnel) ou `.claude/skills/<nom>/` (projet) ; Claude le charge
automatiquement quand votre demande correspond à sa `description`, et `/<nom>` le lance à la main.
[officiel : [skills](https://code.claude.com/docs/en/skills#where-skills-live), page consultée le 2026-10-05]

## Le problème

Un modèle livre des posts polis, trop longs, qui s'ouvrent sur « Dans un monde où », inventent un « 10 fois plus vite » et dépassent la limite du réseau. Personne ne s'arrête dessus.

## Pour qui

Les indépendants, fondateurs et petites équipes qui écrivent leurs propres posts et veulent un premier jet net, sourcé et déjà à la bonne longueur. Le skill écrit en français ou en anglais.

## Ce qu'il apporte

- Un style par défaut direct (« Tu paies encore … ? », « Arrête de … », « Fini de … »), remplaçable par un échantillon de vos posts.
- Les limites de X (280), Bluesky (300 graphèmes) et Threads (500), sourcées et datées, et une adaptation réseau par réseau, pas un copier-coller.
- Des règles dures : aucun chiffre, prix, client ni citation inventé (ce qui manque devient `[[à confirmer]]`), pas de tiret cadratin, pas d'émoji par défaut, rien n'est publié.
- Un vérificateur hors ligne (`scripts/verifier.py`) qui mesure la longueur de chaque post d'un fil et signale les dépassements, les hashtags en trop et les chiffres à sourcer.

## Statut

**Bêta, version 1.2.0** (2026-09-29). Le vérificateur et les cas d'évaluation sont couverts par 32 tests hors ligne. Le comportement du skill dans Claude n'a pas d'évaluation automatique : 7 cas sont fournis dans `evals/` pour être rejoués à la main. « Viral » est le nom du skill, pas une promesse : aucune portée n'est garantie ni chiffrée. Voir [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

## Exemple de sortie

Demande : « Écris un tweet pour mon outil de facturation pour artisans, utilisable depuis le téléphone, 12 € par mois. » (outil et prix fictifs)

```
Tu fais encore tes factures le dimanche soir ?

Arrête. Fais-les depuis ton téléphone, sur le chantier. 12 € par mois.

Tu les fais quand, toi, tes factures ?
```

Sortie réelle du vérificateur sur ce texte (`--network x`) : `159/280`, aucun blocage.

## Prérequis

- Claude Code (skills dans `~/.claude/skills/` ou `.claude/skills/`).
- Python 3.10 ou plus récent pour le vérificateur (bibliothèque standard seulement). Sans Python, le skill fonctionne ; seul le comptage automatique manque.

## Démarrage

```bash
git clone https://github.com/RAAAAAGEEEEE/redaction-tweets-viraux ~/.claude/skills/redaction-tweets-viraux
cd ~/.claude/skills/redaction-tweets-viraux && python -m unittest discover -s tests
```

Puis, dans Claude Code : « Écris un tweet sur … » ou « Fais-en un fil X ».

## Exemple minimal

```bash
printf 'Tu fais quoi ?\n---\nUn deuxième post ?' > fil.txt
python scripts/verifier.py fil.txt --network bluesky
```

Code de sortie : 0 sans blocage, 1 si un P0 est trouvé (limite dépassée, cadratin, placeholder), 2 si le fichier est illisible.

## Architecture

`SKILL.md` porte le style, les règles dures et la procédure ; `references/` le détail chargé à la demande (limites par réseau, accroches et exemples) ; `scripts/verifier.py` le contrôle mécanique. Détail : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Configuration

Aucune variable d'environnement, aucune clé. Options du vérificateur : [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

## Sécurité et confidentialité

Aucun accès réseau, aucune publication. Le vérificateur lit un fichier local. Détail : [docs/PRIVACY_AND_SECURITY.md](docs/PRIVACY_AND_SECURITY.md).

## Limites

- Les longueurs du vérificateur sont une approximation des règles officielles (poids X, graphèmes).
- Les conseils d'accroche sont des pratiques observées, non mesurées (CLAIMED).
- Le vérificateur ne voit pas un fait inventé : il liste les chiffres à rattacher au brief.

Liste complète : [docs/LIMITATIONS.md](docs/LIMITATIONS.md).

## Feuille de route (non contractuelle)

- Exécution automatisée des cas de `evals/`.
- Mise à jour des limites quand les réseaux les changent.

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT, voir [LICENSE](LICENSE).

## Documentation

- [SKILL.md](SKILL.md) : ce que lit Claude
- [docs/INSTALLATION.md](docs/INSTALLATION.md)
- [docs/USAGE.md](docs/USAGE.md)
- [docs/CONFIGURATION.md](docs/CONFIGURATION.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- [docs/LIMITATIONS.md](docs/LIMITATIONS.md)
- [docs/PRIVACY_AND_SECURITY.md](docs/PRIVACY_AND_SECURITY.md)
- [references/reseaux.md](references/reseaux.md) : limites par réseau, avec sources
- [references/accroches.md](references/accroches.md) : accroches et exemples
- [evals/README.md](evals/README.md) : cas d'évaluation
- [SECURITY.md](SECURITY.md)
- [CHANGELOG.md](CHANGELOG.md)
