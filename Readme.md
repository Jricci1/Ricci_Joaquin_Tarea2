# Tarea 2 Chat


* ***Las llaves están publicadas en pgp.mit.edu en vez de pool.sks-keyservers.net.***


### Test Users:
El archivo testUserCreator.py fue utilizado para crear 3 usuarios y un servidor a modo de prueba de la aplicación junto con sus passphrase.
Fue utilizando el comando:
```
  python3 testUserCreator.py
```
  - Server Email: serverprob12@server.cl, passphrase: contraseñaservidor
  - Client1 Email: prob33@test.cl, passphrase: contraseñaCliente1
  - Client2 Email: prob34@test.cl, passphrase: contraseñaCliente2
  - Client3 Email: prob35@test.cl, passphrase: contraseñaCliente3

Este archivo ya ha sido ejecutado, por lo que no es necesario correrlo nuevamente.
Junto con los archivos de la tarea, se envian los archivos gpg de cada cliente y del servidor respectivo para que puedan utilizarlos para la corrección. Para cada cliente de prueba, su llave pública fue subida al servidor pgp.mit.edu, por lo que la tarea hace uso de estos.

## Tarea

A modo de simpllificación, se crean los 3 usuarios mencionados anteriormente junto con el servidor y sus carpetas gpg respectivas con sus claves.

Para utilizar el programa, debe ejecutar en primer lugar el servidor en un terminal con el comando:
```
  python3 server.py
```

Luego puede inicializar los clientes, para eso utilizara el siguiente comando:

```
  python3 client.py email
```

donde email debe ser reemplazado por alguno de los expuesto en la primera parte.

Cuando se inizializa un cliente, este va al servidor pgp.mit.edu en busca de la llave pública del servidor, por lo que puede demorar. Dado que es algo molesto esperar tanto, hay un atajo implementado, dado que las carpetas gpg ya tienen guardada la llave pública del servidor, la van a buscar directamente entre sus llaves, si desea implementar la funcionalidad completa y esperar lo que corresponda, solo debe cambiar
esto:

```
  getEmailPublicKey(email, gpg)
```
por

```
  getEmailPublicKey(email, gpg, search=True)
```
en la linea 37 del archivo *client.py*.

Luego de conseguir la llave pública del servidor en cuestión, el usuario o cliente se conecta y envía un mensaje al servidor para autenticarse, en el envía su email, y una contraseña a elección del usuario a la hora de iniciar (la contraseña puede y debe cambiarse cada vez por razones de seguridad) para luego verificar que el servidor es el indicado. Este mensaje lo envía encriptado con la llave pública del servidor.

El servidor recibe la conexión, inicializa un thread y recibe el mensaje de login. Este mensaje lo desencripta y procede a buscar indefinidamente la llave pública del usuario en el servidor pgp.mit.edu. Dado que busca indefinidamente es que cree los usuarios de prueba, para asegurarme de que eventualmente los encontrara (la librería o el servidor fallan de repeente, por eso se busca hasta encontrar). Luego de haber encontrado la llave pública, la guarda y envía de vuelta el mensaje de encriptado con la llave pública del cliente y junto con un número de verificación.

El usuario recibe la respuesta, compara si la contraseña que ingreso es la enviado por el servidor, si es correcta, queda verificado que el servidor es el correcto, y procede a devolverle el código de verificación enviado por el servidor.

El servidor chequea que el código de verificación sea el correcto y entonces queda verificado y autenticado el usuario.

Luego de esto el usuario puede mandar mensajes que serán recibidos por todos los usuarios conectados simultaneamente.

Si un usuario se desconecta y vuelve a conectarse seguira funcinando como debe ser.

Es importante recordar que si aparece el dialogo pidiendo el ingreso de la contraseña, verificar que email es (en el dialogo), e ingresar su  **passphrase**.

La implementación cumple con los requerimientos de la tarea.