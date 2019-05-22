# import socket
import socket
import gnupg
import json
import sys
import select
from helpers import getEmailPublicKey
  
if len(sys.argv) < 2:
  print('Lea el Readme para entender como correr el programa adecuadamaente')
  sys.exit()
POSIBLE_USERS = {
  'prob33@test.cl': 'client1',
  'prob34@test.cl': 'client2',
  'prob35@test.cl': 'client3'
}
user = sys.argv[1]
if user not in POSIBLE_USERS:
  print('Ingrese un usuario válido, puede ser prob33@test.cl o prob34@test.cl o prob35@test.cl')
  sys.exit()

gpg = gnupg.GPG(
    gnupghome='./{}/gpg'.format(POSIBLE_USERS[user]))
gpg.encoding = 'utf-8'

SERVER_EMAIL = 'serverprob12@server.cl'

def sendVerification(s, validation_code):
  encrypted_validation_code = gpg.encrypt(validation_code, recipients=[SERVER_EMAIL], always_trust=True)
  s.send(str(encrypted_validation_code).encode('ascii'))

def Main():
  # local host IP '127.0.0.1'
  host = '127.0.0.1'

  # set to True to search for server public key in pgp.mit.edu
  getEmailPublicKey(SERVER_EMAIL, gpg)

  # Define the port on which you want to connect
  port = 12345

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # connect to server on local computer
  s.connect((host, port))
  password = input('Ingrese una contraseña para autentificar al servidor: ')
  print('Enviando email {} encryptado para logear al servidor'.format(user))
  login = json.dumps({
    "user": user,
    "password": password
  })
  encrypted_ascii_user = gpg.encrypt(login, recipients=[SERVER_EMAIL], always_trust=True)
  s.send(str(encrypted_ascii_user).encode('ascii'))
  check_server = s.recv(1024)
  check_server = gpg.decrypt(check_server.decode('ascii'))
  login = json.loads(login)
  check_server = json.loads(str(check_server))
  if check_server["password"] != login["password"] or not "validation" in check_server:
    print('El Servidor está comprometido, intentelo más tarde')
    s.close()
    sys.exit()
  print('Servidor conectado correctamente')

  sendVerification(s, check_server["validation"])

  while True: 
  
    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, s]
    
    """ There are two possible input situations. Either the 
    user wants to give  manual input to send to other people, 
    or the server is sending a message  to be printed on the 
    screen. Select returns from sockets_list, the stream that 
    is reader for input. So for example, if the server wants 
    to send a message, then the if condition will hold true 
    below.If the user wants to send a message, the else 
    condition will evaluate as true"""

    read_sockets, write_socket, error_socket = select.select(sockets_list,[],[]) 
  
    for socks in read_sockets: 
        if socks == s: 
            message = socks.recv(2048)
            message = gpg.decrypt(message.decode('ascii'))
            sys.stdout.write(str(message))
            sys.stdout.flush()
        else: 
            message = sys.stdin.readline()
            sys.stdout.write("<You>") 
            sys.stdout.write(message) 
            sys.stdout.flush()
            message = '<{}> : '.format(user) + message
            encrypted_message = gpg.encrypt(message, recipients=[SERVER_EMAIL], always_trust=True)
            s.send(str(encrypted_message).encode('ascii'))

  s.close() 


if __name__ == '__main__': 
  Main() 



