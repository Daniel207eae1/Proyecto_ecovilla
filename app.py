import os
import requests
import pprint
import time
import datetime


# Leer el archivo de variables de entorno
with open('AWN.env', 'r') as f:
    for line in f:
        # Dividir la línea en nombre y valor de la variable
        nombre, valor = line.strip().split('=')

        print(nombre)
        print(valor)
        # Establecer la variable de entorno
        os.environ[nombre] = valor


##ENVIROMENT VARIABLES

##  Weather Station
AMBIENT_ENDPOINT = os.environ["AMBIENT_ENDPOINT"]
applicationKey = os.environ["applicationKey"]
apiKey = os.environ["apiKey"]
#target_url = os.environ["WS_URL"]

target_url = "http://localhost:1026/v2/entities/WS_UPB_EVI/attrs"
headers = {
    "Content-Type": "application/json"
}

from ambient_api.ambientapi import AmbientAPI

#weather = AmbientAPI(log_level='CONSOLE')
weather = AmbientAPI()
devices = weather.get_devices()

for device in devices:
    # Wait two seconds between requests so we don't get a 429 response.
    # https://ambientweather.docs.apiary.io/#introduction/rate-limiting
    # This probably won't happen much in real world situations.
    time.sleep(2)
    print('Device')
    print((str(device)))

    print('Last Data')
    pprint.pprint(device.last_data)

    #print('Get Data')
    #pprint.pprint(device.get_data())
 
while True:
    print("Start")
    devices[1].get_data()
    device = devices[1].api_device.get('lastData', {})
    devices[1].refresh_last_data()
    devices[1].last_data
    print(device)
    api_response_data = devices[1].last_data
    pm10_value = 0
    pm25_value = 0
    #pm10_value = api_response_data['pm_10']
    #pm25_value = api_response_data['pm_2_5']
    humidity_value = api_response_data['humidity']
    pressure_value = api_response_data['baromrelin']
    solar_radiation_value = api_response_data['solarradiation']
    temperature_value = api_response_data['tempf']  # Assuming 'tempf' is the temperature value in the API response
    wind_dir_value = api_response_data['winddir']
    wind_speed_value = api_response_data['windspeedmph']

    print("mid")
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
