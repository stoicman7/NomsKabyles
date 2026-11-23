# Ismwaen

Site de recherche documentaire consacré aux noms de famille kabyles.

## Fonctionnement

- Recherche dans les textes des deux PDF présents à la racine du dépôt.
- PDF.js extrait le texte directement dans le navigateur.
- Chaque résultat affiche un extrait, le document et le numéro de page.
- Recherche insensible à la casse et aux accents.
- Aucun nom ni aucune requête n'est envoyé à un serveur applicatif.

## Déploiement

Le site est statique : `index.html` et les deux PDF doivent rester dans le même répertoire.
Pour publier avec GitHub Pages, ouvrir **Settings → Pages**, sélectionner **Deploy from a branch**, puis choisir `main` et `/(root)`.
