import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import numpy as np

# Cargar el archivo CSV
data = pd.read_csv('reto_precios.csv')

# Seleccionar solo columnas numéricas para aplicar PCA
columnas_numericas = data.select_dtypes(include=[int, float]).columns
data_numericas = data[columnas_numericas]

# Imputar los valores faltantes con la media de cada columna
imputer = SimpleImputer(strategy='mean')
data_imputed = imputer.fit_transform(data_numericas)

# Encontrar columnas con valores iguales a cero
columnas_ceros = data_imputed.min(axis=0) == 0

# Aplicar logaritmo solo a las columnas que no tienen valores iguales a cero
data_imputed_log = data_imputed.copy()
data_imputed_log[:, columnas_ceros] = np.log1p(data_imputed_log[:, columnas_ceros])

# Normalizar los datos antes de aplicar PCA
scaler = StandardScaler()
data_normalized = scaler.fit_transform(data_imputed_log)

# Aplicar PCA
pca = PCA()
data_pca = pca.fit_transform(data_normalized)

# Obtener la cantidad de varianza explicada por cada componente principal
varianza_explicada = pca.explained_variance_ratio_

# Análisis de componentes principales
componentes_principales = pd.DataFrame(pca.components_, columns=columnas_numericas)
componentes_principales_abs = componentes_principales.abs()

# Obtener las características más influyentes en el precio por metro cuadrado y ordenar de mayor a menor
caracteristicas_influyentes = componentes_principales_abs.loc[0].sort_values(ascending=False)

print("Características más influyentes en el precio por metro cuadrado:")
print(caracteristicas_influyentes)
