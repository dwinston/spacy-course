def test():
    assert "spacy.load" in __solution__, "Appelles-tu spacy.load ?"
    assert nlp.meta["lang"] == "en", "Charges-tu le bon modèle ?"
    assert nlp.meta["name"] == "core_web_sm", "Charges-tu le bon modèle ?"
    assert "nlp(text)" in __solution__, "Traites-tu correctement le texte ?"
    assert "print(doc.text)" in __solution__, "Affiches-tu le texte du Doc ?"

    __msg__.good(
        "Bien joué ! Mainteant que tu as pratiqué le chargement de modèles, "
        "voyons quelques-unes de leurs prédictions."
    )
