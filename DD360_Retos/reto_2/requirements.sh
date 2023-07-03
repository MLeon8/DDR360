#!/bin/bash

# Instalar las dependencias
pip3 install pandas spacy folium beautifulsoup4

# Descargar el modelo de spaCy en español
python3 -m spacy download es_core_news_sm

#Generar los archivos
python3 Generar_archivos.py
