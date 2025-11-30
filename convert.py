import pandas as pd
import json

print("Iniciando conversión de CSV a JSON...")

try:
    # 1. Cargar tu archivo CSV completo
    df = pd.read_csv('Consumo_Agua_Estados_rm.csv')
    
    # 2. Seleccionar solo las columnas que Firebase necesita (para ahorrar espacio)
    #    Filtramos las columnas calculadas como 'color' o 'nivel_consumo'
    columnas_base = [
        'nombre_area', 'estado', 'poblacion', 'lat', 'lon', 
        'tipo_zona', 'consumo_anual_m3'
    ]
    df_firebase = df[columnas_base]

    # 3. Convertir el DataFrame a un diccionario con formato de índice (0, 1, 2...)
    #    Este es el formato que Firebase importa mejor.
    datos_dict = df_firebase.to_dict('index')

    # 4. Crear la estructura final para Firebase
    #    Todo estará bajo un nodo principal llamado "municipios"
    firebase_data = {
        "municipios": datos_dict 
    }

    # 5. Guardar el resultado en un nuevo archivo JSON
    with open('Consumo_Agua_Estados_rm.json', 'w', encoding='utf-8') as f:
        json.dump(firebase_data, f, ensure_ascii=False, indent=2) # indent=2 para un archivo más compacto
    
    print("\n¡ÉXITO! Se ha creado el archivo 'datos_para_firebase.json'.")
    print(f"Total de {len(df_firebase)} municipios procesados.")

except FileNotFoundError:
    print("\nERROR: No se encontró el archivo 'datos_municipios_mexico.csv'.")
    print("Asegúrate de que esté en la misma carpeta que este script.")
except Exception as e:
    print(f"\nOcurrió un error inesperado: {e}")