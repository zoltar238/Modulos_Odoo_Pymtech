import pandas as pd

# Cargar los datos
dataframe_codigos = pd.read_excel("Codigos_filtrados.xlsx")

columnas_codigos = dataframe_codigos['descripcion_art'].astype(str).str.strip().str.lower()

for index, columna in enumerate(columnas_codigos):
    if index != 0:
        if columna == columnas_codigos[index -1]:
            dataframe_codigos.at[index, 'descripcion_art'] = ''
            dataframe_codigos.at[index, 'articulo'] = ''


dataframe_codigos.to_excel("Codigos_filtrados_sin_duplicados.xlsx")

