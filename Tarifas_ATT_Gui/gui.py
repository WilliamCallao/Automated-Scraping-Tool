from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
# rutas
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.geometry("700x559")
window.configure(bg = "#FFFFFF")
window.resizable(False, False)


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 559,
    width = 700,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# Diccionario para seguir el estado de los botones
button_states = {i: False for i in range(3, 11)}
# Imprimir botones seleccionados
def print_selected_buttons():
    selected_buttons = [id for id, selected in button_states.items() if selected]
    print("Botones seleccionados:", selected_buttons)

def toggle_button(button_id):
    button_states[button_id] = not button_states[button_id]
    new_image = PhotoImage(file=relative_to_assets(f"button_{button_id}{'_select' if button_states[button_id] else ''}.png"))
    buttons[button_id].config(image=new_image)
    buttons[button_id].image = new_image
    
canvas.place(x = 0, y = 0)
# button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
# button_1 = Button( image=button_image_1, borderwidth=0, highlightthickness=0,
#     command=lambda: print("button_1 clicked"), relief="flat" )
# button_1.place( x=176.0, y=62.0, width=349.0, height=49.0)
image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
canvas.create_image( 176 + 349 / 2, 62 + 49 / 2, image=image_1 )

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button( image=button_image_2, borderwidth=0, highlightthickness=0,
    command=print_selected_buttons, relief="flat" )
button_2.place( x=226.0, y=490.0, width=249.0, height=38.0)

button_images = {}
buttons = {}
for i in range(3, 11):
    button_images[i] = PhotoImage(file=relative_to_assets(f"button_{i}.png"))
    buttons[i] = Button(
        image=button_images[i],
        borderwidth=0,
        highlightthickness=0,
        command=lambda i=i: toggle_button(i),
        relief="flat"
    )

button_positions = {
    3: (540, 287),
    4: (385, 287),
    5: (230, 287),
    6: (75, 288),
    7: (540, 150),
    8: (385, 150),
    9: (230, 150),
    10: (75, 150)}

for i in button_positions:
    buttons[i].place(x=button_positions[i][0], y=button_positions[i][1], width=100, height=121.43000030517578)

window.mainloop()
