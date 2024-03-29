import pandas as pd
import re

def cargar_y_preparar_df(original_csv):
    df = pd.read_csv(original_csv)
    df['precio'] = None
    df['tamaño'] = None 
    df.to_csv('sz_restante.csv', index=False)

def aplicar_expresion_regex_y_actualizar(archivo_fuente, expresion_regex, columna_tamaño='tamaño'):
    df = pd.read_csv(archivo_fuente)
    df_procesado = pd.read_csv('sz_procesado.csv')

    def extraer_tamaño(texto):
        matches = re.findall(expresion_regex, texto, re.IGNORECASE)
        return matches[0] if matches else None

    df['tamaño_temp'] = df['descripcion'].apply(extraer_tamaño)
    df['tamaño_titulo'] = df['titulo'].apply(extraer_tamaño)
    df[columna_tamaño] = df['tamaño_temp'].combine_first(df['tamaño_titulo'])

    df_con_tamaño = df.dropna(subset=[columna_tamaño])
    df_sin_tamaño = df[df[columna_tamaño].isnull()]

    df_sin_tamaño.drop(columns=['tamaño_temp', 'tamaño_titulo'], inplace=True)
    df_sin_tamaño.to_csv('sz_restante.csv', index=False)

    df_procesado = pd.concat([df_procesado, df_con_tamaño[['fecha', 'departamento', 'tipo', 'inmueble', 'precio', columna_tamaño, 'titulo', 'descripcion']]], ignore_index=True)
    df_procesado.to_csv('sz_procesado.csv', index=False)

pd.DataFrame(columns=['fecha', 'departamento', 'tipo', 'inmueble', 'precio', 'tamaño', 'titulo', 'descripcion']).to_csv('sz_procesado.csv', index=False)

cargar_y_preparar_df('anuncios_inmuebles.csv')

expresiones_tamaño = [
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?mts\b', 'metros'),
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?metros\b', 'metros'),
    (r'\b\d+\s?mts2\b', 'metros cuadrados'),
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?mts2\b', 'metros cuadrados'),
    (r'\b\d+\s?m2\b', 'metros cuadrados'),
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?m2\b', 'metros cuadrados'),
]

for expresion, descripcion in expresiones_tamaño:
    aplicar_expresion_regex_y_actualizar('sz_restante.csv', expresion, 'tamaño')
