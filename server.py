# import socket programming library
import threading
from _thread import *
import socket
import gnupg
import json
from helpers import getEmailPublicKey
import random

gpg = gnupg.GPG(gnupghome='./server/gpg')
gpg.encoding = 'utf-8'


def Main():

    host = ""

    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to post", port)

    # put the socket into listening mode
    s.listen(4)
    print("socket is listening")

    # a forever loop until client wants to exit
    list_of_clients = []

    def encryptMessage(message, client):
        connection, email = client
        encrypted_message = gpg.encrypt(
            message, recipients=[email], always_trust=True)
        return str(encrypted_message).encode('ascii')

    def broadcast(message, connection):
        for client in list_of_clients:
            if type(client) == type([]) and client[0] != connection:
                try:
                    encrypted_message = encryptMessage(message, client)
                    client[0].send(encrypted_message)
                except:
                    client[0].close()
                    print('Fallo, desconectando a {}'.format(client[1]))
                    # if the link is broken, we remove the client
                    remove(client[0])

    def remove(connection):
        for client in list_of_clients:
            if client[0] == connection:
                list_of_clients.remove(client)
                break

    def validateUser(c, validate_user):
        """
        Función que valida que el usuario es el correcto a través
        del chequeo del código validador previamente enviado 
        """
        validation = c.recv(2048)
        validation = str(gpg.decrypt(validation.decode('ascii')))
        return validate_user == validation

    def getUser(c, validate_user):
        login_message_encripted = c.recv(1024)
        login_message = gpg.decrypt(login_message_encripted.decode('ascii'))
        login_message = json.loads(str(login_message))
        login_message["validation"] = validate_user
        email = login_message["user"]
        print(email)
        getEmailPublicKey(email, gpg, search=True, looking='Cliente')
        verification = json.dumps(login_message)
        encrypted_verification = gpg.encrypt(
            verification, recipients=[email], always_trust=True)
        encrypted_verification = str(encrypted_verification).encode('ascii')
        print(login_message)
        c.send(encrypted_verification)
        return email

    # thread fuction

    def threaded(c):
        validate_user = str(random.randint(0,1000))

        email = getUser(c, validate_user)
        
        index = list_of_clients.index(c)
        list_of_clients[index] = [c, email]

        if not validateUser(c, validate_user):
            print('Usuario no validado')
            c.close()
            return

        while True:
            try:
                message = c.recv(2048)
                if message:

                    """prints the message and address of the 
                    user who just sent the message on the server 
                    terminal"""
                    message = str(gpg.decrypt(message.decode('ascii')))
                    broadcast(message, c)

                else:
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    remove(c)
                    print('Cerrada la conección con {}, por envio de mensaje vacío'.format(email))
                    break

            except:
                continue

        c.close()

    while True:
        # establish connection with client
        c, addr = s.accept()
        list_of_clients.append(c)
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
