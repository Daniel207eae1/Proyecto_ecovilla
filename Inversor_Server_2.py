import socket
import struct

# Definir variables simuladas
bobina_1 = True
registro_1 = 100

# Crear socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Configurar dirección y puerto
server_address = ('localhost', 502)

# Vincular socket a la dirección y puerto
server_socket.bind(server_address)

# Poner el socket en modo escucha
server_socket.listen(1)

while True:
    # Aceptar conexión entrante
    client_socket, client_address = server_socket.accept()

    # Recibir datos del cliente
    data = client_socket.recv(1024)
    
    # Leer 7 bytes de la cabecera Modbus
    header_data = client_socket.recv(7)

    # Si no se reciben 7 bytes completos, manejar el error
    if len(header_data) < 7:
        # Manejar error de datos incompletos
        pass

    # Completar la lectura de datos según el tipo de solicitud Modbus
    if function_code == 1:
        # Leer 1 byte de datos para la bobina
        data += client_socket.recv(1)
    elif function_code == 3:
        # Leer 2 bytes de datos para el registro
        data += client_socket.recv(2)
    else:
        # Manejar error de función no válida
        pass
    
    
    # Desempaquetar datos Modbus
    transaction_id, protocol_id, length, unit_id, function_code = struct.unpack(">HHBBH", data[:7])

    # Procesar solicitud Modbus
    if function_code == 1:  # Leer bobinas
        if unit_id == 1:
            # Leer estado de la bobina 1
            response_data = struct.pack(">HHBBBBB", transaction_id, protocol_id, 2, unit_id, function_code, 1, bobina_1)
            client_socket.sendall(response_data)
        else:
            # Enviar error de unidad no válida
            error_response = struct.pack(">HHBBH", transaction_id, protocol_id, 2, 0, 255)
            client_socket.sendall(error_response)
    elif function_code == 3:  # Leer registros holding
        if unit_id == 1:
            # Leer valor del registro 1
            response_data = struct.pack(">HHBBHBBH", transaction_id, protocol_id, 4, unit_id, function_code, 2, registro_1, 0)
            client_socket.sendall(response_data)
        else:
            # Enviar error de unidad no válida
            error_response = struct.pack(">HHBBH", transaction_id, protocol_id, 2, 0, 255)
            client_socket.sendall(error_response)
    else:
        # Enviar error de función no válida
        error_response = struct.pack(">HHBBH", transaction_id, protocol_id, 2, 0, 255)
        client_socket.sendall(error_response)

    # Cerrar conexión con el cliente
    client_socket.close()