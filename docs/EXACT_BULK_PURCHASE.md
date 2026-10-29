# Achat maximum fiable — correctif isolé 2026-10-29

## Problème réel

Le bouton `Max` de `idle_clicker_v6_6_4.py` était une boucle `while True` achetant une unité par itération, sans borne : sur une sauvegarde riche ou corrompue, l'interface Tkinter pouvait être bloquée. La méthode auxiliaire `_max_affordable_qty` utilisait une somme géométrique **non arrondie** alors que chaque achat réel coûte `round(base * multiplicateur ** owned)`. Ces deux règles ne sont pas interchangeables. Enfin, `_upgrade_cost` revenait au **prix de base** si le calcul débordait la plage numérique, ce qui pouvait rendre à nouveau bon marché une amélioration inaccessible.

## Fonctionnalités livrées

- `idle_economy.plan_bulk_purchase` calcule la quantité, la somme entière dépensée et le solde, en utilisant **le prix arrondi de chaque unité**. Le coût unitaire est désormais représenté par un entier Python, plutôt qu'une conversion inutile de ce prix arrondi en float.
- Le calcul comporte une limite de **10 000 achats maximum par clic**, configurée pour les tests. Si cette limite empêche d'acheter toutes les unités encore abordables, `capped=True` provoque un avertissement clair au joueur. Le bouton ne prétend plus effectuer un véritable achat maximum dans ce cas extrême.
- Les dépenses sont additionnées comme **entiers**, évitant l'illusion d'achats gratuits quand l'or est immense et qu'un petit débit serait indiscernable en flottant.
- Les coûts non finis deviennent indisponibles, sans repli dangereux sur le prix initial. `format_num` affiche `∞` lorsqu'une valeur positive déborde au lieu de tenter un logarithme impossible.
- La méthode existante `_max_affordable_qty` s'appuie maintenant sur le même moteur que le bouton, garantissant leur cohérence.

## Contrats de test

`tests/test_bulk_purchase.py` compare le résultat du moteur à **250 simulations déterministes d'achats unitaires**, avec plusieurs valeurs de croissance, de stocks et de budgets. Elle couvre aussi un seuil d'arrondi, le plafond d'itérations, les énormes budgets sans blocage et les entrées invalides.

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python -m py_compile idle_clicker_v6_6_4.py idle_economy.py
```

Ces tests ne créent pas de fenêtre Tkinter et ne lisent pas de sauvegarde. Les tests CI doivent encore être observés pour confirmer leur exécution avant annonce de réussite. **Aucun gameplay manuel Windows n'est validé** dans ce correctif.

## Concurrence, reprise Codex et limites

La branche `fix/idle-exact-buy-max-20261029` dérive du commit de la PR de conseiller d'achats / autosave `feat/idle-purchase-advisor-autosave-20261029`. **Ne pas fusionner ce correctif avant la PR parent**, ni écraser la PR #1 de durcissement indépendant ; comparer les diffs et les tests avant la convergence.

Pour le produit, l'achat Max exact ne garantit absolument pas l'équilibrage des prix, la durée vers le prestige ou une expérience satisfaisante. Les prochains tests pertinents sont des simulations économiques de parcours sur plusieurs politiques de clic/achats et des tests GUI sur poste Windows avec copie d'une sauvegarde.

Règles : préserver les données locales et historiques ; ne pas intégrer des fichiers `idle_save.json` à Git ; ne pas fusionner sans revue ; mettre à jour `AGENTS.md` et `docs/CHATGPT_PROJECT_HISTORY.md` à chaque reprise.
