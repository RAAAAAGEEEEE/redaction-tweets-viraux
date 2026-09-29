# Dépannage

## Le skill ne se charge pas

- Vérifier que le dossier s'appelle exactement `redaction-tweets-viraux` et contient `SKILL.md` : `ls ~/.claude/skills/redaction-tweets-viraux/SKILL.md`.
- Ouvrir une nouvelle session Claude Code (la liste des skills est lue au démarrage).
- Nommer le skill dans la demande : « avec le skill redaction-tweets-viraux, … ».

## Le vérificateur ne se lance pas

- `python: command not found` : essayer `python3`, ou installer Python 3.10+.
- `Entrée illisible` (code 2) : le fichier n'existe pas ou n'est pas en UTF-8. Ré-enregistrer en UTF-8.
- Avec `-` comme fichier, l'entrée doit arriver sur l'entrée standard : `python scripts/verifier.py - < posts.txt`.

## Le vérificateur annonce un dépassement, mais X accepte le post

Le comptage est une approximation. Cas connus : compte X avec posts longs (utiliser `--limit`), et tout changement récent du compteur officiel. Le compteur de l'application fait foi.

## Le vérificateur ne voit pas mon fil

Les posts d'un fil sont séparés par une ligne contenant **uniquement** `---`. Sans elle, tout le texte est traité comme un seul post.

## Faux positif sur un chiffre

Le signal `chiffre-a-sourcer` (P2) liste tous les chiffres pour que vous les rattachiez au brief. Un chiffre du brief est légitime : ignorer le signal.

## Une limite de réseau a changé

Mettre à jour `NETWORKS` dans `scripts/verifier.py` et [../references/reseaux.md](../references/reseaux.md) (source et date) : voir [../CONTRIBUTING.md](../CONTRIBUTING.md).

Voir aussi : [INSTALLATION.md](INSTALLATION.md), [LIMITATIONS.md](LIMITATIONS.md).
