import pandas as pd
import requests
from bs4 import BeautifulSoup
import spacy
from spacy.lang.es import Spanish
import concurrent.futures
import folium

# Descarga el modelo de español de spaCy (solo es necesario hacerlo una vez)
# python -m spacy download es_core_news_sm

def extract_name_and_location(text):
    # Cargar el modelo de lenguaje de spaCy
    nlp = Spanish()

    # Analizar el texto utilizando spaCy
    doc = nlp(text)

    # Buscar patrones que sugieran el nombre del lugar y la ubicación
    place_name = ""
    location = ""

    for token in doc:
        # Buscar palabras clave que sugieran el nombre del lugar
        if token.text.lower() in ["nombre", "lugar"]:
            next_token = token.i + 1
            while next_token < len(doc) and not doc[next_token].is_stop:
                place_name += doc[next_token].text + " "
                next_token += 1

        # Buscar palabras clave que sugieran la ubicación
        if token.text.lower() in ["ubicación", "dirección"]:
            next_token = token.i + 1
            while next_token < len(doc) and not doc[next_token].is_stop:
                location += doc[next_token].text + " "
                next_token += 1

    return place_name.strip(), location.strip()

def get_place_info_from_url(url):
    # Agregar tiempo de espera (timeout) en la solicitud
    try:
        if pd.notna(url):  # Verificar que la URL no sea nula (NaN)
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # Resto del código igual...
    except requests.exceptions.Timeout:
        print(f"Tiempo de espera agotado para la solicitud: {url}")
    except Exception as e:
        print(f"Error al obtener detalles del lugar con URL: {url}")
    return None, None

def main():
    # Cargar el archivo CSV en un DataFrame usando pandas
    df = pd.read_csv("places_reviews.csv")

    # Calcular el promedio de rating por place_id
    ratings_avg = df.groupby("place_id")["rating"].mean()

    # Lista para almacenar las coordenadas de ubicación
    locations = []

    # Utilizar ThreadPoolExecutor para ejecutar las solicitudes de forma paralela
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        # Iterar por cada place_id para obtener el nombre del lugar y su ubicación
        future_to_url = {executor.submit(get_place_info_from_url, url): url for url in df["url"].tolist()}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            place_name, location = future.result()

            if place_name and location:
                # Guardar el nombre del lugar, ubicación y promedio de rating en un nuevo DataFrame
                # Podemos contar las filas del grupo para obtener la cantidad de personas que evaluaron el lugar
                place_id = df[df["url"] == url]["place_id"].values[0]
                num_reviews = len(df[df["place_id"] == place_id])
                avg_rating = ratings_avg[place_id]
                df_result = pd.DataFrame({"place_id": [place_id], "place_name": [place_name], "location": [location], "avg_rating": [avg_rating], "num_reviews": [num_reviews]})
                # Guardar los resultados en un archivo llamado "places_info.csv"
                df_result.to_csv("places_info.csv", mode="a", header=False, index=False)
                locations.append((place_name, location))

    # Crear mapa con folium
    map_center = [40.0, -3.0]  # Coordenadas del centro del mapa
    map_places = folium.Map(location=map_center, zoom_start=5)

    for place_name, location in locations:
        # Agregar marcadores al mapa
        if location:
            location_split = location.split()
            try:
                lat = float(location_split[0])
                lon = float(location_split[1])
                popup_text = f"{place_name}<br>Ubicación: {location}"
                folium.Marker(location=[lat, lon], popup=popup_text).add_to(map_places)
            except ValueError:
                print(f"No se pudo agregar el marcador para {place_name}, ubicación no válida: {location}")

    # Guardar el mapa en un archivo HTML
    map_places.save("places_map.html")

    # Análisis de PLN
    # Vamos a suponer que un sitio es "bueno" si su promedio de rating es mayor o igual a 4.0 y el texto contiene la palabra "bueno"
    # Utilizamos un valor booleano por defecto False para los casos donde no podamos determinar si es "bueno" o no
    df["is_good_site"] = (df["rating"] >= 4.0) & df["text"].apply(lambda x: "bueno" in x.lower() if isinstance(x, str) else False)

    # Contar cuántos sitios son considerados "buenos"
    num_good_sites = df[df["is_good_site"] == True].shape[0]

    print(f"Se han evaluado {num_good_sites} sitios como 'buenos'.")

if __name__ == "__main__":
    main()
