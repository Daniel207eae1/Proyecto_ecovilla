import socket
import struct

# Definir dirección y puerto del servidor
server_address = ('localhost', 502)

# Crear socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
client_socket.connect(server_address)

# Leer estado de la bobina 1
transaction_id = 1
unit_id = 1
function_code = 1
request_data = struct.pack(">HHBBHBB", transaction_id, 0, 7, unit_id, function_code, 0, 1)
client_socket.sendall(request_data)

# Recibir respuesta del servidor
response_data = client_socket.recv(1024)

# Desempaquetar respuesta Modbus
response_transaction_id, response_protocol_id, response_length, response_unit_id, response_function_code, byte_count, \
    bobina_1_estado = struct.unpack(">HHBBHBB", response_data[:10])

# Imprimir estado de la bobina 1
print("Estado de la bobina 1:", bobina_1_estado)

# Leer valor del registro 1
request_data = struct.pack(">HHBBHBBH", transaction_id, 0, 7, unit_id, function_code, 1, 0, 2)
client_socket.sendall(request_data)

# Recibir respuesta del servidor
response_data = client_socket.recv(1024)

# Desempaquetar respuesta Modbus
response_transaction_id, response_protocol_id, response_length, response_unit_id, response_function_code, byte_count, \
    registro_1_valor, registro_1_LSB = struct.unpack(">HHBBHBBHH", response_data[:11])

# Imprimir valor del registro 1
print("Valor del registro 1:", registro_1_valor)

# Cerrar conexión con el servidor
client_socket.close()