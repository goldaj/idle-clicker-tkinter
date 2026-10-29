# Idle Clicker — jeu de progression Tkinter
Run:
```bash
python idle_clicker_v6_6_4.py
```

Dans un environnement virtuel, installer les dépendances avec `python -m pip install -r requirements.txt`. Python doit inclure Tkinter. Les sauvegardes `idle_save.json` et leurs copies restent locales et sont ignorées par Git.

## Situer ce prototype parmi les autres jeux

| Projet | Expérience explorée | Organisation du code |
| --- | --- | --- |
| [Moonrail](https://github.com/goldaj/moonrail-narrative-deckbuilder) | Deckbuilding narratif, collection et progression persistante | Projet distinct, avec sa direction de produit et ses personnages |
| [Bestiaire](https://github.com/goldaj/roguelite-bestiary-deckbuilder) | Créatures, cartes et attrition persistante au fil des combats | Prototype autonome, moteur `core/` et tests ; progression encore à corriger |
| [DeckLite](https://github.com/goldaj/decklite-roguelite-deckbuilder) | Construire son deck pendant une run, choisir des récompenses, événements et boutique méta | Prototype Pygame concentré dans `main.py` |
| [Exploration sur tuiles](https://github.com/goldaj/tilemap-exploration-roguelite) | Se déplacer sur une grille, rencontrer des ennemis, gérer objets et boutique | Modules monde/combat/interface, tuiles et sprites |
| [Chess Roguelite](https://github.com/goldaj/chess-roguelite) | Déplacer des pièces d'échecs et acquérir des améliorations entre les affrontements | Plateau, IA, progression et interface souris |
| [Idle Clicker](https://github.com/goldaj/idle-clicker-tkinter) | Clics, revenus et achats avec coût dynamique | Interface de bureau Tkinter/ttkbootstrap |

Ces dépôts conservent des expériences distinctes, à différents niveaux d'avancement.

## Évolution : conseil d'achat et autosave (29 octobre 2026)

Sur la branche `feat/idle-purchase-advisor-autosave-20261029`, le jeu ajoute un conseiller d'achat en bas de la zone de prestige : **meilleur retour CPS/coût parmi les améliorations visibles**, temps approximatif pour pouvoir acheter avec le seul revenu passif, et délai d'amortissement. Il **ne réalise aucun achat automatiquement**. Sauvegarde locale silencieuse chaque minute, en plus de l'enregistrement manuel et à la fermeture.

Contrôles sans fenêtre : `python -m unittest discover -s tests -p 'test_idle_economy.py' -v`. Guide et limites : [docs/PURCHASE_ADVISOR_AUTOSAVE.md](docs/PURCHASE_ADVISOR_AUTOSAVE.md). La suite complète Tkinter/Windows et les sauvegardes réelles doivent être testées avant fusion. La branche part de `main` et **n'intègre pas** la PR #1 de durcissement des nombres non finis.

## Achat maximum exact et sûr — reprise 2026-10-29

La branche empilée `fix/idle-exact-buy-max-20261029` corrige le bouton **Max**. Le cumul utilise désormais exactement les **mêmes prix entiers arrondis individuellement** que les achats simples, et évite les boucles non bornées en limitant le calcul à 10 000 achats par clic. Si cette borne est atteinte alors que d'autres unités sont encore achetables, le jeu le signale. Les coûts débordant la plage numérique deviennent indisponibles (au lieu de revenir au prix initial). Voir `docs/EXACT_BULK_PURCHASE.md`, avec tests sans interface.
