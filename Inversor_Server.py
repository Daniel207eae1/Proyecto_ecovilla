from pymodbus.server.async_io import ModbusServerTCP
from pymodbus.datastore import ModbusDataStore
import threading
import struct 

# Definir variables del servidor
SERVER_ADDRESS = "localhost"
SERVER_PORT = 502

# Create storage for Modbus data (combined for simplicity)
data_store = ModbusDataStore()
data_store.add_holding_registers(0, [0] * 100)  # Initialize 100 holding registers

# Crear almacenamiento de datos Modbus
register_values = ModbusDataStore()
register_values.add_holding_registers(0, [0] * 100)  # Initialize 100 holding registers

# Define storage for input registers (optional)
input_register_values = [0] * 2  # Adjust length based on number of variables you want to receive


# Función para procesar las variables enviadas por el cliente
def process_variables(variables):
    # Capturar las variables del diccionario
    temperature = variables.get("temperature")
    humidity = variables.get("humidity")

    # Realizar acciones en base a las variables capturadas
    print(f"Temperatura recibida: {temperature}")
    print(f"Humedad recibida: {humidity}")

    # Simular el control de un sistema de climatización
    if temperature > 25:
        print("Encendiendo aire acondicionado")
    elif temperature < 20:
        print("Encendiendo calefacción")
    else:
        print("Condiciones de temperatura adecuadas")

    if humidity > 60:
        print("Encendiendo deshumidificador")
    elif humidity < 40:
        print("Encendiendo humidificador")
    else:
        print("Condiciones de humedad adecuadas")

# Crear servidor Modbus TCP
server = ModbusServerTCP(data_store, address=(SERVER_ADDRESS, SERVER_PORT))

def handle_client(client_socket):
    """Manejar la conexión con un cliente Modbus."""
    while True:
        # Recibir solicitud del cliente
        request_data = client_socket.recv(1024)

        # Decodificar solicitud Modbus
        function_code = request_data[0]
        starting_address = struct.unpack(">H", request_data[1:3])[0]
        quantity = struct.unpack(">H", request_data[3:5])[0]

        # Procesar solicitud según el código de función
        if function_code == 16:  # Leer registros de retención
            response_data = build_read_holding_registers_response(
                starting_address, quantity, register_values["holding_registers"]
            )
        elif function_code == 17:  # Escribir registros de retención
            new_values = request_data[5:]
            register_values["holding_registers"][starting_address : starting_address + quantity] = new_values
            response_data = build_write_multiple_registers_response(starting_address, quantity)
        elif function_code == 23:  # Leer registros de entrada
            response_data = build_read_input_registers_response(
                starting_address, quantity, input_register_values
            )
        elif function_code == 24:  # Escribir registros de entrada
            new_values = request_data[5:]
            input_register_values[starting_address : starting_address + quantity] = new_values
            response_data = build_write_multiple_input_registers_response(starting_address, quantity)
        elif function_code == 1:  # Leer registros de retención (para capturar variables del cliente)
            if starting_address == 10 and quantity == 2:  # Si se leen los registros de temperatura y humedad
                variables = {
                    "temperature": input_register_values[0],
                    "humidity": input_register_values[1]
                }
                # Procesar las variables recibidas del cliente
                process_variables(variables)
            response_data = build_read_holding_registers_response(
                starting_address, quantity, register_values["holding_registers"]
            )
        else:
            response_data = build_exception_response(function_code)

        # Enviar respuesta al cliente
        client_socket.sendall(response_data)

def build_read_holding_registers_response(starting_address, quantity, register_values):
    """Construir una respuesta de lectura de registros de retención."""
    response_data = struct.pack(">BBHH", 1, 0, quantity * 2, starting_address)
    for value in register_values[starting_address : starting_address + quantity]:
        response_data += struct.pack(">H", value)
    return response_data

def build_write_multiple_registers_response(starting_address, quantity):
    """Construir una respuesta de escritura de registros de retención."""
    return struct.pack(">BBHH", 4, 0, quantity, starting_address)

def build_read_input_registers_response(starting_address, quantity, input_register_values):
    """Construir una respuesta de lectura de registros de entrada."""
    response_data = struct.pack(">BBHH", 3, 0, quantity * 2, starting_address)
    for value in input_register_values[starting_address : starting_address + quantity]:
        response_data += struct.pack(">H", value)
    return response_data

def build_read_input_registers_response(starting_address, quantity, input_register_values):
    """Construir una respuesta de lectura de registros de entrada."""
    response_data = struct.pack(">BBHH", 3, 0, quantity * 2, starting_address)
    for value in input_register_values[starting_address : starting_address + quantity]:
        response_data += struct.pack(">H", value)
    return response_data

def build_write_multiple_input_registers_response(starting_address, quantity):
    """Construir una respuesta de escritura de registros de entrada."""
    return struct.pack(">BBHH", 16, 0, quantity, starting_address)

def build_exception_response(function_code):
    """Construir una respuesta de excepción."""
    return struct.pack(">BB", function_code + 128, 0)