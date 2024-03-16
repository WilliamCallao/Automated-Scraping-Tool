import requests
from bs4 import BeautifulSoup
import pickle
import os

def cargar_anuncios_previos():
    if os.path.exists('anuncios_inmuebles.pickle'):
        with open('anuncios_inmuebles.pickle', 'rb') as file:
            return pickle.load(file)
    return []

def guardar_anuncios(anuncios):
    with open('anuncios_inmuebles.pickle', 'wb') as file:
        pickle.dump(anuncios, file)

def anuncio_unico(anuncio, anuncios):
    for anuncio_existente in anuncios:
        if anuncio_existente['titulo'] == anuncio['titulo'] and anuncio_existente['fecha'] == anuncio['fecha']:
            return False
    return True
def extraer_anuncios(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    
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

url_base = 'https://clasificados.lostiempos.com/inmuebles'
parametros = '?sort_by=created&sort_order=DESC&page='

todos_anuncios = []

pagina = 0
limite_paginas = 10

anuncios_previos = cargar_anuncios_previos()
anuncios_nuevos = []

while pagina < limite_paginas:
    url = f"{url_base}{parametros}{pagina}"
    anuncios_pagina = extraer_anuncios(url)
    if not anuncios_pagina:
        break
    for anuncio in anuncios_pagina:
        if anuncio_unico(anuncio, anuncios_previos):
            anuncios_nuevos.append(anuncio)
    pagina += 1

anuncios_actualizados = anuncios_previos + anuncios_nuevos
guardar_anuncios(anuncios_actualizados)

print(f"Se han agregado {len(anuncios_nuevos)} nuevos registros.")

print(f"Total de anuncios guardados: {len(anuncios_actualizados)}")