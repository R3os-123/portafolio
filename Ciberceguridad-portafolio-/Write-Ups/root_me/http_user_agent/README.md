# Write-up: HTTP - User-Agent Manipulation

## 📝 Descripción
El servidor restringe el acceso a la información basándose en la identidad del navegador (User-Agent). Si el agente no coincide con el valor esperado, el acceso es denegado.

## 🚀 Explotación
Al analizar la respuesta inicial del servidor, se observa el mensaje de error:
`Wrong user-agent: you are not the...`

Utilizando `curl`, podemos suplantar nuestra identidad enviando la cabecera modificada:

```bash
curl -A "admin" -L [http://challenge01.root-me.org/web-serveur/ch2](http://challenge01.root-me.org/web-serveur/ch2)

```

🚩 Resultado
El servidor valida la cadena "admin" y devuelve el mensaje de bienvenida junto con la contraseña.

Flag: rr$Li9%L34qd1AAe27

🛡️ Mitigación
Nunca se debe usar el User-Agent para control de acceso o seguridad, ya que es una cabecera controlada totalmente por el cliente y es trivialmente falsificable.
