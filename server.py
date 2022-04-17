#Se importa los módulos
import socket
import sys

#instanciamos un objeto para trabajar con el socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Puerto y servidor que debe escuchar
server_address = ('localhost', 10000)

#Aceptamos conexiones entrantes con el metodo listen. Por parámetro las conexiones simutáneas.
socket.bind(server_address)

#print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address

# poner socket a modo de servidor
socket.listen(1)

while True:
    # Esperando conexion
    #print >>sys.stderr, 'Esperando para conectarse'

    #accept, acepta una conexión
    connection, client_address = socket.accept()

    try:
        #print >>sys.stderr, 'concexion desde', client_address

        # Recibe los datos en trozos y reetransmite
        while True:
            data = connection.recv(19)
            #print >>sys.stderr, 'recibido "%s"' % data
            if data:
                #print >>sys.stderr, 'enviando mensaje de vuelta al cliente'
                connection.sendall(data)
            else:
                #print >>sys.stderr, 'no hay mas datos', client_address
                break

    finally:
        # Cerrando conexion
        connection.close()
