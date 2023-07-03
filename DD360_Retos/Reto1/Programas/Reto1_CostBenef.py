import pandas as pd
import numpy as np
import folium
from branca.colormap import linear
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

def calculate_quality_price_ratio(data):
    data['quality_price_ratio'] = data['final_price'] / data['m2']
    return data

def generate_heatmap(data):
    relevant_columns = ['m2', 'final_price', 'price_square_meter','bathrooms','num_bedrooms','parking_lots','price_mod']
    numerical_data = data[relevant_columns]
    correlation_matrix = numerical_data.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Mapa de calor - Correlación entre variables')
    plt.savefig('heatmap_correlation.png')
    plt.close()

def generate_interactive_map(data):
    map_center = [data['lat'].mean(), data['lon'].mean()]
    m = folium.Map(location=map_center, zoom_start=14)

    color_scheme = {
        (70000, np.inf): 'red',    # Propiedades más caras en rojo
        (60000, 70000): 'orange',  # Propiedades medio altas en naranja
        (50000, 60000): 'yellow',  # Propiedades medio bajas en amarillo
        (0, 50000): 'green'        # Propiedades más baratas en verde
    }

    for index, row in data.iterrows():
        price_per_sqm = row['price_square_meter']
        color = get_color(price_per_sqm, color_scheme)
        folium.Marker([row['lat'], row['lon']], popup=f"Precio por metro cuadrado: {price_per_sqm:.2f}", icon=folium.Icon(color=color)).add_to(m)

    # Obtener la mejor propiedad con su explicación
    best_property = get_property_with_best_cost_benefit(data)
    explanation_text = f"La propiedad con mejor costo-beneficio es:\n"
    explanation_text += f"Nombre: {best_property['main_name']}\n"
    explanation_text += f"Ubicación: {best_property['location']}\n"
    explanation_text += f"Precio: {best_property['final_price']} {best_property['price_currency']}\n"
    explanation_text += f"Área construida: {best_property['m2']} m²\n"
    explanation_text += f"Calidad-Precio Ratio: {best_property['quality_price_ratio']:.2f}\n\n"
    explanation_text += f"Descripción:\n{best_property['description']}"

    # Guardar la explicación en el archivo
    with open("explicacion_mejor_propiedad.txt", "w", encoding="utf-8") as file:
        file.write(explanation_text)

    folium.Marker([best_property['lat'], best_property['lon']], popup="Mejor costo-beneficio", icon=folium.Icon(color='blue', icon='star')).add_to(m)

    m.save('mapa_interactivo.html')

def get_property_with_best_cost_benefit(data):
    min_max_scaler = preprocessing.MinMaxScaler()
    data_scaled = min_max_scaler.fit_transform(data[['m2', 'final_price']])

    X = pd.DataFrame(data_scaled, columns=['m2', 'final_price'])
    y = data['price_square_meter']

    model = LinearRegression()
    rfe = RFE(model, n_features_to_select=1)
    fit = rfe.fit(X, y)

    ranking = fit.ranking_
    index = np.where(ranking == 1)[0][0]
    property_with_best_cost_benefit = data.iloc[index]

    return property_with_best_cost_benefit

def get_color(price_per_sqm, color_scheme):
    for price_range, color in color_scheme.items():
        if price_range[0] <= price_per_sqm <= price_range[1]:
            return color
    return 'blue'  # Default to blue if no range matches

def find_best_properties(data, num_properties=5):
    data = data.copy()
    data['quality_price_ratio'] = data['final_price'] / data['m2']
    best_properties = data.nlargest(num_properties, 'quality_price_ratio')
    return best_properties
