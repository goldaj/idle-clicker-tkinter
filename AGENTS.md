# AGENTS.md — Idle Clicker

## Avant toute intervention
- Lire `README.md`, puis **`docs/CHATGPT_PROJECT_HISTORY.md`** pour les décisions de conception et les limites documentaires. Consulter ensuite les documents spécialisés cités par le README.
- Mission : Jeu incrémental desktop Tkinter/ttkbootstrap (version source v6.6.4), clics, revenus et améliorations.
- Invariants : Préserver les sauvegardes personnelles non versionnées et l'application desktop autonome.

## Exécution
- `python -m pip install -r requirements.txt` puis `python idle_clicker_v6_6_4.py`.
- Préserver le travail préexistant, les versions anciennes et les fichiers non concernés. Valider uniquement ce qui peut être vérifié dans l'environnement disponible.

## Continuité du contexte
- Après toute modification de projet, consulter et enrichir `docs/CHATGPT_PROJECT_HISTORY.md` avec les échanges fournis, les décisions et le résultat de la validation.
- Distinguer `Utilisateur (verbatim)`, `Assistant (verbatim)` et `Résumé reconstruit (non verbatim)`. Donner date et heure uniquement si attestées, sinon noter qu'elles manquent.
- Ne pas inventer d'échanges ou de tests. Si une transcription n'est pas accessible, demander son export plutôt que supposer son contenu.
- Le dépôt peut être public : expurger secrets, données personnelles et contenus ne relevant pas du projet. Ne pas écraser les éléments historiques.

## Travail 2026-10-29 : conseiller économique et autosave

Lire `docs/PURCHASE_ADVISOR_AUTOSAVE.md` avant toute modification. La branche `feat/idle-purchase-advisor-autosave-20261029` repart de `main`, a été trouvée initialement sans commit, et ne comprend pas encore la PR #1 (`chatgpt/review-20261024`) sur les nombres non finis.

- `idle_economy.py` : règles pures de choix selon ratio coût/CPS, ETA sans clic, temps d'amortissement, garde coûts non finis. **Informatif uniquement**, aucun achat automatisé.
- `idle_clicker_v6_6_4.py` : encadré de recommandation recalculé avec les statistiques, `root.after` d'autosave toutes les 60s, annulation du minuteur à la fermeture.
- `tests/test_idle_economy.py`, `.github/workflows/idle-economy.yml` : tests sans Tkinter, CI Python 3.10/3.12 et compilation syntaxique. Cela ne constitue pas un test de l'interface ou de la sauvegarde sur disque.
- Vérifier la PR et ses checks, tester sur Windows avec une **copie** d'`idle_save.json`, puis auditer les grands achats Max, l'équilibrage économique et les temps vers prestige. Ne pas revendiquer un algorithme économiquement optimal ; seulement le meilleur ratio local parmi les options visibles.
