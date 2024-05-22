import pytesseract
from PIL import ImageGrab
import win32gui

# Obtener HWND de la ventana del software de monitoreo
window_name = "SolarPowerMonitor"  # Reemplaza con el nombre real
hwnd = win32gui.FindWindow(None, window_name)
win32gui.GetCapture()
print(hwnd)

# Si se encuentra la ventana
if hwnd:
    # Capturar imagen de la ventana
    rect = win32gui.GetWindowRect(hwnd)  # Obtener rectángulo de la ventana
    x0, y0, x1, y2 = rect
    screenshot = ImageGrab.grab((x0, y0, x1, y2))

    # Procesamiento posterior (como se muestra en el código anterior)
    # Reconocimiento de texto
    text = pytesseract.image_to_string(screenshot)

    # Procesamiento de datos
    data = []
    for line in text.split('\n'):
        if line:
            # Separar valores y convertir a tipos de datos
            values = [float(value) for value in line.split()]
            data.append(values)

    # Envío de datos a Python
    print(data) # Imprime los datos en la consola
    # Puedes modificar este código para enviar los datos a una función o archivo
else:
    print("No se encontró la ventana:", window_name)