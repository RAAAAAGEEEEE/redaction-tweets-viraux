# Limites

- **Aucune promesse de portée.** Le nom du skill dit « viraux » ; aucune étude citée ici ne mesure l'effet d'un style sur la portée. Les conseils d'accroche sont des pratiques observées (CLAIMED).
- **Pas d'évaluation du comportement du modèle.** Les 32 tests couvrent le vérificateur et la cohérence des cas de `evals/`. Rien ne mesure automatiquement si Claude choisit ce skill au bon moment ni si ses posts sont meilleurs ; les 7 cas de [../evals/](../evals/README.md) se rejouent à la main.
- **Longueurs approximatives.** Le poids X suit la configuration publique de `twitter-text` v3, non confirmée pour le compteur actuel de X ; les graphèmes de Bluesky sont approchés sans bibliothèque tierce ; Threads compte ici en graphèmes. Le compteur de l'application fait foi.
- **Posts longs X (Premium).** La limite de 25 000 caractères vient de sources tierces ; à vérifier dans l'application, puis à passer avec `--limit`.
- **Liens.** Sur Bluesky et Threads, le vérificateur compte le lien en entier, par prudence ; certains clients raccourcissent l'affichage.
- **Le vérificateur voit des formes, pas le sens.** Il ne repère ni un fait inventé, ni un fil dont les posts portent plusieurs idées. Il liste les chiffres pour que vous les rattachiez au brief.
- **Réseaux couverts.** X, Bluesky, Threads. Pas Instagram, LinkedIn, TikTok ni YouTube.
- **Limites datées.** Vérifiées le 2026-09-29 ; les réseaux les changent sans préavis.
- **Un skill ne publie pas.** Publier, programmer, répondre : hors périmètre par règle dure.

Voir aussi : [USAGE.md](USAGE.md), [../references/reseaux.md](../references/reseaux.md).
