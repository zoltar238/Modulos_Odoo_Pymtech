import pandas as pd

from scripts.productos_a_excell.eliminador_duplicados import columnas_codigos

# Cargar los datos
dataframe_productos = pd.read_excel("Productos.xlsx")
dataframe_codigos = pd.read_excel("Codigos_Filtrados_sin_duplicados.xlsx")

columnas_codigos_nombres = dataframe_codigos['descripcion_art'].astype(str).str.strip().str.lower()
columnas_codigos_codigos = dataframe_codigos['codigo_barra']

columnas_productos = dataframe_productos['name'].astype(str).str.strip().str.lower()
identificador = "__export__.product_barcode_multi_10_a"
contador = 1

for indice, producto in enumerate(columnas_codigos_nombres):
    indice_coincidencia = columnas_productos.indexOf(producto)
    if indice_coincidencia != -1:
        dataframe_productos.at[indice_coincidencia, 'barcode_ids'] = columnas_codigos_codigos[indice]
        dataframe_productos.at[indice_coincidencia, 'barcode_ids/name'] = columnas_codigos_codigos[indice]
        dataframe_productos.at[indice_coincidencia, 'barcode_ids/id'] = columnas_codigos_codigos[indice]
        dataframe_productos.at[indice_coincidencia, 'barcode_ids/name'] = identificador + str(contador)
        dataframe_productos.at[indice_coincidencia, 'barcode_ids/product_id'] = identificador + str(contador)
        contador += 1
