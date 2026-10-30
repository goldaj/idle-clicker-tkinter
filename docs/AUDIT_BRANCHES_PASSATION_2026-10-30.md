# Audit GitHub et passation Idle Clicker — 30/10/2026

## État des branches
Branche de référence `main` : `caca2be5d2e08a7bbf46f5b2d5912bb91eb33196`.
- `chatgpt/review-20261024` (`0c4013ca122fc26c2cf583646e0d110b7121612b`) : behind, ahead 0, behind 21 ; contenu Git intégré ; candidate au nettoyage de la seule référence, après vérification.
- `feat/idle-purchase-advisor-autosave-20261029` (`86f4b1c5fb550f335e92ad241acb01f40848e7e5`) : behind, ahead 0, behind 19 ; contenu Git intégré ; candidate au nettoyage de la seule référence, après vérification.
- `fix/idle-exact-buy-max-20261029` (`0552e6cc9c37b5e190b0c5e55608d0040ee6a4bb`) : behind, ahead 0, behind 3 ; contenu Git intégré ; candidate au nettoyage de la seule référence, après vérification.

## PR
- [#3](https://github.com/goldaj/idle-clicker-tkinter/pull/3) : fusionnée (`fix/idle-exact-buy-max-20261029` → `main`).
- [#2](https://github.com/goldaj/idle-clicker-tkinter/pull/2) : fusionnée (`feat/idle-purchase-advisor-autosave-20261029` → `main`).
- [#1](https://github.com/goldaj/idle-clicker-tkinter/pull/1) : fusionnée (`chatgpt/review-20261024` → `main`).

## Challenge gameplay et persistance
Le conseiller d'achat doit rester **informatif**, pas automatiser les dépenses. Vérifier ration coûts/CPS, arrondis de Buy Max, nombres non finis et frontière des ressources restantes. En cas de fermeture/reprise, le timer d'autosave doit être annulé et la sauvegarde doit rester compatible avec les anciennes versions. Les tests purs n'établissent pas le bon comportement de Tkinter, du scaling écran ni des sauvegardes utilisateur réelles.

## Suite reproductible
1. Lire `docs/PURCHASE_ADVISOR_AUTOSAVE.md`, `AGENTS.md`, l'historique et README (« # Idle Clicker — jeu de progression Tkinter »).
2. Tester `python -m unittest discover -s tests -v`, puis cas limites de ressources et un essai GUI en conservant les saves privées.
3. Ajouter des tests de reprise/fermeture/recommandation après achats répétés avant toute nouvelle évolution d'équilibrage.

Audit statique seulement : pas de tests exécutés, de fusion, de suppression ni de modification de code pendant ce passage.
