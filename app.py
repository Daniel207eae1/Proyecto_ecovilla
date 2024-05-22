import os
import requests
import time

# Leer el archivo de variables de entorno
with open('AWN.env', 'r') as f:
    for line in f:
        nombre, valor = line.strip().split('=')
        os.environ[nombre] = valor

target_url = os.environ["AWN_FIWARE_ENDPOINT"]
headers = {
    "Content-Type": "application/json"
}

while True:
    from ambient_api.ambientapi import AmbientAPI
    weather = AmbientAPI()
    devices = weather.get_devices()
    devices[1].get_data()
    devices[1].last_data
    api_response_data = devices[1].last_data
    print(api_response_data['dateutc'])
    pm10_value = 0
    pm25_value = 0
    humidity_value = api_response_data['humidity']
    pressure_value = api_response_data['baromrelin']
    solar_radiation_value = api_response_data['solarradiation']
    temperature_value = api_response_data['tempf'] 
    wind_dir_value = api_response_data['winddir']
    wind_speed_value = api_response_data['windspeedmph']
    patch_payload = {
        "humidity": {
            "type": "Number",
            "value": humidity_value,
            "metadata": {}
        },
        "pm_10": {
            "type": "Number",
            "value": pm10_value,
            "metadata": {}
        },
        "pm_2_5": {
            "type": "Number",
            "value": pm25_value,
            "metadata": {}
        },
        "pressure": {
            "type": "Number",
            "value": pressure_value,
            "metadata": {}
        },
        "solar_radiation": {
            "type": "Number",
            "value": solar_radiation_value,
            "metadata": {}
        },
        "temperature": {
            "type": "Number",
            "value": temperature_value,
            "metadata": {}
        },
        "wind_dir": {
            "type": "Number",
            "value": wind_dir_value,
            "metadata": {}
        },
        "wind_speed": {
            "type": "Number",
            "value": wind_speed_value,
            "metadata": {}
        }
    }
    response = requests.patch(target_url, headers=headers, json=patch_payload)
    if response.status_code == 204:
        print("Attributes updated successfully")
    else:
        print("Error updating attributes:", response.status_code)
      
    time.sleep(5)
