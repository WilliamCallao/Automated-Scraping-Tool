import pickle

def cargar_anuncios_desde_pickle(archivo):
    try:
        with open(archivo, 'rb') as file:
            anuncios = pickle.load(file)
        return anuncios
    except FileNotFoundError:
        print("Archivo no encontrado.")
        return []

def imprimir_anuncios(anuncios):
    if not anuncios:
        print("No hay anuncios para mostrar.")
        return

    for anuncio in anuncios:
        print("titulo:", anuncio['titulo'])
        print("fecha:", anuncio['fecha'])
        print("descripcion:", anuncio['descripcion'])
        print("departamento:", anuncio['departamento'])
        print("tipo:", anuncio['tipo'])
        print("inmueble:", anuncio['inmueble'])
        print("-" * 10)
        
archivo_pickle = 'anuncios_inmuebles.pickle'
anuncios = cargar_anuncios_desde_pickle(archivo_pickle)
imprimir_anuncios(anuncios)
print(f"Total de registros procesados: {len(anuncios)}")