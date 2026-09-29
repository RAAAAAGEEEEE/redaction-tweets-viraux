#!/usr/bin/env python3
"""Contrôle mécanique de posts (X, Bluesky, Threads) avant publication.

Compte la longueur selon les règles du réseau et signale ce qu'une
consigne ne suffit pas à empêcher : dépassement de limite, tiret cadratin,
placeholder oublié, hashtags en trop, émojis, chiffres à rattacher au brief.

Usage :
    python scripts/verifier.py posts.txt --network x
    python scripts/verifier.py fil.txt --network bluesky
    python scripts/verifier.py - --network threads < posts.txt

Format d'entrée : un post par bloc ; un fil sépare ses posts par une ligne
contenant seulement `---`.

Code de sortie : 0 = aucun P0, 1 = au moins un P0, 2 = entrée illisible.
Bibliothèque standard seulement, aucun accès réseau. Les longueurs sont une
approximation des règles officielles (voir docs/LIMITATIONS.md).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass

VERSION = "1.2.0"

EM_DASH = "—"

# Limites documentées (état au 2026-09-29, voir references/reseaux.md).
NETWORKS = {
    "x": {"limit": 280, "hashtags": 3, "links": None},
    "bluesky": {"limit": 300, "hashtags": 3, "links": None},
    "threads": {"limit": 500, "hashtags": 1, "links": 5},
}

URL_RE = re.compile(r"(?:https?://|www\.)[^\s]+", re.I)
HASHTAG_RE = re.compile(r"(?<![\w&])#(?=\w*[^\W\d_])\w+", re.U)
PLACEHOLDER_RE = re.compile(
    r"\[(ville|nom|pr[ée]nom|entreprise|produit|client|lien|url|prix|chiffre)\]|\{\{[^}]+\}\}|\bTODO\b|\bXXX\b|\blorem ipsum\b",
    re.I,
)
OPEN_ITEM_RE = re.compile(r"\[\[\s*[àa] confirmer[^\]]*\]\]", re.I)
AI_TICS = [
    (r"\bdans un monde o[ùu]\b", "remplissage d'ouverture"),
    (r"\bplongeons\b", "élan avant le propos"),
    (r"\bil est important de (noter|souligner)\b", "remplissage"),
    (r"\ben conclusion\b", "conclusion annoncée"),
    (r"\bn'h[ée]sitez pas\b", "formule de chatbot"),
    (r"\bj'esp[èe]re que (cela|ceci|ça)\b", "formule de chatbot"),
    (r"\bce n'est pas [^.;:!?]{1,60}, c'est\b", "faux contraste « ce n'est pas X, c'est Y »"),
    (r"\bvoici (pourquoi|comment|ce que)\b", "annonce creuse (à garder seulement si le post tient sa promesse)"),
]
NUMBER_RE = re.compile(r"\d[\d   ,.]*\d|\d")
ORDINAL_RE = re.compile(r"\b(?:[ée]tape|point|conseil|astuce|r[èe]gle|n°)\s*\d{1,2}\b", re.I)
THREAD_INDEX_RE = re.compile(r"^\s*\(?\d{1,2}\s*/\s*\d{0,2}\)?")
EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF☀-➿⭐⬆↔-⇿️]")

# Poids X (twitter-text v3) : 1 caractère pour ces plages, 2 pour le reste.
X_LIGHT_RANGES = ((0x0000, 0x10FF), (0x2000, 0x200D), (0x2010, 0x201F), (0x2032, 0x2037))
X_URL_LENGTH = 23


@dataclass
class Finding:
    priority: str  # P0, P1, P2
    rule: str
    post: int
    excerpt: str
    message: str


# --- Longueurs -----------------------------------------------------------

def graphemes(text: str) -> list[str]:
    """Approximation des clusters de graphèmes (sans bibliothèque tierce) :
    marques combinantes, sélecteurs de variation, modificateurs de teint,
    séquences ZWJ, drapeaux (paires d'indicateurs régionaux), CRLF."""
    clusters: list[str] = []
    joined = False
    for ch in text:
        cp = ord(ch)
        cat = unicodedata.category(ch)
        extends = (
            cat in ("Mn", "Me", "Mc")
            or cp == 0x200D
            or 0x1F3FB <= cp <= 0x1F3FF
            or 0xE0020 <= cp <= 0xE007F
        )
        if clusters and (extends or joined):
            if ch == "\n" and clusters[-1] == "\r":
                pass
            clusters[-1] += ch
            joined = cp == 0x200D
            continue
        if (
            clusters
            and 0x1F1E6 <= cp <= 0x1F1FF
            and len(clusters[-1]) == 1
            and 0x1F1E6 <= ord(clusters[-1]) <= 0x1F1FF
        ):
            clusters[-1] += ch
            continue
        if ch == "\n" and clusters and clusters[-1] == "\r":
            clusters[-1] += ch
            continue
        clusters.append(ch)
        joined = cp == 0x200D
    return clusters


def _is_emoji_cluster(cluster: str) -> bool:
    return any(0x1F000 <= ord(c) <= 0x1FAFF or 0x2600 <= ord(c) <= 0x27BF or ord(c) == 0xFE0F for c in cluster)


def _x_weight(ch: str) -> int:
    cp = ord(ch)
    return 1 if any(lo <= cp <= hi for lo, hi in X_LIGHT_RANGES) else 2


def _split_urls(text: str) -> tuple[str, int]:
    urls = URL_RE.findall(text)
    return URL_RE.sub("", text), len(urls)


def length_x(text: str) -> int:
    rest, n_urls = _split_urls(text)
    total = 0
    for cluster in graphemes(rest):
        if _is_emoji_cluster(cluster):
            total += 2
        else:
            total += sum(_x_weight(c) for c in cluster)
    return total + X_URL_LENGTH * n_urls


def length_bluesky(text: str) -> int:
    return len(graphemes(text))


def length_threads(text: str) -> int:
    return len(graphemes(text))


LENGTH = {"x": length_x, "bluesky": length_bluesky, "threads": length_threads}


# --- Découpage et contrôles ---------------------------------------------

def split_posts(text: str) -> list[str]:
    posts = re.split(r"(?m)^\s*---\s*$", text)
    return [p.strip("\n").strip() for p in posts if p.strip()]


def excerpt(text: str, width: int = 50) -> str:
    flat = " ".join(text.split())
    return flat if len(flat) <= width else flat[: width - 1] + "…"


def check_post(index: int, post: str, network: str, limit: int, allow_emoji: bool, is_last: bool):
    cfg = NETWORKS[network]
    found: list[Finding] = []
    length = LENGTH[network](post)
    if length > limit:
        found.append(Finding("P0", "longueur", index, f"{length}/{limit}", f"Dépasse la limite de {limit} sur {network} ({length})."))
    if network == "bluesky" and len(post.encode("utf-8")) > 3000:
        found.append(Finding("P0", "longueur-octets", index, str(len(post.encode("utf-8"))), "Dépasse 3000 octets (limite technique Bluesky)."))
    if EM_DASH in post:
        found.append(Finding("P0", "cadratin", index, excerpt(post[max(0, post.index(EM_DASH) - 20): post.index(EM_DASH) + 20]), "Tiret cadratin interdit : virgule, deux-points, parenthèses ou point."))
    m = PLACEHOLDER_RE.search(post)
    if m:
        found.append(Finding("P0", "placeholder", index, m.group(0), "Placeholder oublié."))
    for m in OPEN_ITEM_RE.finditer(post):
        found.append(Finding("P1", "a-confirmer", index, m.group(0), "Point à confirmer avant publication."))
    tags = HASHTAG_RE.findall(post)
    if len(tags) > cfg["hashtags"]:
        found.append(Finding("P1", "hashtags", index, " ".join(tags), f"{len(tags)} hashtags, maximum {cfg['hashtags']} sur {network}."))
    links = URL_RE.findall(post)
    if cfg["links"] is not None and len(links) > cfg["links"]:
        found.append(Finding("P0", "liens", index, str(len(links)), f"Plus de {cfg['links']} liens : refusé par {network}."))
    if not allow_emoji and EMOJI_RE.search(post):
        found.append(Finding("P1", "emoji", index, EMOJI_RE.search(post).group(0), "Émoji : interdit par défaut, seulement sur demande pour ce post."))
    for pat, msg in AI_TICS:
        mm = re.search(pat, post, re.I)
        if mm:
            found.append(Finding("P1", "formule-ia", index, mm.group(0), msg))
    for mm in re.finditer(r"(?<=[^\s  (])([?!:;])(?=\s|$)", post):
        before = post[max(0, mm.start() - 10): mm.start()]
        if mm.group(1) == ":" and re.search(r"(https?|www|\d)$", before):
            continue
        found.append(Finding("P1", "espace-ponctuation", index, excerpt(post[max(0, mm.start() - 15): mm.end()]), "Une espace (insécable de préférence) précède « : ; ! ? » en français."))
        break
    body = ORDINAL_RE.sub("", THREAD_INDEX_RE.sub("", URL_RE.sub("", post)))
    numbers = [n.strip() for n in NUMBER_RE.findall(body)]
    if numbers:
        found.append(Finding("P2", "chiffre-a-sourcer", index, ", ".join(dict.fromkeys(numbers))[:60], "Chaque chiffre doit venir du brief ou d'une source citée."))
    if is_last and "?" not in post and not OPEN_ITEM_RE.search(post):
        found.append(Finding("P2", "pas-de-question-finale", index, excerpt(post[-40:]), "Le dernier post se termine par une question qui appelle une réponse (règle par défaut)."))
    return length, found


def verify(text: str, network: str = "x", limit: int | None = None, allow_emoji: bool = False):
    limit = limit or NETWORKS[network]["limit"]
    posts = split_posts(text)
    findings: list[Finding] = []
    lengths: list[int] = []
    for i, post in enumerate(posts, 1):
        length, found = check_post(i, post, network, limit, allow_emoji, i == len(posts))
        lengths.append(length)
        findings.extend(found)
    if not posts:
        findings.append(Finding("P0", "vide", 0, "", "Aucun post trouvé dans l'entrée."))
    return lengths, findings


def render(network: str, limit: int, lengths: list[int], findings: list[Finding]) -> str:
    counts = {p: sum(f.priority == p for f in findings) for p in ("P0", "P1", "P2")}
    out = [f"verifier.py {VERSION} [{network}, limite {limit}] : P0={counts['P0']} P1={counts['P1']} P2={counts['P2']}"]
    for i, n in enumerate(lengths, 1):
        out.append(f"  post {i} : {n}/{limit}")
    for f in findings:
        where = f"post {f.post}" if f.post else "texte"
        out.append(f"  {f.priority} [{f.rule}] {where} : {f.excerpt}")
        out.append(f"      {f.message}")
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Contrôle mécanique de posts X, Bluesky ou Threads.")
    parser.add_argument("fichier", help="chemin du texte, ou - pour l'entrée standard")
    parser.add_argument("--network", choices=sorted(NETWORKS), default="x", help="réseau visé (défaut : x)")
    parser.add_argument("--limit", type=int, help="limite de longueur à la place de celle du réseau (ex. compte X Premium)")
    parser.add_argument("--allow-emoji", action="store_true", help="ne pas signaler les émojis")
    parser.add_argument("--json", action="store_true", help="sortie JSON")
    args = parser.parse_args(argv)
    try:
        if args.fichier == "-":
            text = sys.stdin.buffer.read().decode("utf-8")
        else:
            with open(args.fichier, encoding="utf-8") as fh:
                text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Entrée illisible : {exc}", file=sys.stderr)
        return 2
    limit = args.limit or NETWORKS[args.network]["limit"]
    lengths, findings = verify(text, args.network, limit, args.allow_emoji)
    if args.json:
        payload = {"network": args.network, "limit": limit, "lengths": lengths, "findings": [asdict(f) for f in findings]}
        sys.stdout.buffer.write(json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8") + b"\n")
    else:
        sys.stdout.buffer.write(render(args.network, limit, lengths, findings).encode("utf-8") + b"\n")
    return 1 if any(f.priority == "P0" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
