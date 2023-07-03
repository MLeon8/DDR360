import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import mstats

# Cargar el archivo CSV
data = pd.read_csv('reto_precios.csv')

# Combinar las columnas "lon" y "lat" en una sola columna de coordenadas
data['coordinates'] = data.apply(lambda row: (row['lon'], row['lat']), axis=1)

# Seleccionar solo columnas numéricas para la matriz de correlación
columnas_numericas = data.select_dtypes(include=[int, float]).columns

# Realizar winsorization en cada columna numérica
data_winsorized = data.copy()
for col in columnas_numericas:
    data_winsorized[col] = mstats.winsorize(data[col], limits=[0.05, 0.05])

# Matriz de correlación sin Winsorization
correlation_cols = data[columnas_numericas].drop(['lon', 'lat'], axis=1)
correlation_matrix = correlation_cols.corr()

# Ordenar los factores por su correlación con "price_square_meter" (sin Winsorization)
correlation_ordered = correlation_matrix['price_square_meter'].sort_values(ascending=False)

# Matriz de correlación con Winsorization
correlation_cols_winsorized = data_winsorized[columnas_numericas].drop(['lon', 'lat'], axis=1)
correlation_matrix_winsorized = correlation_cols_winsorized.corr()

# Ordenar los factores por su correlación con "price_square_meter" (con Winsorization)
correlation_ordered_winsorized = correlation_matrix_winsorized['price_square_meter'].sort_values(ascending=False)


# Crear subplots para mostrar las comparativas con y sin Winsorization
fig, axes = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [1, 1]})

# Plot del mapa de calor (heatmap) con resaltado de características importantes (sin Winsorization)
sns.heatmap(correlation_matrix.loc[correlation_ordered.index, correlation_ordered.index], annot=True, cmap='coolwarm', fmt=".2f", ax=axes[0])
axes[0].set_title('Matriz de Correlación (Sin Winsorization)')
axes[0].set_xticks(ticks=range(len(correlation_ordered)))
axes[0].set_yticks(ticks=range(len(correlation_ordered)))
axes[0].set_xticklabels([col for col in correlation_ordered.index], rotation=45)
axes[0].set_yticklabels([col for col in correlation_ordered.index], rotation=0)

# Plot del mapa de calor (heatmap) con resaltado de características importantes (con Winsorization)
sns.heatmap(correlation_matrix_winsorized.loc[correlation_ordered_winsorized.index, correlation_ordered_winsorized.index], annot=True, cmap='coolwarm', fmt=".2f", ax=axes[1])
axes[1].set_title('Matriz de Correlación (Con Winsorization)')
axes[1].set_xticks(ticks=range(len(correlation_ordered_winsorized)))
axes[1].set_yticks(ticks=range(len(correlation_ordered_winsorized)))
axes[1].set_xticklabels([col for col in correlation_ordered_winsorized.index], rotation=45)
axes[1].set_yticklabels([col for col in correlation_ordered_winsorized.index], rotation=0)

# Eliminar el espacio vacío entre los subplots
plt.tight_layout()

# Crear subplots para mostrar las comparativas con y sin Winsorization
fig, axes = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [1, 1]})

# Histograma del precio por metro cuadrado (sin Winsorization)
sns.histplot(data['price_square_meter'], kde=True, ax=axes[0])
axes[0].set_title('Distribución del Precio por Metro Cuadrado (Sin Winsorization)')
axes[0].set_xlabel('Precio por Metro Cuadrado')
axes[0].set_ylabel('Frecuencia')

# Histograma del precio por metro cuadrado (con Winsorization)
sns.histplot(data_winsorized['price_square_meter'], kde=True, ax=axes[1])
axes[1].set_title('Distribución del Precio por Metro Cuadrado (Con Winsorization)')
axes[1].set_xlabel('Precio por Metro Cuadrado')
axes[1].set_ylabel('Frecuencia')

# Eliminar el espacio vacío entre los subplots
plt.tight_layout()

# Crear subplots para mostrar las comparativas con y sin Winsorization
fig, axes = plt.subplots(1, 2, figsize=(14, 8), gridspec_kw={'width_ratios': [1, 1]})

# Scatterplot de precio por metro cuadrado vs. metros cuadrados (sin Winsorization)
sns.scatterplot(data=data, x='m2', y='price_square_meter', ax=axes[0])
axes[0].set_title('Precio por Metro Cuadrado vs. Metros Cuadrados (Sin Winsorization)')
axes[0].set_xlabel('Metros Cuadrados')
axes[0].set_ylabel('Precio por Metro Cuadrado')

# Scatterplot de precio por metro cuadrado vs. metros cuadrados (con Winsorization)
sns.scatterplot(data=data_winsorized, x='m2', y='price_square_meter', ax=axes[1])
axes[1].set_title('Precio por Metro Cuadrado vs. Metros Cuadrados (Con Winsorization)')
axes[1].set_xlabel('Metros Cuadrados')
axes[1].set_ylabel('Precio por Metro Cuadrado')

# Eliminar el espacio vacío entre los subplots
plt.tight_layout()


# Guardar los plots como imágenes PNG con nombres distintos
plt.savefig('mapas_de_calor.png')
plt.savefig('histogramas.png')
plt.savefig('scatterplots.png')

# Mostrar los plots
plt.show()
