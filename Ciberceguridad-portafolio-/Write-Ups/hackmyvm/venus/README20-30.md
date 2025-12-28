################
# MISSION 0x21 #
################

## EN ##
User eloise has saved her password in a particular way.

## ES ##
La usuaria eloise ha guardado su password de una forma particular.

cat mission.txt
################
# MISSION 0x21 #
################

## EN ##
User eloise has saved her password in a particular way.

## ES ##
La usuaria eloise ha guardado su password de una forma particular.

copiamos el contenido del archivo eloise a nuestra maquina y ejecutamos el siguiente comando

```bash
cat eloise | base64 -d > password_eloise.jpg```
esto se debe a que el texto en el archivo es una codificacion en base64 para una imagen,
en caso de hacer esto en un terminal sin acceso a un visualisador de imagenes se puede ejecutar un
servidor python con
```python
python3 -m http.server 800
````
y acceder desde el navegador a la imagen siendo la contraseña

yOUJlV0SHOnbSPm
