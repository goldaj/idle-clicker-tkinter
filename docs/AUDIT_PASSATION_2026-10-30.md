# Audit et passation contradictoire — goldaj/idle-clicker-tkinter (2026-10-30)

Inspection GitHub des branches (4), PR (3) et fichiers ; aucune partie simulée ni interface graphique lancée.

## Références
`main` à `a901d45b60348778281733e5d519e80592d9088f`.
- `chatgpt/review-20261024` (`0c4013ca122fc26c2cf583646e0d110b7121612b`) : behind, 0 exclusif(s), 19 derrière ; historique absorbé, candidate nettoyage.
- `feat/idle-purchase-advisor-autosave-20261029` (`86f4b1c5fb550f335e92ad241acb01f40848e7e5`) : behind, 0 exclusif(s), 17 derrière ; historique absorbé, candidate nettoyage.
- `fix/idle-exact-buy-max-20261029` (`0552e6cc9c37b5e190b0c5e55608d0040ee6a4bb`) : behind, 0 exclusif(s), 1 derrière ; historique absorbé, candidate nettoyage.

## PR
- [#3](https://github.com/goldaj/idle-clicker-tkinter/pull/3) : fusionnée (closed) : fix: exact bounded Buy Max with rounded unit costs and regression tests
- [#2](https://github.com/goldaj/idle-clicker-tkinter/pull/2) : fusionnée (closed) : feat: Idle Clicker live upgrade advisor and 60-second autosave
- [#1](https://github.com/goldaj/idle-clicker-tkinter/pull/1) : fusionnée (closed) : [ChatGPT] Sécurisation des nombres non finis et tests GUI indépendants

## Fichiers
`.github`, `.gitignore`, `AGENTS.md`, `README.md`, `docs`, `idle_clicker_v6_6_4.py`, `idle_economy.py`, `requirements.txt`, `tests`.

## Remise en cause / prochaines preuves
1. Tester rigoureusement le calcul `Buy Max` avec erreurs flottantes, arrondis, achats à fonds limités et montée de prix après chaque achat ; comparer à une implémentation de référence brute.
2. Tester autosave à 60 secondes, crash, fermeture forcée, corruption de sauvegarde, migration et reprise de partie.
3. Mesurer la pertinence de l'advisor d'upgrade sous plusieurs stratégies initiales, pas seulement une trajectoire optimale théorique.
4. Vérifier blocage potentiel de Tkinter et fréquence des boucles UI en longue session.
5. Les trois branches de correction ont 0 commit exclusif. Vérifier workflows et PR avant suppression, ne pas rouvrir de PR pour le même code.

Aucun test exécuté, aucun changement de production durant l'audit.
