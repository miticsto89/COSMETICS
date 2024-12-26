import json
import requests
from datetime import datetime

# Tu clave API de fortniteapi.io
API_KEY = '107a1219-96c01308-f4569489-336df56e'

# URL de la API de fortniteapi.io
API_URL = 'https://fortniteapi.io/v2/shop?lang=es'

# Headers para la solicitud
headers = {
    'Authorization': API_KEY
}

# Realizar la llamada a la API
response = requests.get(API_URL, headers=headers)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
else:
    print(f'Error en la solicitud: {response.status_code}')
    data = {"shop": []}

# Función para convertir la fecha de fin en un objeto datetime
def get_end_date(item):
    return datetime.fromisoformat(item["offerDates"]["out"].replace('Z', '+00:00'))

# Función para limpiar la fecha de fin
def clean_end_date(end_date):
    return end_date.replace('T00:00:00.000Z', '').replace('T23:59:59.999Z', '')

# Ordenar los datos por la fecha de fin
sorted_data = sorted(data["shop"], key=get_end_date)

# Agrupar los datos por secciones
grouped_data = {}
for item in sorted_data:
    section_name = item["section"]["name"] if "section" in item and item["section"] else "Sin Sección"
    if section_name not in grouped_data:
        grouped_data[section_name] = []
    grouped_data[section_name].append(item)

# Orden de los tipos principales
type_order = [
    "bundle", "outfit", "backpack", "pickaxe",
    "emote", "glider", "wrap", "sparks_song",
    "shoes", "vehicle_booster", "sparks_bass",
    "sparks_guitar", "sparks_keyboard", "sparks_microphone", "building_set", "sparks_drum"
]

# Función para calcular el precio en USD
def calculate_price(finalPrice):
    return ((finalPrice * 0.46) / 100) - 0.25

# Imprimir los datos agrupados por secciones en el formato solicitado y organizados por tipo
for section, items in grouped_data.items():
    if items:
        # Usar la fecha de fin de la oferta del primer item de la sección
        offer_end_date = clean_end_date(items[0].get("offerDates", {}).get("out", "N/A"))
        print(f'Sección: {section}')
        print(f'Disponible hasta el: {offer_end_date}')
    
    # Ordenar los items dentro de la sección según el tipo principal
    items_sorted_by_type = sorted(items, key=lambda x: type_order.index(x["mainType"]) if "mainType" in x else len(type_order))
    
    for item in items_sorted_by_type:
        displayName = item.get("displayName", "N/A")
        full_background = item.get("displayAssets", [{}])[0].get("full_background", "N/A")
        finalPrice = item.get("price", {}).get("finalPrice", 0)
        price_usd = calculate_price(finalPrice)

        print(f'Item = {displayName}')
        print(f'Imagen = {full_background}')
        print(f'Precio(USD) = ${price_usd:.2f}')
        print()  # Añadir una línea en blanco después de cada item
    print('----------------------------------')
