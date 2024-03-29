import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

file_path = os.path.join(current_directory, 'RawData.csv')

url = "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetMovil"

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
        tarifas = json.loads(json_str)
        columnas = tarifas[0].keys()
        # Crear CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(tarifas)
else:
    print("No se encontró la variable.")
