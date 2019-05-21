import gnupg

server_gpg = gnupg.GPG(gnupghome='./server/gpg')
server_gpg.encoding = 'utf-8'

input_data_server = server_gpg.gen_key_input(
  key_type="RSA",
  key_length=1024,
  name_email='serverprob12@server.cl',
  passphrase='contraseñaservidor'
  )
server_key = server_gpg.gen_key(input_data_server)
print('1: ', server_key)

key = []
while not key:
  server_gpg.send_keys('pgp.mit.edu', server_gpg.list_keys()[0]['keyid'])
  key = server_gpg.search_keys('serverprob12@server.cl', 'pgp.mit.edu')
print('server:', key)

print('----------')

client1_gpg = gnupg.GPG(gnupghome='./client1/gpg')
client1_gpg.encoding = 'utf-8'

input_data_cliente1 = client1_gpg.gen_key_input(
  key_type="RSA",
  key_length=1024,
  name_email='prob33@test.cl',
  passphrase='contraseñaCliente1'
  )
client1_key = client1_gpg.gen_key(input_data_cliente1)
print('1: ', client1_key)
key = []
while not key:
  client1_gpg.send_keys('pgp.mit.edu', client1_gpg.list_keys()[0]['keyid'])
  key = client1_gpg.search_keys('prob33@test.cl', 'pgp.mit.edu')
print('cliente1:', key)

print('----------')

client2_gpg = gnupg.GPG(gnupghome='./client2/gpg')
client2_gpg.encoding = 'utf-8'

input_data_cliente2 = client2_gpg.gen_key_input(
  key_type="RSA",
  key_length=1024,
  name_email='prob34@test.cl',
  passphrase='contraseñaCliente2'
  )
client2_key = client2_gpg.gen_key(input_data_cliente2)
print('1: ', client2_key)
key = []
while not key:
  client2_gpg.send_keys('pgp.mit.edu', client2_gpg.list_keys()[0]['keyid'])
  key = client2_gpg.search_keys('prob34@test.cl', 'pgp.mit.edu')
print('cliente2:', key)

print('----------')

client3_gpg = gnupg.GPG(gnupghome='./client3/gpg')
client3_gpg.encoding = 'utf-8'

input_data_cliente3 = client3_gpg.gen_key_input(
  key_type="RSA",
  key_length=1024,
  name_email='prob35@test.cl',
  passphrase='contraseñaCliente3'
  )
client3_key = client3_gpg.gen_key(input_data_cliente3)
print('1: ', client3_key)
key = []
while not key:
  client3_gpg.send_keys('pgp.mit.edu', client3_gpg.list_keys()[0]['keyid'])
  key = client3_gpg.search_keys('prob35@test.cl', 'pgp.mit.edu')
print('cliente3:', key)

print('----------')