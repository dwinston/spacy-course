import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Berlin is a nice city")

# Obtiens tous les tokens et les étiquettes de partie de discours
token_texts = [token.text for token in doc]
pos_tags = [token.pos_ for token in doc]

for index, pos in enumerate(pos_tags):
    # Vérifie si le token courant est un nom propre
    if pos == "PROPN":
        # Vérifie si le token suivant est un verbe
        if pos_tags[index + 1] == "VERB":
            result = token_texts[index]
            print("Found proper noun before a verb:", result)
