#EV2_SDN_NicolasHitscherich_ByronObreque_ValentinSerrano

import requests
import urllib.parse

# Define la clave de API y las URLs de geocodificación y ruta
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "9fa00cb8-c1ef-4850-af7d-de11b44cb0d1"  # Reemplaza con tu clave de API de Graphhopper

# Función para obtener coordenadas de una ciudad
def get_coordinates(city, key):
    url = geocode_url + urllib.parse.urlencode({"q": city, "limit": "1", "key": key})
    response = requests.get(url)
    data = response.json()
    
    if 'hits' not in data or len(data['hits']) == 0:
        print(f"No se encontraron coordenadas para {city}")
        return None
    
    location = data['hits'][0]['point']
    return location['lat'], location['lng']

#EV2_SDN_NicolasHitscherich_ByronObreque_ValentinSerrano
# Función para obtener información de la ruta
def get_route_info(api_key, origin_coords, destination_coords):
    params = {
        'point': [f"{origin_coords[0]},{origin_coords[1]}", f"{destination_coords[0]},{destination_coords[1]}"],
        'vehicle': 'car',
        'locale': 'es',
        'instructions': 'true',
        'calc_points': 'true',
        'key': api_key
    }
    
    response = requests.get(route_url, params=params)
    data = response.json()
    
    if 'paths' not in data:
        print("Error al obtener la ruta. Por favor, verifica las ciudades ingresadas.")
        return None
    
    path = data['paths'][0]
    distance_km = path['distance'] / 1000.0
    time_ms = path['time']
    
    return distance_km, time_ms, path['instructions']

#EV2_SDN_NicolasHitscherich_ByronObreque_ValentinSerrano
# Función principal
def main():
    api_key = key  # Usamos la clave de API definida anteriormente
    
    while True:
        origin = input("Ciudad de Origen: ")
        if origin.lower() in ['s', 'salir']:
            print("Saliendo del programa.")
            break
        
        destination = input("Ciudad de Destino: ")
        if destination.lower() in ['s', 'salir']:
            print("Saliendo del programa.")
            break
        
        origin_coords = get_coordinates(origin, api_key)
        destination_coords = get_coordinates(destination, api_key)
        
        if not origin_coords or not destination_coords:
            continue

        # Obtén información de la ruta entre las ciudades proporcionadas por el usuario
        distance_km, time_ms, instructions = get_route_info(api_key, origin_coords, destination_coords)
        print(f"\nDistancia entre {origin} y {destination}: {distance_km:.2f} km")
        
#EV2_SDN_NicolasHitscherich_ByronObreque_ValentinSerrano
        # Mostrar la duración del viaje en horas, minutos y segundos
        hours = int(time_ms // (1000 * 60 * 60))
        minutes = int((time_ms % (1000 * 60 * 60)) // (1000 * 60))
        seconds = int((time_ms % (1000 * 60)) // 1000)
        
        print(f"Duración del viaje: {hours} horas, {minutes} minutos, {seconds} segundos")

#EV2_SDN_NicolasHitscherich_ByronObreque_ValentinSerrano
        # Imprimir la narrativa del viaje
        print("\nNarrativa del viaje:")
        for instruction in instructions:
            print(f"{instruction['distance']:.2f} m: {instruction['text']}")
        
if __name__ == "__main__":
    main()

