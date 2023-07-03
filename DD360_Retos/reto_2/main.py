import pandas as pd
import spacy
import folium

# Función para preprocesar el texto de las reseñas
def preprocess_text(text, nlp):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(lemmas)

# Función para asignar color a las reseñas según su calificación
def asignar_color_calificacion(calificacion):
    if calificacion >= 5:
        return 'blue'  # Las mejores reseñas en azul
    elif calificacion >= 4:
        return 'green'  # Lugares buenos en verde
    elif calificacion >= 3:
        return 'yellow'  # Lugares no malos ni buenos en amarillo
    else:
        return 'red'  # Lugares no recomendables en rojo



# Leer y procesar los archivos CSV "detalles_lugares.csv" y "reseñas_lugares.csv"
detalles_df = pd.read_csv('detalles_lugares.csv')
reseñas_df = pd.read_csv('reseñas_lugares.csv')

# Identificar si más de una persona ha visitado el mismo lugar y juntar esa información
lugares_evaluados_df = reseñas_df.drop_duplicates(subset=['identificador_lugar'])

# Crear una referencia cruzada para identificar lugares en "reseñas_lugares.csv"
lugares_evaluados_df = pd.merge(lugares_evaluados_df, detalles_df, left_on='identificador_lugar', right_on='identificador', how='left', suffixes=('_reseña', '_detalles'))

# Llenar los valores NaN en las columnas de calificación_reseña con ceros para evitar problemas con la clasificación de colores
lugares_evaluados_df['calificacion_reseña'] = lugares_evaluados_df['calificacion_reseña'].fillna(0)

# Cargar el modelo de spaCy en español
nlp = spacy.load('es_core_news_sm')

# Aplicar PLN para analizar las reseñas y clasificar los lugares
lugares_evaluados_df['texto_procesado'] = lugares_evaluados_df['texto'].fillna('').apply(lambda x: preprocess_text(x, nlp))
lugares_evaluados_df['calificacion'] = lugares_evaluados_df['calificacion_reseña'].combine_first(lugares_evaluados_df['calificacion_detalles'])
lugares_evaluados_df['color'] = lugares_evaluados_df['calificacion'].apply(asignar_color_calificacion)

# Crear un mapa con Folium para identificar los lugares y sus códigos de colores
mapa = folium.Map(location=[lugares_evaluados_df['latitud'].mean(), lugares_evaluados_df['longitud'].mean()], zoom_start=12)

# Agregar marcadores para los lugares en el mapa

for index, lugar in lugares_evaluados_df.iterrows():
    # Verificar si la latitud y longitud no son NaN
    if not pd.isna(lugar['latitud']) and not pd.isna(lugar['longitud']):
        popup_text = f"<b>{lugar['nombre']}</b><br>Calificación: {lugar['calificacion']}<br>{lugar['texto_procesado']}"
        folium.Marker(
            location=[lugar['latitud'], lugar['longitud']],
            popup=popup_text,
            tooltip=lugar['nombre'],
            icon=folium.Icon(color=lugar['color'])  # Usa el color definido para cada lugar
        ).add_to(mapa)


# Guardar el mapa interactivo en un archivo HTML
mapa.save('mapa_interactivo_lugares_evaluados.html')

# Guardar los datos de los lugares evaluados en un archivo CSV
lugares_evaluados_df.to_csv('lugares_evaluados.csv', index=False)


