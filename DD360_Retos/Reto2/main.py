#main

#
#pip install pandas folium spacy scikit-learn
#python -m spacy download es_core_news_md
#python main.py
#


import pandas as pd
import folium
import webbrowser
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from topic_extraction import preprocess_text, get_top_topics


def main():
    # Cargar datos
    places_df = pd.read_csv('places_details.csv')
    reviews_df = pd.read_csv('places_reviews.csv')

    # Extraer temas principales de las reseñas
    topics_df = extract_topics(reviews_df)
    places_df['Top Topics'] = places_df.apply(get_top_topics, args=(topics_df, 3), axis=1)

    # Crear el mapa
    map = folium.Map(location=[places_df['latitude'].mean(), places_df['longitude'].mean()], zoom_start=12)

    for _, row in places_df.iterrows():
        name = row['name']
        latitude = row['latitude']
        longitude = row['longitude']
        top_topics = row['Top Topics']
        website = row['website']

        # Colocar marcadores en el mapa
        popup_html = f"<b>{name}</b><br>Temas principales: {', '.join([topic_descriptions[i] for i in top_topics])}"
        if pd.notnull(website):
            popup_html += f"<br><a href='{website}' target='_blank'>Visitar sitio web</a>"
        
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color=get_marker_color(row['rating']))
        ).add_to(map)

    # Guardar el mapa en un archivo HTML
    map.save('map.html')
    print("Mapa generado y guardado como 'map.html'.")

def extract_topics(reviews):
    # Cargar modelo de lenguaje de spaCy para español
    nlp = spacy.load('es_core_news_md')

    # Preprocesar el texto de las reseñas
    reviews['text'] = reviews['text'].apply(preprocess_text)

    # Vectorizar el texto utilizando CountVectorizer
    vectorizer = CountVectorizer(stop_words='spanish')
    X = vectorizer.fit_transform(reviews['text'])

    # Obtener los nombres de los temas
    topics = vectorizer.get_feature_names_out()

    # Crear un DataFrame para almacenar los resultados
    topics_df = pd.DataFrame(X.toarray(), columns=topics)

    return topics_df

def get_marker_color(rating):
    if rating >= 4.5:
        return 'green'
    elif rating >= 4.0:
        return 'yellow'
    elif rating >= 3.0:
        return 'red'
    else:
        return 'blue'

if __name__ == "__main__":
    main()
