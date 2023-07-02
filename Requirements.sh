
#Requeriments.sh para reto 1
#created by Moises Leon 

#!/bin/bash

# Instala la última versión de pip
sudo apt update
sudo apt install python3-pip
pip install --upgrade pip



# Instala las bibliotecas necesarias
pip3 install scikit-learn
pip3 install pandas
pip3 install numpy
pip3 install seaborn 
pip3 install numpy 
pip3 install folium
pip3 install os
pip3 install ipywidgets

#Metodo de uso:
#chmod +x requirements.sh
#./requirements.sh



#Si desea ocupar jupyter como entorno de desarrollo
#Verificar versiones e istalar python:
	#python --version
	#sudo apt update
	#sudo apt install python3

#Instalar pip
	#sudo apt install python3-pip

#Instalar Jupyter:
	#sudo -H pip3 install jupyter

#Ejecutar jupyter:
	#jupyter notebook
