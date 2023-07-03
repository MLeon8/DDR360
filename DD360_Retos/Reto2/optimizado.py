import pandas as pd
import folium
import webbrowser
import spacy
from spacy.lang.es.stop_words import STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer

# Función para preprocesar el texto
def preprocess_text(text, nlp):
    # Verificar que el texto sea una cadena de texto (string) válida
    if isinstance(text, str):
        # Convertir el texto a minúsculas
        text = text.lower()
        # Tokenizar el texto y eliminar espacios en blanco y caracteres especiales
        tokens = [token.text for token in nlp(text) if not token.is_space and not token.is_punct]
        # Eliminar palabras vacías (stop words)
        tokens = [token for token in tokens if token not in STOP_WORDS]
        # Unir los tokens procesados para formar el texto preprocesado
        processed_text = " ".join(tokens)
        return processed_text
    return ""

def preprocess_data():
    # Cargar los datos de los archivos CSV
    places_df = pd.read_csv('places details.csv')
    reviews_df = pd.read_csv('places_reviews.csv')
    
    # Crear el objeto spaCy para el procesamiento de texto
    nlp = spacy.load('es_core_news_sm', disable=['ner', 'parser'])
    
    # Preprocesar los textos de las reseñas
    reviews_df['texto'] = reviews_df['text'].apply(preprocess_text, nlp=nlp)
    
    # Fusionar los DataFrames de lugares y reseñas en base al place_id
    df = pd.merge(places_df, reviews_df, on='place_id', how='inner')
    
    # Eliminar columnas innecesarias
    df.drop(['reviewer', 'reviewer_avatar', 'datetime', 'text', 'language', 'id'], axis=1, inplace=True)
    
    return df

if __name__ == "__main__":
    # Procesar los datos
    df = preprocess_data()
    
    # Imprimir los primeros 5 registros
    print(df.head())
