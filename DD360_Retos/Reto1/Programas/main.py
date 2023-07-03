import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from branca.colormap import linear
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
import numpy as np
from Reto1_CostBenef import load_data, calculate_quality_price_ratio, generate_heatmap, generate_interactive_map, get_property_with_best_cost_benefit

# Cargamos los datos y realizamos el análisis
data = load_data('reto_precios.csv')
calculate_quality_price_ratio(data)
generate_heatmap(data)
generate_interactive_map(data)
