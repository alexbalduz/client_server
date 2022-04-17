import sys
import socket
import selectors
import types

def accept_wrapper(sock):
    #para poner el socket en un modo de no-bloqueo
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

sel = selectors.DefaultSelector()

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {(host, port)}")

#con esta diferencia, el servidor no se podrá bloquear
lsock.setblocking(False)

#data almacena la información en el socket
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        #devuelve una lista de tuplas, una por cada socket
        events = sel.select(timeout=None)
        for key, mask in events:
            #tenemos dos opciones, que la tupla sea None
            #entonces, entonces de la función listen, se tendrá que aceptar la conexión
            if key.data is None:
                accept_wrapper(key.fileobj)

            #si no es None, entonces el socket ya ha sido aceptado y se tendrá que servir al cliente
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Caught keyboard interrupt, exiting")
finally:
    sel.close()