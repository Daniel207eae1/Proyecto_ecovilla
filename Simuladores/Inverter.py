import os
import requests
import time
import random

# Leer el archivo de variables de entorno
with open('AWN.env', 'r') as f:
    for line in f:
        nombre, valor = line.strip().split('=')
        os.environ[nombre] = valor


target_url = os.environ["INV_FIWARE_ENDPOINT"]
headers = {
    "Content-Type": "application/json"
}

impexp = random.random()
frec = random.uniform(59.7, 60.2)

rangos = {
    # Battery Charge/Discharge (Active and Power)
    "batterychargeactive": (0, 500),  # kW
    "batterychargeactiveday": (0, 2500),  # kWh
    "batterychargeactivemonth": (0, 10000),  # kWh
    "batterycurrent": (-50, 50),  # A
    "batterydischargeactive": (0, 1000),  # kW
    "batterydischargeactiveday": (0, 5000),  # kWh
    "batterydischargeactivemonth": (0, 20000),  # kWh
    "batterypower": (-1000, 1000),  # kW
    "batteryvoltage": (200, 250),  # V

    # Charger and Inverter States
    "chargedccurrent": (0, 20),  # A
    "chargedcpower": (0, 5000),  # kW
    "chargedcpowerpercentage": (0, 100),  # %
    "chargerenabled": (0, 1),  # Boolean (0: False, 1: True)
    "chargerstatus": (0,1),  # String
    "devicestate": (0,1),  # String
    "forcedsell": (0, 1),  # Boolean (0: False, 1: True)
    "inverterenabled": (0, 1),  # Boolean (0: False, 1: True)
    "inverterstatus": (0,1),  # String
    "sellenabled": (0, 1),  # Boolean (0: False, 1: True)

    # Grid AC Data
    "gridaccurrent": (-50, 50),  # A
    "gridacfrequency": (49.5, 50.5),  # Hz
    "gridacinputcurrent": (-20, 20),  # A
    "gridacinputpowerapparent": (0, 10000),  # kVA
    "gridacinputvoltage": (200, 250),  # V
    "gridacl1current": (-20, 20),  # A
    "gridacl1voltage": (200, 250),  # V
    "gridacpower": (-10000, 10000),  # kW
    "gridacvoltage": (200, 250),  # V

    # Grid Input/Output (Active, Energy)
    "gridinputactive": (0, 5000),  # kW
    "gridinputactiveday": (0, 20000),  # kWh
    "gridinputactivemonth": (0, 80000),  # kWh
    "gridinputenergy": (0, 100000),  # kWh
    "gridinputenergyday": (0, 50000),  # kWh
    "gridinputenergymonth": (0, 200000),  # kWh
    "gridoutputactive": (-5000, 5000),  # kW
    "gridoutputactiveday": (-20000, 20000),  # kWh
    "gridoutputactivemonth": (-80000, 80000),  # kWh
    "gridoutputcurrent": (-50, 50),  # A
    "gridoutputenergy": (0, 100000),  # kWh
    "gridoutputenergyday": (0, 50000),  # kWh
    "gridoutputenergymonth": (0, 200000),  # kWh
    "gridoutputfrequency": (49.5, 50.5),  # Hz
    "gridoutputpower": (-10000, 10000),  # kW
    "gridoutputpowerapparent": (0, 20000),  # kVA
    "gridoutputvoltage": (200, 250),  # V

    # Inverter DC Data
    "inverterdccurrent": (-50, 50),  # A
    "inverterdcpower": (-1000, 1000),  # kW

    # Load AC Data
    "loadaccurrent": (-50, 50),  # A
    "loadacfrequency": (49.5, 50.5),  # Hz
    "loadacl1current": (-20, 20),  # A
    "loadacl1voltage": (200, 250),  # V
    "loadacpower": (-10000, 10000),  # kW
    "loadacpowerapparent": (0, 20000),  # kVA
    "loadacvoltage": (200, 250),  # V

    # Load Output (Active, Energy)
    "loadoutputactive": (0, 5000),  # kW
    "loadoutputactiveday": (0, 20000),  # kWh
    "loadoutputactivemonth": (0, 80000),  # kWh
    "loadoutputenergy": (0, 100000),  # kWh
    "loadoutputenergyday": (0, 50000),  # kWh
    "loadoutputenergymonth": (0, 200000),  # kWh
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
        
    
    #print(patch_payload)
    response = requests.patch(target_url, headers=headers, json=datos)
    if response.status_code == 204:
        print("Attributes updated successfully")
    else:
        print("Error updating attributes:", response.status_code)
        print(response.content)
      
    time.sleep(8)