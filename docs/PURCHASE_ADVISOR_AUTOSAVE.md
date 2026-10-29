# Idle Clicker — Conseiller d'achats et sauvegarde automatique (2026-10-29)

## Travail réellement livré

La branche `feat/idle-purchase-advisor-autosave-20261029` existait mais était **strictement identique à `main`** : aucune amélioration n'y avait été commitée. Cette intervention a ajouté une vraie fonctionnalité sans supprimer le jeu ou ses sauvegardes :

- Encadré de **conseil stratégique** en jeu : parmi les bâtiments déjà découverts et le prochain bâtiment déblocable, calcule le meilleur **retour CPS/coût** pour l'achat d'une unité supplémentaire. Affiche le coût, les CPS gagnés, l'attente estimée pour disposer de l'or (en supposant une production CPS stable, **sans clic**), et la durée théorique d'amortissement.
- L'avis est informatif : **aucun achat automatique** n'a été ajouté. L'algorithme se trouve dans `idle_economy.py`, indépendamment de Tkinter ; il résiste aux données non finies et aux coûts qui débordent la plage numérique.
- Sauvegarde silencieuse **toutes les 60 secondes** avec `root.after`, en réutilisant la routine de sauvegarde atomique existante ; le minuteur est annulé à la fermeture. L'enregistrement sur demande et lors de la fermeture est conservé.
- Sept tests autonomes de calcul et régressions dans `tests/test_idle_economy.py`. Workflow Python 3.10/3.12 sans GUI, qui compile aussi le script Tkinter à titre de contrôle syntaxique.

## Utilisation

Depuis le dépôt avec Tkinter :

```bash
python -m pip install -r requirements.txt
python idle_clicker_v6_6_4.py
```

L'encadré apparaît entre les boutons Prestige et les effets visuels ; il se met à jour avec le niveau et l'or. L'autosave prend le même chemin que la sauvegarde manuelle `idle_save.json`. En cas d'arrêt brutal, la perte maximale visée est la progression depuis la dernière sauvegarde réussie (environ une minute), mais **ce n'est pas une garantie** en cas d'erreur du système de fichiers.

### Valider sans fenêtre

```bash
python -m unittest discover -s tests -p 'test_idle_economy.py' -v
python -m py_compile idle_clicker_v6_6_4.py idle_economy.py
```

Ces tests ne valident ni Tkinter sur Windows, ni le comportement des sauvegardes réelles. Le workflow est ajouté mais son résultat doit être consulté avant de déclarer la CI verte.

## Méthode de décision

La durée d'amortissement simplifiée est `coût_de_la_prochaine_unité / (CPS_unitaire * multiplicateur_de_prestige)`. Le prochain coût utilise le nombre d'unités déjà possédées et la croissance géométrique. Si le CPS est nul, aucune durée artificielle pour gagner la somme manquante n'est annoncée : **à financer par clics**. Le classement est reproductible, égalités départagées par coût puis nom.

**Limites de l'économie :** l'algorithme ne simule pas de stratégie multi-achats, ni de clics futurs, ni les gains de prestige, ni des changements de production. L'affichage indique donc « meilleur retour CPS », et **non** « stratégie optimale ». Un résultat de ROI favorable ne garantit pas l'équilibrage global du jeu.

## Suite Codex

1. Lire `README.md`, `AGENTS.md`, `docs/CHATGPT_PROJECT_HISTORY.md`, puis comparer la PR #1 de durcissement et sa branche `chatgpt/review-20261024` **avant toute fusion**. La nouvelle branche repart de `main` et n'a pas absorbé #1.
2. Vérifier Python 3.10/3.12 via Actions puis tester la fenêtre sur Windows (chargement, clic, achats, prestige, fermeture).
3. Tester explicitement l'autosave sur copie de sauvegarde factice : écriture après 60 s, écrasement atomique, retour après fermeture, fermeture rapide sans perte.
4. Auditer `buy_upgrade_max` et `_max_affordable_qty` pour les grands nombres. La formule de max peut différer du coût d'une véritable succession d'achats et la boucle peut se prolonger longtemps ; séparer le correctif en PR dédiée avec tests économiques exacts.
5. Mesurer l'équilibrage réel : simulations deterministic/monte-carlo des progressions avec 0, 1, 5 clics/s, comparer temps vers les premiers prestiges, éviter une optimisation seulement locale du ratio coût/CPS.
6. Ne pas effacer les sauvegardes personnelles, ne pas introduire d'accès réseau ou de télémetrie.

Aucune UI Tkinter n'a été lancée dans cette intervention ; aucune sauvegarde privée n'a été lue ou modifiée.
