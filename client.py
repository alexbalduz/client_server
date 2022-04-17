#Se importa los módulos
import socket
import sys

#instanciamos un objeto para trabajar con el socket(lado cliente)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 10000)
print >>sys.stderr, 'conectando a %s puerto %s' % server_address
socket.connect(server_address)

try:
    # Enviando datos
    message = 'Este es el mensaje.  Se repitio.'
    print >>sys.stderr, 'enviando "%s"' % message
    socket.sendall(message)
    # Buscando respuesta
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = socket.recv(19)
        amount_received += len(data)
        print >>sys.stderr, 'recibiendo "%s"' % data

finally:
    print >>sys.stderr, 'cerrando socket'
    socket.close()