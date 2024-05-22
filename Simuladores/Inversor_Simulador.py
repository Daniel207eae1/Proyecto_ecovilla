import os
import requests
import time
import random

# Leer el archivo de variables de entorno
with open('AWN.env', 'r') as f:
    for line in f:
        nombre, valor = line.strip().split('=')
        os.environ[nombre] = valor


#target_url = os.environ["AWN_FIWARE_ENDPOINT"]
target_url = "http://localhost:1026/v2/entities/SM_EVI01/attrs"
headers = {
    "Content-Type": "application/json"
}

impexp = random.random()
frec = random.uniform(59.7, 60.2)

rangos = {
    "activeenergyexport": (0, 10000),  # kWh
    "activeenergyexportday": (0, 5000),  # kWh
    "activeenergyimport": (0, 10000),  # kWh
    "activeenergyimportday": (0, 5000),  # kWh
    "activepower": (0, 5000),  # kW
    "activepower1": (0, 2500),  # kW
    "activepower2": (0, 2500),  # kW
    "activepower3": (0, 2500),  # kW
    "frecuency": (59.8, 60.2),  # Hz
    "harmonicsi1": (0, 100),  # %
    "harmonicsi2": (0, 100),  # %
    "harmonicsi3": (0, 100),  # %
    "harmonicsv1": (0, 100),  # %
    "harmonicsv2": (0, 100),  # %
    "harmonicsv3": (0, 100),  # %
    "i1": (0, 100),  # A
    "i2": (0, 100),  # A
    "i3": (0, 100),  # A
    "i1angle": (0, 360),  # grados
    "i2angle": (0, 360),  # grados
    "i3angle": (0, 360),  # grados
    "in": (0, 0.1),  # A
    "powerfactor1": (0.9, 1),  # %
    "powerfactor2": (0.9, 1),  # %
    "powerfactor3": (0.9, 1),  # %
    "reactiveenergyexport": (-5000, 5000),  # kVArh
    "reactiveenergyexportday": (-2500, 2500),  # kVArh
    "reactiveenergyimport": (-5000, 5000),  # kVArh
    "reactiveenergyimportday": (-2500, 2500),  # kVArh
    "reactivepower": (-2500, 2500),  # kvar
    "reactivepower1": (-1250, 1250),  # kvar
    "reactivepower2": (-1250, 1250),  # kvar
    "reactivepower3": (-1250, 1250),  # kvar
    "relativethdcurrent": (0, 100),  # %
    "relativethdpower": (0, 100),  # %
    "relativethdvoltage": (0, 100),  # %
    "relativethdfactor": (0.9, 1),  # %
    "totalpowerfactor": (0.9, 1),  # %
    "v1": (0, 220),  # V
    "v1angle": (0, 360),  # grados
    "v1_ps": (0, 1),  # V
    "v2": (0, 220),  # V
    "v2angle": (0, 360),  # grados
    "v2_ps": (0, 1),  # V
    "v3": (0, 220),  # V
    "v3angle": (0, 360),  # grados
    "v3_ps": (0, 1)  # V
}

while True:
    # Generar números aleatorios para cada variable
    datos = {}
    for variable, rango in rangos.items():
        valor_aleatorio = random.uniform(*rango)
        valor_redondeado = round(valor_aleatorio, 2)
        datos[variable] = {
            "type": "Number",
            "value": valor_redondeado
        }
        
    print(datos)
    
    #print(patch_payload)
    response = requests.patch(target_url, headers=headers, json=datos)
    if response.status_code == 204:
        print("Attributes updated successfully")
    else:
        print("Error updating attributes:", response.status_code)
        print(response.content)
      
    time.sleep(8)