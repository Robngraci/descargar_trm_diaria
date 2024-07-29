import requests
import pandas as pd
from datetime import datetime
import os

# URL del API de TRM (Asegúrate de usar la URL correcta para el proveedor del servicio de TRM)
url = "https://www.datos.gov.co/resource/32sa-8pi3.json"

# Realizar la solicitud GET al API
response = requests.get(url)
data = response.json()

# Obtener la TRM y la fecha
trm = data[0]['valor']
fecha = data[0]['vigenciadesde']

# Convertir la fecha a formato datetime
fecha_datetime = datetime.strptime(fecha, '%Y-%m-%dT%H:%M:%S.%f')

# Crear un DataFrame con los datos
df = pd.DataFrame({'Fecha': [fecha_datetime], 'TRM': [trm]})

# Definir el nombre del archivo CSV
archivo_csv = 'trm_diaria.csv'

# Verificar si el archivo ya existe
if os.path.exists(archivo_csv):
    # Si el archivo existe, cargar los datos existentes
    df_existente = pd.read_csv(archivo_csv, parse_dates=['Fecha'])
    # Concatenar los nuevos datos con los existentes
    df_total = pd.concat([df_existente, df], ignore_index=True)
    # Eliminar duplicados en caso de que el script se ejecute más de una vez al día
    df_total = df_total.drop_duplicates(subset=['Fecha'])
    # Guardar los datos actualizados en el archivo CSV
    df_total.to_csv(archivo_csv, index=False)
else:
    # Si el archivo no existe, guardar el nuevo DataFrame en el archivo CSV
    df.to_csv(archivo_csv, index=False)

print("TRM guardada exitosamente.")
