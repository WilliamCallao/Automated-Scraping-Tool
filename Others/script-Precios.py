import pandas as pd
import re

def cargar_y_preparar_df(original_csv):
    df = pd.read_csv(original_csv)
    df['precio'] = None
    df['tamaño'] = None 
    df.to_csv('restante.csv', index=False)

def aplicar_expresion_regex_y_actualizar(archivo_fuente, expresion_regex, columna_precio='precio'):
    df = pd.read_csv(archivo_fuente)
    df_procesado = pd.read_csv('procesado.csv')

    def extraer_precio(texto):
        matches = re.findall(expresion_regex, texto, re.IGNORECASE)
        return matches[0] if matches else None

    df['precio_temp'] = df['descripcion'].apply(extraer_precio)
    df['precio_titulo'] = df['titulo'].apply(extraer_precio)
    df[columna_precio] = df['precio_temp'].combine_first(df['precio_titulo'])

    df_con_precio = df.dropna(subset=[columna_precio])
    df_sin_precio = df[df[columna_precio].isnull()]

    df_sin_precio.drop(columns=['precio_temp', 'precio_titulo'], inplace=True)
    df_sin_precio.to_csv('restante.csv', index=False)

    df_procesado = pd.concat([df_procesado, df_con_precio[['fecha', 'departamento', 'tipo', 'inmueble', columna_precio, 'tamaño', 'titulo', 'descripcion']]], ignore_index=True)
    df_procesado.to_csv('procesado.csv', index=False)

pd.DataFrame(columns=['fecha', 'departamento', 'tipo', 'inmueble', 'precio', 'tamaño', 'titulo', 'descripcion']).to_csv('procesado.csv', index=False)

cargar_y_preparar_df('anuncios_inmuebles.csv')

expresiones = [
    (r'\d{1,3}(?:\.\d{3})*\s*\$us', '280.000 $us'),
    (r'\$us\.\s\d{1,3}(?:\.\d{3})*', '$us. 185.000'),
    (r'\$us\s\d{1,3}(?:\.\d{3})*', '$us 5200'),       
    (r'\d{1,3}(?:\.\d{3})+\.\s\$us\.', '$us. 185.000'),
    (r'\d{1,3}(?:\.\d{3})*\s*BS\.', '1.700 BS.'),
    (r'Bs\.\s\d{1,3}(?:\.\d{3})*', 'Bs. 2.000'),
    (r'\d+(?:[.,]\d{3})*\s*Bs', '2000 Bs'),
    (r'Bs\s\d{1,}(?:[.,]\d{3})*', 'Bs 1200'),
    (r'\b\d{1,2}(?:[.,]\d{3}){1,2}\s*\$', '15.000 $'),
    (r'\$\d+(?:[.,]\d+)?\b', '$400'),
    (r'\d{1,3}(?:[.,]\d{3})*\s*\$', '105.000 $'),
    (r'\$(\d{1,3}(?:,\d{3})+)', '$50,000'),
    (r'\$(\d{1,3}(?:[.,]\d{3})+)\b', '$120,000.')
]

for expresion, descripcion in expresiones:
    aplicar_expresion_regex_y_actualizar('restante.csv', expresion)
     