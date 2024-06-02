import pandas as pd
import folium
from folium import plugins
import branca
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse



app = FastAPI()

@app.get("/{ruta}/{mes}/{dia}", response_class=HTMLResponse)
async def root(ruta:str,mes:str,dia:str):
    meses = {
    "ENERO": "01",
    "FEBRERO": "02",
    "MARZO": "03",
    "ABRIL": "04",
    "MAYO": "05",
    "JUNIO": "06",
    "JULIO": "07",
    "AGOSTO": "08",
    "SEPTIEMBRE": "09",
    "OCTUBRE": "10",
    "NOVIEMBRE": "11",
    "DICIEMBRE": "12"
    }


    datos = pd.read_excel(f'./{mes.upper()}/2024-{meses[mes.upper()]}-{dia}.xlsx')
    fecha='2024-04-02'
    datos[datos['date'].isin([fecha])]
    nombres_columnas = datos.columns

    # Convertir el objeto Index a una lista (opcional)
    lista_eliminables = list(nombres_columnas)
    print(lista_eliminables)

    for i in ['latitude','longitude','route_name']:
        lista_eliminables.remove(i)

    datos.drop(lista_eliminables, axis=1, inplace=True)

    datos.head()
    rutas = datos.groupby('route_name')
    for route_name, grupo in rutas:
        if route_name==ruta.capitalize():
            # Crear un mapa centrado en un punto específico de la ruta
            mapa = folium.Map(location=[grupo['latitude'].mean(), grupo['longitude'].mean()], zoom_start=14.4)
            # Preparar los datos para el mapa de calor
            heatmap_data = list(zip(grupo['latitude'], grupo['longitude']))
            # Agregar el mapa de calor al mapa
            heatmap = plugins.HeatMap(heatmap_data)
            heatmap.add_to(mapa)
            
    return mapa.get_root().render()

