import pandas as pd
import numpy as np

# Cargar el archivo CSV
data = pd.read_csv('reto_precios.csv')

# Obtener solo columnas numéricas
columnas_numericas = data.select_dtypes(include=[int, float]).columns
data_numericas = data[columnas_numericas]

# Imputar los valores faltantes con la media de cada columna
data_imputed = data_numericas.fillna(data_numericas.mean())

# Calcular la matriz de correlación con el precio por metro cuadrado
correlation_matrix = data_imputed.corr()
precio_metro_cuadrado_corr = correlation_matrix['price_square_meter'].abs().sort_values(ascending=False)

print("Características más influyentes en el precio por metro cuadrado (por correlación):")
print(precio_metro_cuadrado_corr)
