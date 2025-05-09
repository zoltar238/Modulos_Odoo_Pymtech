import pandas as pd

# Cargar los datos
dataframe_productos = pd.read_excel("Productos.xlsx")
dataframe_codigos = pd.read_excel("Codigos.xlsx")

# Extraer las columnas y normalizarlas
# Convertimos a string y eliminamos espacios en blanco al inicio y final
columnas_productos = dataframe_productos['name'].astype(str).str.strip().str.lower()
columnas_codigos = dataframe_codigos['descripcion_art'].astype(str).str.strip().str.lower()

# Crear una lista para almacenar índices a eliminar
indices_a_eliminar = []
contador = 0

# Convertir columnas_productos a una lista para búsqueda más eficiente
lista_productos = columnas_productos.tolist()

# Imprimir información para diagnóstico
print(f"Total productos en lista de productos: {len(columnas_productos)}")
print(f"Total productos en lista de códigos: {len(columnas_codigos)}")

# Realizar la comparación
for index, columna in enumerate(columnas_codigos):
    if columna not in lista_productos:
        indices_a_eliminar.append(index)
        contador += 1

print(f"Total de productos no encontrados: {contador}")

# Eliminar las filas que no están en la lista de productos
if indices_a_eliminar:
    dataframe_codigos_filtrado = dataframe_codigos.drop(indices_a_eliminar)
    print(f"Se eliminaron {len(indices_a_eliminar)} productos")
else:
    dataframe_codigos_filtrado = dataframe_codigos
    print("No se eliminó ningún producto")

# Guardar el resultado
dataframe_codigos_filtrado.to_excel("Codigos_filtrados.xlsx", index=False)

