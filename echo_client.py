import socket

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 34566  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    print('Introduzca los siguientes datos meteorológicos: temperatura mínima, temperatura máxima, presión y pluviometría')

    lista_datos=[]

    message = input(" -> ")
    temp_min=int(message)
    lista_datos.append(temp_min)

    message = input(" -> ")
    temp_max=int(message)
    lista_datos.append(temp_max)

    message = input(" -> ")
    presion=int(message)
    lista_datos.append(presion)

    message = input(" -> ")
    pluvi=int(message)
    lista_datos.append(pluvi)

    #mensaje para parar la conexión cuando se han introducido los datos
    message = input(" -> ")

    while message.lower().strip() != 'fin':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection
    print(lista_datos)

if __name__ == '__main__':
    client_program()