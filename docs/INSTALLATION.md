# Installation

## Prérequis

- Claude Code, qui charge les skills de `~/.claude/skills/` (personnels) et de `.claude/skills/` (par projet).
- Git pour cloner.
- Python 3.10+ pour le vérificateur et les tests (bibliothèque standard seulement). Vérifier avec `python --version`.

## Installation personnelle

macOS, Linux, Git Bash sous Windows :

```bash
git clone https://github.com/RAAAAAGEEEEE/redaction-tweets-viraux ~/.claude/skills/redaction-tweets-viraux
```

PowerShell :

```powershell
git clone https://github.com/RAAAAAGEEEEE/redaction-tweets-viraux "$env:USERPROFILE\.claude\skills\redaction-tweets-viraux"
```

Le dossier doit s'appeler `redaction-tweets-viraux` (le nom du skill dans `SKILL.md`).

## Installation par projet

Depuis la racine du projet :

```bash
git clone https://github.com/RAAAAAGEEEEE/redaction-tweets-viraux .claude/skills/redaction-tweets-viraux
```

## Skill compagnon (recommandé pour le français)

```bash
git clone https://github.com/RAAAAAGEEEEE/claude-skill-redaction ~/.claude/skills/redaction
```

## Vérifier

```bash
cd ~/.claude/skills/redaction-tweets-viraux
python -m unittest discover -s tests
```

Résultat attendu : `Ran 32 tests` puis `OK`.

Dans une nouvelle session Claude Code, le skill apparaît dans la liste des skills ; une demande comme « écris un tweet sur … » le charge.

Vérification faite le 2026-09-29 (version 1.2.0) : clone dans un dossier vide, puis la commande de test ci-dessus, sous Windows 11 avec Git Bash et Python 3.11.

## Mettre à jour

```bash
cd ~/.claude/skills/redaction-tweets-viraux && git pull
```

## Désinstaller

Supprimer le dossier `~/.claude/skills/redaction-tweets-viraux`.

Voir aussi : [USAGE.md](USAGE.md), [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
