# import socket

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# # if instead of '127.0.0.1' you pass an empty string ''
# # the server will accept connections on all available IPv4 interfaces
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# import socket programming library 
import socket
import gnupg
import json

gpg = gnupg.GPG(gnupghome='./gpg')
gpg.encoding = 'utf-8' 
  
# import thread module 
from _thread import *
import threading 
  
print_lock = threading.Lock() 
  
# thread fuction 
def threaded(c):
  data = b'Bienvenido al Chat Seguro\n'
  c.send(data)
  email = True
  client_key = []
  while not client_key:
    email = c.recv(1024)
    if not email:
      break
    email = email.decode('ascii')
    print('Looking for client', email)
    for _ in range(3):
      client_key = gpg.search_keys(email, 'pgp.mit.edu')
      print(client_key)
      if not client_key:
        continue
      break
    if not client_key:
      data = json.dumps({
        "msg": "Email no encontrado, intentelo denuevo\n",
        "error": "True"
        })
      c.send(data.encode('ascii'))
      continue
    client_key = str(client_key)
    data = json.dumps({
        "msg": client_key,
        "error": "False"
        }).encode('ascii')
    c.send(data)

  c.close() 
    # while True: 
  
    #     # data received from client 
    #     data = c.recv(1024) 
    #     if not data: 
    #         print('Bye') 
              
    #         # lock released on exit 
    #         # print_lock.release()
    #         break
        
    #     # reverse the given string from client 
    #     data = data[::-1] 
  
    #     # send back reversed string to client 
    #     c.send(data)
    #     # print_lock.release()
  
    # # connection closed 
  
  
def Main(): 
    host = "" 
  
    # reverse a port on your computer 
    # in our case it is 12345 but it 
    # can be anything 
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((host, port)) 
    print("socket binded to post", port) 
  
    # put the socket into listening mode 
    s.listen(5) 
    print("socket is listening") 
  
    # a forever loop until client wants to exit 
    while True: 
  
        # establish connection with client 
        c, addr = s.accept() 
  
        # lock acquired by client 
        # print_lock.acquire() 
        print('Connected to :', addr[0], ':', addr[1]) 
  
        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,)) 
    s.close() 
  
  
if __name__ == '__main__': 
    Main() 