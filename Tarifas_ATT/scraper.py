import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import os

def scrape_section(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    script_content = None
    for script in soup.find_all("script"):
        if script.text and 'var dataJSONArray = JSON.parse(' in script.text:
            script_content = script.text
            break

    if script_content:
        pattern = re.compile(r'var dataJSONArray = JSON\.parse\(\'(.*?)\'\);', re.DOTALL)
        match = pattern.search(script_content)
        if match:
            json_str = match.group(1).encode().decode('unicode_escape')
            data = json.loads(json_str)
            return data
    else:
        print(f"No se encontró la variable en {url}.")
        return None

def save_to_csv(data, file_path):
    if data:
        columnas = data[0].keys()
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(data)

#para el RawData.csv, pero será desordenado Dx
def save_to_combined_csv(data, file_path):
    if data:
        mode = 'a' if os.path.exists(file_path) else 'w'
        with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            if mode == 'w':
                writer.writeheader()
            writer.writerows(data)
            
# URLs de las secciones
urls = [
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetMovil",
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasServicioMovilPrepago",
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetFijo",
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasTvcable",
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasServicioLocalTelefoniaFija",
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasServicioAccesoPublico",
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/serviciosEmpaquetados",
    "https://tarifas.att.gob.bo/index.php/tarifaspizarra/promociones",
]

# para los CSV de las secciones
file_paths = [
    "serviciosMovil_Internet.csv",
    "serviciosMovil_Prepago.csv",
    "serviciosFijos_Internet.csv",
    "serviciosFIjos_Television.csv",
    "serviciosLocal_TelefoniaFija.csv",
    "servicio_AccesoPublico.csv",
    "serviciosEmpaquetados_ServiciosTelecomunicaciones.csv",
    "promociones_ServiciosTelecomunicaciones.csv"   
]

#para que se guarde en archivos separados
for url, file_path in zip(urls, file_paths):
    data = scrape_section(url)
    if data:
        save_to_csv(data, file_path)
        
#para que se guarde en un solo archivo RawData.cvs
combined_file_path = "RawData.csv"
for file_path in file_paths:
    if os.path.exists(file_path):
        data = []
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        save_to_combined_csv(data, combined_file_path)