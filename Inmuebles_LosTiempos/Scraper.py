import requests
from bs4 import BeautifulSoup
import csv
import os

def cargar_anuncios_previos():
    if os.path.exists('RawData.csv'):
        with open('RawData.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    return []

def guardar_anuncios(anuncios):
    with open('RawData.csv', 'a', newline='', encoding='utf-8') as file:
        campos = ['titulo', 'fecha', 'descripcion', 'departamento', 'tipo', 'inmueble']
        writer = csv.DictWriter(file, fieldnames=campos)
        
        for anuncio in anuncios:
            writer.writerow(anuncio)

def anuncio_unico(anuncio, anuncios):
    for anuncio_existente in anuncios:
        if anuncio_existente['titulo'] == anuncio['titulo'] and anuncio_existente['fecha'] == anuncio['fecha']:
            return False
    return True

def extraer_anuncios(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            anuncios = []
            items_anuncio = soup.find_all('div', class_='views-row')
            for item in items_anuncio:
                titulo = item.find('div', class_='title')
                fecha_publicado = item.find('div', class_='publish-date')
                descripcion = item.find('div', class_='body')
                detalles = item.find('div', class_='description').text.strip().split(' - ')
                if titulo and descripcion:
                    anuncio = {
                        'titulo': titulo.text.strip(),
                        'fecha': fecha_publicado.text.strip() if fecha_publicado else 'Fecha no disponible',
                        'descripcion': descripcion.text.strip(),
                        'departamento': detalles[0] if len(detalles) > 0 else '',
                        'tipo': detalles[1] if len(detalles) > 1 else '',
                        'inmueble': detalles[2] if len(detalles) > 2 else ''
                    }
                    anuncios.append(anuncio)
            return anuncios
        else:
            print(f"Error al acceder a la página: {url} - Estado HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"Excepción al intentar acceder a {url}: {e}")
        return []

url_base = 'https://clasificados.lostiempos.com/inmuebles'
parametros = '?sort_by=created&sort_order=DESC&page='

todos_anuncios = []

pagina = 0
limite_paginas = 5

anuncios_previos = cargar_anuncios_previos()
anuncios_nuevos = []

while pagina < limite_paginas:
    url = f"{url_base}{parametros}{pagina}"
    anuncios_pagina = extraer_anuncios(url)
    if not anuncios_pagina:
        print(f"No se encontraron anuncios en la página {pagina} o hubo un error al acceder a ella.")
        pagina += 1
        continue
    for anuncio in anuncios_pagina:
        if anuncio_unico(anuncio, anuncios_previos):
            anuncios_nuevos.append(anuncio)
    pagina += 1

anuncios_actualizados = anuncios_previos + anuncios_nuevos
guardar_anuncios(anuncios_nuevos)

print(f"Se han agregado {len(anuncios_nuevos)} nuevos registros.")
print(f"Total de anuncios guardados: {len(anuncios_actualizados)}")
