import pandas as pd

# Traducción de los encabezados a español
traduccion_details = {
    'place_id': 'identificador',
    'name': 'nombre',
    'business_status': 'estado_negocio',
    'latitude': 'latitud',
    'longitude': 'longitud',
    'user_ratings_total': 'total_calificaciones_usuarios',
    'rating': 'calificacion',
    'website': 'sitio_web',
    'price_level': 'nivel_precio',
    'photos': 'fotos',
    'sunday_open': 'domingo_apertura',
    'sunday_close': 'domingo_cierre',
    'monday_open': 'lunes_apertura',
    'monday_close': 'lunes_cierre',
    'tuesday_open': 'martes_apertura',
    'tuesday_close': 'martes_cierre',
    'wednesday_open': 'miercoles_apertura',
    'wednesday_close': 'miercoles_cierre',
    'thursday_open': 'jueves_apertura',
    'thursday_close': 'jueves_cierre',
    'friday_open': 'viernes_apertura',
    'friday_close': 'viernes_cierre',
    'saturday_open': 'sabado_apertura',
    'saturday_close': 'sabado_cierre',
    'tipo_lugar': 'tipo_lugar'
}

traduccion_reviews = {
    'url': 'url',
    'reviewer': 'revisor',
    'reviewer_avatar': 'avatar_revisor',
    'datetime': 'fecha_hora',
    'rating': 'calificacion',
    'text': 'texto',
    'language': 'idioma',
    'id': 'identificador',
    'place_id': 'identificador_lugar'
}

# Leer los archivos CSV originales
places_details_df = pd.read_csv('places_details.csv')
places_reviews_df = pd.read_csv('places_reviews.csv')

# Generar nuevos archivos CSV con los encabezados en español y sin caracteres especiales
places_details_df.rename(columns=traduccion_details, inplace=True)
places_reviews_df.rename(columns=traduccion_reviews, inplace=True)

# Eliminar caracteres especiales y espacios en blanco de los nombres de las columnas
places_details_df.columns = places_details_df.columns.str.replace('[^a-zA-Z0-9]', '_')
places_reviews_df.columns = places_reviews_df.columns.str.replace('[^a-zA-Z0-9]', '_')

# Guardar los nuevos archivos CSV
places_details_df.to_csv('detalles_lugares.csv', index=False)
places_reviews_df.to_csv('reseñas_lugares.csv', index=False)
