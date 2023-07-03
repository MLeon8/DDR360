import pandas as pd
import googlemaps
from geopy.geocoders import Nominatim

GOOGLE_MAPS_API_KEY = "AIzaSyAFvAM7FQhWRWvgUeGIIr7aIW2Yev2IoHg"

def extract_coordinates(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None

def get_place_info_from_url(url):
    gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    # Extraemos el ID del lugar del URL (última parte después de !2s)
    place_id = url.split('!2s')[-1]

    try:
        place_details = gmaps.place(place_id=place_id, language='en')
        if place_details and place_details['status'] == 'OK':
            result = place_details['result']
            place_name = result['name']
            address = result['formatted_address']
            return place_name, address
        else:
            print(f"Error al obtener detalles del lugar con URL: {url}")
            return None, None
    except Exception as e:
        print(f"Error al obtener detalles del lugar con URL: {url}")
        return None, None

def main():
    # Cargar el archivo CSV en un DataFrame usando pandas
    df = pd.read_csv("places_reviews.csv")

    # Calcular el promedio de rating por place_id
    ratings_avg = df.groupby("place_id")["rating"].mean()

    # Iterar por cada URL para obtener el nombre del lugar, dirección y ubicación (coordenadas)
    for index, row in df.iterrows():
        url = row["url"]
        place_name, address = get_place_info_from_url(url)

        if place_name and address:
            # Obtener las coordenadas de ubicación
            latitude, longitude = extract_coordinates(address)
            if latitude and longitude:
                # Guardar el nombre del lugar, ubicación (dirección) y promedio de rating en un nuevo DataFrame
                # También guardamos las coordenadas geográficas
                # Podemos contar las filas del grupo para obtener la cantidad de personas que evaluaron el lugar
                num_reviews = df[df["url"] == url].shape[0]
                avg_rating = ratings_avg[row["place_id"]]
                df_result = pd.DataFrame({
                    "place_id": [row["place_id"]],
                    "place_name": [place_name],
                    "address": [address],
                    "latitude": [latitude],
                    "longitude": [longitude],
                    "avg_rating": [avg_rating],
                    "num_reviews": [num_reviews]
                })
                # Guardar los resultados en un archivo llamado "places_info.csv"
                df_result.to_csv("places_info.csv", mode="a", header=False, index=False)
            else:
                print(f"No se pudo obtener coordenadas para el lugar con URL: {url}")
        else:
            print(f"No se pudo obtener información del lugar con URL: {url}")

    
    # Análisis de PLN
    # Vamos a suponer que un sitio es "bueno" si su promedio de rating es mayor o igual a 4.0 y el texto contiene la palabra "bueno"
    # Utilizamos un valor booleano por defecto False para los casos donde no podamos determinar si es "bueno" o no
    df["is_good_site"] = (df["rating"] >= 4.0) & df["text"].apply(lambda x: "bueno" in x.lower() if isinstance(x, str) else False)

    # Contar cuántos sitios son considerados "buenos"
    num_good_sites = df[df["is_good_site"] == True].shape[0]

    print(f"Se han evaluado {num_good_sites} sitios como 'buenos'.")

if __name__ == "__main__":
    main()


