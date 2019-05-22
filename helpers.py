def getEmailPublicKey(email, gpg, search=False, looking='Servidor'):
  server_key = []
  print('Buscando {}....'.format(looking))
  if not search:
    if len(gpg.list_keys()) > 1:
      return gpg.list_keys()[1]
  while not server_key:
    server_key = gpg.search_keys(email, 'pgp.mit.edu')
  public_key = [x for x in gpg.list_keys() if x['fingerprint'] == server_key[0]['keyid']]
  while not public_key:
    public_key = gpg.recv_keys('pgp.mit.edu', server_key[0]['keyid'])
  print('{} encontrado....'.format(looking))
  return public_key