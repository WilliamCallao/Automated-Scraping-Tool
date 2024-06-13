from tkinter import Tk, Canvas, Button, PhotoImage, ttk, IntVar, Label, messagebox
from pathlib import Path
import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import os
import threading
import schedule
import time

# Asumiendo que tienes la ruta correcta para ASSETS_PATH
ASSETS_PATH = Path(__file__).parent / "assets" / "frame1"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Funciones de scraping y guardado
def scrape_section(url, departamento=None):
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
            if departamento and departamento != "Todos":
                data = [row for row in data if row.get("DEPARTAMENTO") == departamento]
            return data
    else:
        print("No se encontró la variable en {}".format(url))
        return None

def read_existing_data(file_path):
    existing_data = []
    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_data.append(row)
    return existing_data

def is_unique_row(new_row, existing_rows):
    for existing_row in existing_rows:
        if new_row['ID_TARIFA'] == existing_row['ID_TARIFA'] and new_row['DEPARTAMENTO'] == existing_row['DEPARTAMENTO']:
            return False
    return True

def save_to_csv(new_data, file_path):
    existing_data = read_existing_data(file_path)
    new_rows = []

    for row in new_data:
        if is_unique_row(row, existing_data):
            new_rows.append(row)

    num_new_rows = len(new_rows)

    if new_rows:
        mode = 'a' if os.path.exists(file_path) else 'w'
        with open(file_path, mode=mode, newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=new_rows[0].keys())
            if mode == 'w':
                writer.writeheader()
            writer.writerows(new_rows)

    if num_new_rows > 0:
        messagebox.showinfo("Información", f"Se agregaron {num_new_rows} registros nuevos al archivo {file_path}.")
    else:
        messagebox.showwarning("Información", "No se encontraron registros nuevos para agregar.")

def initiate_scraping():
    departamento = combo_departamentos.get()
    data = scrape_section("https://tarifas.att.gob.bo/index.php/tarifaspizarra/tarifasInternetFijo", departamento)
    if data:
        save_to_csv(data, "serviciosFijos_Internet.csv")

def schedule_scraping():
    selected_hour = combo_horas.get()
    schedule.clear()
    if execution_var.get() == 1:
        schedule.every().day.at(selected_hour).do(initiate_scraping_thread)

def initiate_scraping_thread():
    scraping_thread = threading.Thread(target=initiate_scraping)
    scraping_thread.start()

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
        
# Inicialización de la ventana
window = Tk()
window.geometry("700x500")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=500,
    width=700,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Botones existentes
image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
canvas.create_image(
    350.0,  # Coordenada X central
    250.0,  # Coordenada Y central
    image=image_1
)

# Botón para extraer los datos
button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(image=button_image_2, borderwidth=0, highlightthickness=0, command=initiate_scraping, relief="flat")
button_2.place(x=350.0, y=379.0, width=249.0, height=38.0)

# Sección de Ejecución Automática
label_auto_exec = Label(window, text="Ejecución Automática", bg="#F0F0F0")
label_auto_exec.place(x=352, y=160)

execution_var = IntVar()
check_auto_execution = ttk.Checkbutton(window, text="Activar", variable=execution_var, onvalue=1, offvalue=0)
check_auto_execution.place(x=352, y=180)

# Selector de Hora
horas = [f"{h:02d}:00" for h in range(24)]
combo_horas = ttk.Combobox(window, values=horas, state="readonly")
combo_horas.place(x=352, y=210, width=249)
combo_horas.set("Seleccione una Hora")

# Sección de Extracción
label_extraction = Label(window, text="Extracción", bg="#F0F0F0")
label_extraction.place(x=352, y=260)

# Selector de Departamentos
departamentos = ['Todos', 'Chuquisaca', 'La Paz', 'Cochabamba', 'Oruro', 'Potosí', 'Tarija', 'Santa Cruz', 'Beni', 'Pando']
combo_departamentos = ttk.Combobox(window, values=departamentos, state="readonly")
combo_departamentos.place(x=352, y=290, width=249)
combo_departamentos.set("Todos")

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

window.resizable(False, False)
window.mainloop()
