# Ismwaen

Ismwaen est un dictionnaire numérique consacré aux noms de famille kabyles.

## Fonctionnement

- Recherche instantanée dans 2 100 fiches de noms.
- Variantes orthographiques et normalisation des accents et de la translittération.
- Fiches présentant la signification ou l'interprétation disponible, avec des renvois vers les noms associés.
- Base indépendante de l'interface : `dictionary.json`.
- Les interprétations formulées comme hypothèses sont signalées comme telles.

## Structure d'une fiche

`id`, `name`, `variants`, `meaning`, `shortMeaning`, `qualification`, `relatedNames`.

Les informations manquantes ne sont pas inventées. La base est conçue pour être enrichie et corrigée à mesure que de nouvelles connaissances sont validées.

## Publication

Le site est statique : `index.html` et `dictionary.json` doivent rester à la racine de `main`.
Pour GitHub Pages : Settings → Pages → Deploy from a branch → main → /(root).