import pandas as pd
import re

def cargar_y_preparar_df(original_csv):
    df = pd.read_csv(original_csv)
    df['precio'] = None 
    df['dormitorios'] = None 
    df.to_csv('room_restante.csv', index=False)

def aplicar_expresion_regex_y_actualizar(archivo_fuente, expresion_regex, columna_dormitorios='dormitorios'):
    df = pd.read_csv(archivo_fuente)
    df_procesado = pd.read_csv('room_procesado.csv')

    def extraer_dormitorios(texto):
        matches = re.findall(expresion_regex, texto, re.IGNORECASE)
        if matches:
        
            return matches[0][0] 
        else:
            return None

    df['dormitorios_temp'] = df['descripcion'].apply(extraer_dormitorios)
    df['dormitorios_titulo'] = df['titulo'].apply(extraer_dormitorios)
    df[columna_dormitorios] = df['dormitorios_temp'].combine_first(df['dormitorios_titulo'])

    df_con_dormitorios = df.dropna(subset=[columna_dormitorios])
    df_sin_dormitorios = df[df[columna_dormitorios].isnull()]

    df_sin_dormitorios.drop(columns=['dormitorios_temp', 'dormitorios_titulo'], inplace=True)
    df_sin_dormitorios.to_csv('room_restante.csv', index=False)

    df_procesado = pd.concat([df_procesado, df_con_dormitorios[['fecha', 'departamento', 'tipo', 'inmueble', 'precio', columna_dormitorios, 'titulo', 'descripcion']]], ignore_index=True)
    df_procesado.to_csv('room_procesado.csv', index=False)

pd.DataFrame(columns=['fecha', 'departamento', 'tipo', 'inmueble', 'precio', 'dormitorios', 'titulo', 'descripcion']).to_csv('room_procesado.csv', index=False)

cargar_y_preparar_df('anuncios_inmuebles.csv')

expresion_dormitorios = r'\b(\d+)\s*(dormitorio[s]?|cuarto[s]?|suite[s]?|habitacion[es]?)\b'

aplicar_expresion_regex_y_actualizar('room_restante.csv', expresion_dormitorios, 'dormitorios')
