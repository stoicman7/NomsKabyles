# Ismwaen

Ismwaen est un dictionnaire numérique consacré aux noms de famille kabyles.

## Structure

- index.html : interface publique, recherche instantanée et fiches.
- dictionary.json : base éditoriale structurée, séparée de l'interface.
- Les documents de travail présents dans le dépôt ne sont pas affichés aux visiteurs.

## Ajouter une fiche

Ajouter un objet dans le tableau entries de dictionary.json :

{
  "id": "nom-normalise",
  "name": "Nom",
  "variants": ["Variante 1", "Variante 2"],
  "shortMeaning": "Résumé court.",
  "meaning": "Explication complète.",
  "origin": "Origine linguistique ou géographique établie.",
  "etymology": "Analyse étymologique documentée.",
  "history": "Éléments historiques et culturels vérifiés.",
  "region": "Ancrage géographique, si connu.",
  "pronunciation": "Prononciation, si connue.",
  "notes": "Informations complémentaires.",
  "tags": ["Anthroponymie"],
  "qualification": "Précision sur le degré de certitude.",
  "sourceRefs": ["Références éditoriales internes"]
}

Les champs inconnus peuvent être omis. Ne pas inventer de signification : publier une fiche uniquement lorsque son contenu est suffisamment étayé. Les références internes ne sont jamais affichées dans l'interface publique.

La recherche gère les accents, la casse, les espaces, les variantes enregistrées et la translittération courante ɣ/gh.

## Publication

Publier index.html et dictionary.json ensemble à la racine de main. Pour GitHub Pages : Settings > Pages > Deploy from a branch > main > /(root).