import spacy
from spacy.lang.es.stop_words import STOP_WORDS
import re

nlp = spacy.load('es_core_news_md')

def preprocess_text(text):
    # Tokenizar el texto
    doc = nlp(text)

    # Convertir a minúsculas, eliminar espacios y caracteres especiales, y eliminar stopwords
    tokens = [token.text.lower() for token in doc if not token.is_space and not token.is_punct and not token.is_stop]

    # Unir los tokens en un texto preprocesado
    preprocessed_text = " ".join(tokens)

    return preprocessed_text

def get_top_topics(topics_df, n):
    # Obtener los nombres de los temas con las puntuaciones más altas
    top_topics = topics_df.sum().nlargest(n).index.tolist()
    
    return top_topics
