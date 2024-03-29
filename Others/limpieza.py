import pandas as pd
import re

expresiones_precio = [
    (r'\d{1,3}(?:\.\d{3})*\s*\$us', 'USD'),
    (r'\$us\.\s\d{1,3}(?:\.\d{3})*', 'USD'),
    (r'\$us\s\d{1,3}(?:\.\d{3})*', 'USD'),
    (r'\d{1,3}(?:\.\d{3})+\.\s\$us\.', 'USD'),
    (r'\d{1,3}(?:\.\d{3})*\s*BS\.', 'BOB'),
    (r'Bs\.\s\d{1,3}(?:\.\d{3})*', 'BOB'),
    (r'\d+(?:[.,]\d{3})*\s*Bs', 'BOB'),
    (r'Bs\s\d{1,}(?:[.,]\d{3})*', 'BOB'),
    (r'\b\d{1,2}(?:[.,]\d{3}){1,2}\s*\$', 'USD'),
    (r'\$\d+(?:[.,]\d+)?\b', 'USD'),
    (r'\d{1,3}(?:[.,]\d{3})*\s*\$', 'USD'),
    (r'\$(\d{1,3}(?:,\d{3})+)', 'USD'),
    (r'\$(\d{1,3}(?:[.,]\d{3})+)\b', 'USD'),
]

expresiones_tamaño = [
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?mts\b', ''),
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?metros\b', ''),
    (r'\b\d+\s?mts2\b', ''),
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?mts2\b', ''),
    (r'\b\d+\s?m2\b', ''),
    (r'\b\d{1,3}(?:[.,]\d{3})*\s?m2\b', ''),
]

expresion_dormitorios = r'\b(\d+)\s*(dormitorio[s]?|cuarto[s]?|habitacion[es]?)\b'

meses = {
    "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04",
    "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08",
    "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
}

def convertir_a_dolares(valor, moneda):
    if moneda == 'BOB':
        return round(float(valor.replace(',', '').replace('.', '')) / 7)
    return float(valor.replace(',', '').replace('.', ''))

def aplicar_expresion_regex(df, columna, expresiones, columna_final, convertir_moneda=False, eliminar_final_2=False):
    def extraer_y_convertir_valor(texto):
        for patron, moneda in expresiones:
            matches = re.findall(patron, texto, re.IGNORECASE)
            if matches:
                valor = str(matches[0])
                valor_numerico = re.sub(r'[^\d.,]', '', valor)
                if eliminar_final_2 and valor_numerico.endswith('2'):
                    valor_numerico = valor_numerico[:-1]
                valor_sin_puntos_comas = valor_numerico.replace(',', '').replace('.', '')
                if valor_sin_puntos_comas != valor_numerico:
                    pass
                if convertir_moneda and moneda == 'BOB':
                    return convertir_a_dolares(valor_sin_puntos_comas, moneda)
                return valor_sin_puntos_comas
        return None
    
    df_temp = df.copy()
    df_temp[columna_final + '_temp'] = df_temp[columna].apply(extraer_y_convertir_valor)
    df_temp[columna_final] = df_temp[columna_final + '_temp'].combine_first(df_temp[columna_final])
    df_temp = df_temp.drop(columns=[columna_final + '_temp'])
    return df_temp

def limpiar_tamaño(valor):
    if pd.isna(valor):
        return valor
    valor_str = str(valor)
    if valor_str.endswith('2'):
        return valor_str[:-1]
    return valor_str

def convertir_fecha_manualmente(texto_fecha):
    fecha_sin_prefijo = texto_fecha.replace('Publicado: ', '')
    partes = fecha_sin_prefijo.split(' ')
    dia, mes_texto, año = partes[0], partes[1], partes[2]
    mes = meses[mes_texto]
    fecha_formateada = f"{año}-{mes}-{dia.zfill(2)}"
    return fecha_formateada

df_original = pd.read_csv('anuncios_inmuebles.csv')

df_original['precio'] = None
df_original['tamaño'] = None
df_original['dormitorios'] = None

df_original = aplicar_expresion_regex(df_original, 'descripcion', expresiones_precio, 'precio', convertir_moneda=True)
df_original = aplicar_expresion_regex(df_original, 'titulo', expresiones_precio, 'precio', convertir_moneda=True)
df_original = aplicar_expresion_regex(df_original, 'descripcion', expresiones_tamaño, 'tamaño')
df_original = aplicar_expresion_regex(df_original, 'titulo', expresiones_tamaño, 'tamaño')
df_original = aplicar_expresion_regex(df_original, 'descripcion', [(expresion_dormitorios, '')], 'dormitorios')
df_original = aplicar_expresion_regex(df_original, 'titulo', [(expresion_dormitorios, '')], 'dormitorios')

df_data = df_original.dropna(subset=['precio', 'tamaño', 'dormitorios'], how='all')
df_trash = df_original[df_original[['precio', 'tamaño', 'dormitorios']].isnull().all(axis=1)]

df_data = df_data[['fecha', 'departamento', 'tipo', 'inmueble', 'precio', 'tamaño', 'dormitorios', 'titulo', 'descripcion']]
df_data['tamaño'] = df_data['tamaño'].apply(limpiar_tamaño)
df_data['fecha'] = df_data['fecha'].apply(convertir_fecha_manualmente)

df_data.to_csv('Data.csv', index=False)
df_trash.to_csv('Data_trash.csv', index=False)
