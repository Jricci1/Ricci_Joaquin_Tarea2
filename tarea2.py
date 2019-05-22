import gnupg

gpg = gnupg.GPG(gnupghome='./gpg')
gpg.encoding = 'utf-8'

# input_data = gpg.gen_key_input(key_type="RSA", key_length=1024, name_email='jprob@prob.cl')
# key = gpg.gen_key(input_data)
# print(key)


# public_keys = gpg.list_keys() # same as gpg.list_keys(False)
# private_keys = gpg.list_keys(True) # True => private keys
# a = gpg.send_keys('pgp.mit.edu', public_keys[0]['keyid'])
# print(a)

# print(public_keys)
# print('---------------------------')
# print(private_keys)

# signed_data = gpg.sign("hola soy el servidor", passphrase = "my passphrase")
# gpg.verify(signed_data.data).valid

key2 = gpg.search_keys('jprob@prob.cl', 'pgp.mit.edu')
print(key2)