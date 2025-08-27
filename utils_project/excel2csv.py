import pandas as pd

# Ruta del archivo Excel
archivo_excel = 'C:/Users/Luis Pizarro/PycharmProjects/OPMS/utils_project/exceldemos/propiedades_dv409_pal_demo.xlsx'

# Leer la primera hoja del Excel
df = pd.read_excel(archivo_excel)

ruta_salida = 'C:/Users/Luis Pizarro/PycharmProjects/OPMS/utils_project/csvdemos/'
# Ruta del archivo CSV de salida
archivo_csv = ruta_salida+'propiedades_dv409_pal_demo.csv'

# Guardar como CSV separado por comas
df.to_csv(archivo_csv, index=False, sep=',')

print(f"Archivo convertido exitosamente: {archivo_csv}")
