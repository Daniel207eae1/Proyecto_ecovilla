import os
import requests
import time
with open('AWN.env', 'r') as f:
    for line in f:
        nombre, valor = line.strip().split('=')
        os.environ[nombre] = valor

target_url = os.environ["WS_URL"]
headers = {
    "Content-Type": "application/json"
}


