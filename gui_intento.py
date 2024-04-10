import requests
from bs4 import BeautifulSoup
from pathlib import Path
from tkinter import Tk, PhotoImage, Label, StringVar, ttk, Entry, Button, Toplevel, Checkbutton, IntVar, Spinbox
from tkcalendar import DateEntry 
import re
import json
import csv
import os

# Ruta de la imagen
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame1"
image_path = ASSETS_PATH / "pantalla_10.png"
continuar_image_path = ASSETS_PATH / "continuar.png"
pantalla_20_image_path = ASSETS_PATH / "pantalla_20.png"
back_image_path = ASSETS_PATH / "back.png"

def scrape_section(url, filtros):
    """
    Extrae y filtra datos del sitio web basado en los parámetros proporcionados.
    
    Args:
    - url (str): La URL del sitio web a raspar.
    - filtros (dict): Un diccionario que contiene los filtros para departamento, operador, precio mínimo,
      precio máximo y velocidad.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    script_content = None
    for script in soup.find_all("script"):
        if 'var dataJSONArray = JSON.parse(' in script.text:
            script_content = script.text
            break

    if not script_content:
        print("No se encontró la variable en {}".format(url))
        return None

    pattern = re.compile(r'var dataJSONArray = JSON\.parse\(\'(.*?)\'\);', re.DOTALL)
    match = pattern.search(script_content)
    if not match:
        return None

    json_str = match.group(1).encode().decode('unicode_escape')
    data = json.loads(json_str)

    # Filtrado de datos
    filtered_data = []
    for row in data:
        if filtros.get("departamento") and filtros.get("departamento") != "Todos" and row.get("DEPARTAMENTO") != filtros["departamento"]:
            continue
        if filtros.get("operador") and filtros.get("operador") != "Todos" and row.get("NOMBRE_COMERCIAL") != filtros["operador"]:
            continue
        if filtros.get("precio_minimo") and float(row.get("PRECIO_MENSUAL", 0)) < filtros["precio_minimo"]:
            continue
        if filtros.get("precio_maximo") and float(row.get("PRECIO_MENSUAL", 0)) > filtros["precio_maximo"]:
            continue
        if filtros.get("velocidad") and filtros.get("velocidad") != "Todos" and float(row.get("ANCHO_BANDA_BAJADA", 0)) != filtros["velocidad"]:
            continue

        filtered_data.append(row)

    return filtered_data

def read_existing_data(file_path):
    """
    Lee los datos existentes de un archivo CSV, si existe.
    """
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_data.append(row)
    return existing_data

def is_unique_row(new_row, existing_rows):
    """
    Verifica si una fila es única comparándola con filas existentes.
    """
    for existing_row in existing_rows:
        if new_row['ID_TARIFA'] == existing_row['ID_TARIFA'] and new_row['DEPARTAMENTO'] == existing_row['DEPARTAMENTO']:
            return False
    return True

def save_to_csv(new_data, file_path):
    """
    Guarda los datos nuevos en un archivo CSV, asegurándose de que no haya duplicados.
    """
    existing_data = read_existing_data(file_path)
    new_rows = []

    for row in new_data:
        if is_unique_row(row, existing_data):
            new_rows.append(row)

    if new_rows:
        mode = 'a' if os.path.exists(file_path) else 'w'
        with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=new_rows[0].keys())
            if mode == 'w':
                writer.writeheader()
            writer.writerows(new_rows)

        print(f"Se agregaron {len(new_rows)} registros nuevos al archivo {file_path}.")
    else:
        print("No se encontraron registros nuevos para agregar.")

def initiate_scraping():
    filtros = {
        "departamento": selected_departamento.get(),
        "operador": selected_operador.get(),
        "precio_minimo": int(entry_precio_min.get()),
        "precio_maximo": int(entry_precio_max.get()),
        "velocidad": selected_velocidad.get() if selected_velocidad.get() != "TODOS" else None
    }
    
    # Realizar el scraping y filtrado
    url = "https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetFijo"
    datos_filtrados = scrape_section(url, filtros)

    # Guardar los datos filtrados en CSV
    if datos_filtrados:
        save_to_csv(datos_filtrados, "datos_filtrados.csv")
    else:
        print("No se encontraron datos con los filtros aplicados.")
        
def center_elements(window):
    window.update_idletasks()  # Actualizar las dimensiones de la ventana
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    image_width = image.width()
    image_height = image.height()
    x_position_image = (window_width - image_width) // 2
    y_position_image = (window_height - image_height) // 2
    image_label.place(x=x_position_image, y=y_position_image)

    filtrarrecoleccion_label.place(x=730, y=325)  
    departamento_label.place(x=760, y=380)
    operador_label.place(x=1100, y=380)
    precio_label.place(x=760, y=490)
    velocidad_label.place(x=1100, y=490)
    combobox_departamento.place(x=760, y=420)  
    combobox_operador.place(x=1100, y=420)  
    label_precio_min.place(x=760, y=530)  
    entry_precio_min.place(x=830, y=530)  
    label_precio_max.place(x=760, y=570)  
    entry_precio_max.place(x=830, y=570) 
    combobox_velocidad.place(x=1100, y=530)  
    boton_continuar.place(x=900, y=630) 

def open_new_window():
    window.withdraw()  # Ocultar la ventana actual
    new_window = Toplevel()
    new_window.title("Nueva Ventana")
    new_window.geometry(window.geometry())
    center_elements(new_window)

    global pantalla_20_image, back_image  
    pantalla_20_image = PhotoImage(file=pantalla_20_image_path)
    pantalla_20_label = Label(new_window, image=pantalla_20_image, bg="#FFFFFF")
    pantalla_20_label.place(x=0, y=0)

    back_image = PhotoImage(file=back_image_path)
    back_button = Button(new_window, image=back_image, bg="#FFFFFF", bd=0, command=lambda: close_new_window(new_window))
    back_button.place(x=10, y=10)

    # Label ventana nueva
    tipoextra_label = Label(new_window, text="TIPO DE EXTRACCIÓN", font=("Arial", 20, "bold"), bg="#DDF4FF")
    extrauto_label = Label(new_window, text="Automática", font=("Arial", 15, "bold"), bg="#DDF4FF")
    extraprogra_label = Label(new_window, text="Programada", font=("Arial", 15, "bold"), bg="#DDF4FF")
    tipoextra_label.place(x=730, y=325)
    extrauto_label.place(x=760, y=380)
    extraprogra_label.place(x=760, y=460)  
   
    automatica_var = IntVar()
    automatica_checkbox = Checkbutton(new_window, variable=automatica_var, bg="#DDF4FF")
    automatica_checkbox.place(x=900, y=380)

    programada_var = IntVar()
    programada_checkbox = Checkbutton(new_window, variable=programada_var, bg="#DDF4FF")
    programada_checkbox.place(x=900, y=460)
    
    hora_label = Label(new_window, text="Hora:", font=("Arial", 13), bg="#DDF4FF")
    hora_label.place(x=780, y=500)
    
    options_horas = ["00:00 am", "01:00 am", "02:00 am", "03:00 am", "04:00 am", "05:00 am", "06:00 am", "07:00 am", "08:00 am",
                 "09:00 am", "10:00 am", "11:00 am", "12:00 pm", "01:00 pm", "02:00 pm", "03:00 pm", "04:00 pm",
                 "05:00 pm", "06:00 pm", "07:00 pm", "08:00 pm", "09:00 pm", "10:00 pm", "11:00 pm"]

    selected_hora = StringVar()
    combobox_hora = ttk.Combobox(new_window, textvariable=selected_hora, values=options_horas, state="readonly", font=("Arial", 13))
    combobox_hora.current(0)  

  
    combobox_hora.place(x=850, y=500)

    
    fecha_label = Label(new_window, text="Fecha:", font=("Arial", 13), bg="#DDF4FF")
    fecha_label.place(x=780, y=550)
    fecha_entry = DateEntry(new_window, font=("Arial", 13), background='darkblue', foreground='white', borderwidth=2)
    fecha_entry.place(x=850, y=550)
    
    # Botón Extraer
    extraer_button = Button(new_window, text="Extraer", font=("Arial", 13), command=initiate_scraping)
    extraer_button.place(x=850, y=600)

    
def close_new_window(new_window):
    new_window.destroy()  
    window.deiconify() 

# Crear la ventana
window = Tk()
window.title("Ventana centrada")
window.configure(bg="#FFFFFF")


window.bind("<Configure>", lambda event: center_elements(window))

image = PhotoImage(file=image_path)

image_label = Label(window, image=image, bg="#FFFFFF")
image_label.pack()

filtrarrecoleccion_label = Label(window, text="FILTRAR", font=("Arial", 20, "bold"), bg="#DDF4FF")
departamento_label = Label(window, text="Departamento", font=("Arial", 15, "bold"), bg="#DDF4FF")
operador_label = Label(window, text="Operador", font=("Arial", 15, "bold"), bg="#DDF4FF")
velocidad_label = Label(window, text="Velocidad", font=("Arial", 15, "bold"), bg="#DDF4FF")
precio_label = Label(window, text="Precio mensual", font=("Arial", 15, "bold"), bg="#DDF4FF")

options_departamento = ["Todos", "Cochabamba", "La Paz", "Chuquisaca", "Oruro", "Potosí", "Tarija", "Santa Cruz", "Beni", "Pando"]
selected_departamento = StringVar()
combobox_departamento = ttk.Combobox(window, textvariable=selected_departamento, values=options_departamento, state="readonly", font=("Arial", 13))
combobox_departamento.current(0)  

options_operador = ["Todos", "ENTEL S.A.", "NUEVATEL PCS", "TELECEL S.A.", "AGENCIA BOLIVIANA ESPACIAL", "COTAS R.L.", "COTES LTDA"]
selected_operador = StringVar()
combobox_operador = ttk.Combobox(window, textvariable=selected_operador, values=options_operador, state="readonly", font=("Arial", 13))
combobox_operador.current(0)  

label_precio_min = Label(window, text="Min:", font=("Arial", 13), bg="#DDF4FF")

entry_precio_min = Spinbox(window, from_=0, to=9999, font=("Arial", 13), width=6)
entry_precio_min.delete(0, "end")  
entry_precio_min.insert(0, "0") 

label_precio_max = Label(window, text="Max:", font=("Arial", 13), bg="#DDF4FF")

entry_precio_max = Spinbox(window, from_=0, to=9999, font=("Arial", 13), width=6)
entry_precio_max.delete(0, "end")  
entry_precio_max.insert(0, "9999") 

options_velocidad = ["Todos","100 Mbps", "200 Mbps", "300 Mbps", "400 Mbps", "500 Mbps"]
selected_velocidad = StringVar()
combobox_velocidad = ttk.Combobox(window, textvariable=selected_velocidad, values=options_velocidad, state="readonly", font=("Arial", 13))
combobox_velocidad.current(0)  

# Botón conti
continuar_image = PhotoImage(file=continuar_image_path)
boton_continuar = Button(window, image=continuar_image, bg="#FFFFFF", bd=0, command=open_new_window) 

# Aplicar estilos al Combobox
style = ttk.Style()
style.theme_use('clam')  
style.configure('TCombobox', background='#FFFFFF', foreground='#000000', bordercolor='#000000', selectbackground='#DDF4FF', selectforeground='#000000')

window.mainloop()
