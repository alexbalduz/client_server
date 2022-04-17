import sys
import socket
import selectors
import types

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


def accept_wrapper(sock):
    #para poner el socket en un modo de no-bloqueo
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

sel = selectors.DefaultSelector()

host, port = '127.0.0.1', 65432
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