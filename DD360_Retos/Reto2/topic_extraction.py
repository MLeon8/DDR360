# topic_extraction.py


import re
import spacy

def preprocess_text(text):
    # Eliminar caracteres especiales y números
    text = re.sub(r'[^a-zA-ZáéíóúüÁÉÍÓÚÜñÑ\s]', '', text)
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar espacios adicionales
    text = re.sub(r'\s+', ' ', text).strip()
    # Lematización usando spaCy
    nlp = spacy.load('es_core_news_md')
    doc = nlp(text)
    lemmatized_text = ' '.join([token.lemma_ for token in doc])
    return lemmatized_text

def get_top_topics(row, topics_df, top_n):
    top_topics = topics_df.iloc[row.name].nlargest(top_n)
    return [topics_df.columns[i] for i in top_topics.index]
