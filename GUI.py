from tkinter import Tk, Label, Button, filedialog, Menu, Toplevel

import cv2

from flowchart_recognition import flowchart
from convert_to_txt import process_json
from digital_diagram import generar_diagrama
import pytesseract

json_file = 'data.json'  # Ajusta este nombre si tu archivo JSON tiene otro nombre
output_file = 'resultado_diagrama.txt'

def alert_popup(title, message):
    """Genera una ventana emergente para mensajes especiales."""
    root = Tk()
    root.title(title)
    w, h = 400, 200  # ancho y alto de la ventana emergente
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (sw - w) / 2, (sh - h) / 2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    m = message + '\n'
    w = Label(root, text=m, width=50, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=5)
    b.pack()


def database():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    try:
        filename = root.filename
    except:
        alert_popup('¡Mensaje de error!', 'Primero selecciona un archivo')
        return
    if filename == '':
        alert_popup('¡Mensaje de error!', 'Primero selecciona un archivo')
        return

    popup = Toplevel()
    Label(popup, text="Procesando...").grid(row=0, column=0)

    popup.pack_slaves()
    popup.update()
    flowchart(filename)
    process_json(json_file, output_file)
    generar_diagrama(output_file, 'Flowchart')
    popup.destroy()

    root.filename = ''
    alert_popup('Completado', 'Tu tarea ha sido completada.')


def OpenFile():
    root.filename = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos JPEG", "*.jpg"), ("Archivos PNG", "*.png"), ("Todos los archivos", "*.*"))
    )
    cv2.namedWindow("Salida", cv2.WINDOW_NORMAL)  # Crear ventana con dimensiones libres
    cv2.imshow("Salida", cv2.resize(cv2.imread(root.filename), (2000, 750)))  # Mostrar imagen
    cv2.waitKey(0)


def About():
    popup = Toplevel()
    Label(popup, text="Reconocimiento de Diagramas de Flujo Dibujados a Mano").grid(row=10, column=1)


def show():
    root.filename = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos PNG", "*.png"), ("Archivos JPEG", "*.jpg"), ("Todos los archivos", "*.*"))
    )


if __name__ == "__main__":
    root = Tk()
    root.geometry('500x400')
    root.title("Reconocimiento de Diagramas de Flujo a Mano")

    menu = Menu(root)
    root.config(menu=menu)

    filemenu = Menu(menu)
    menu.add_cascade(label="Archivo", menu=filemenu)

    filemenu.add_command(label="Abrir...", command=OpenFile)
    filemenu.add_separator()

    filemenu.add_command(label="Salir", command=root.destroy)

    help_menu = Menu(menu)
    menu.add_cascade(label="Ayuda", menu=help_menu)
    help_menu.add_command(label="Acerca de...")

    label_0 = Label(root, text="Reconocimiento de\nDiagramas de Flujo a Mano", width=30, font=("bold", 20))
    label_0.place(x=60, y=50)

    Button(root, text='Seleccionar imagen', width=30, bg='blue', fg='white', command=show).place(x=150, y=150)
    Button(root, text='Iniciar', width=30, bg='brown', fg='white', command=database).place(x=150, y=250)

    root.mainloop()
