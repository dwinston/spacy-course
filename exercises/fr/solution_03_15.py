import json
from spacy.lang.en import English
from spacy.tokens import Doc

with open("exercises/en/bookquotes.json") as f:
    DATA = json.loads(f.read())

nlp = English()

# Déclare l'extension de Doc "author" (défaut None)
Doc.set_extension("author", default=None)

# Déclare l'extension de Doc "book" (default None)
Doc.set_extension("book", default=None)

for doc, context in nlp.pipe(DATA, as_tuples=True):
    # Définis les attributs doc._.book et doc._.author à partir du contexte
    doc._.book = context["book"]
    doc._.author = context["author"]

    # Affiche le texte et les données des attributs personnalisés
    print(f"{doc.text}\n — '{doc._.book}' by {doc._.author}\n")
