from spacy.lang.en import English

nlp = English()

# Importe les classes Doc et Span
from spacy.tokens import Doc, Span

words = ["I", "like", "David", "Bowie"]
spaces = [True, True, True, False]

# Crée un doc à partir des mots et des espaces
doc = Doc(nlp.vocab, words=words, spaces=spaces)
print(doc.text)

# Crée un span pour "David Bowie" à partir du doc
# et assigne-lui le label "PERSON"
span = Span(doc, 2, 4, label="PERSON")
print(span.text, span.label_)

# Ajoute le span aux entités du doc
doc.ents = [span]

# Affiche les textes et les labels des entités
print([(ent.text, ent.label_) for ent in doc.ents])
