hacker@venus:~$ ls
mission.txt  readme.txt
hacker@venus:~$ cat mission.txt
#################
# MISSION 0x01 #
################

## EN ##
User sophia has saved her password in a hidden file in this folder. Find it and log in as sophia.

## ES ##
La usuaria sophia ha guardado su contraseña en un fichero oculto en esta carpeta.Encuentralo y logueate como sophia.
hacker@venus:~$ ls -la
total 44
drwxr-x--- 1 root   hacker 4096 Apr  5  2024 .
drwxr-xr-x 1 root   root   4096 Apr  5  2024 ..
-rw-r----- 1 root   hacker   31 Apr  5  2024 ...
-rw-r--r-- 1 hacker hacker  220 Apr 23  2023 .bash_logout
-rw-r--r-- 1 hacker hacker 3526 Apr 23  2023 .bashrc
-rw-r----- 1 root   hacker   16 Apr  5  2024 .myhiddenpazz
-rwxr-xr-x 1 hacker hacker  807 Apr 23  2023 .profile
-rw-r----- 1 root   hacker  287 Apr  5  2024 mission.txt
-rw-r----- 1 root   hacker 2542 Apr  5  2024 readme.txt
hacker@venus:~$ cat .myhiddenpazz
Y1o645M3mR84ejc
hacker@venus:~$ exit


sophia@venus:~$ cat mission.txt
################
# MISSION 0x02 #
################

## EN ##
The user angela has saved her password in a file but she does not remember where ... she only remembers that the file was called whereismypazz.txt

## En ##
```bash
La usuaria angela ha guardado su password en un fichero pero no recuerda donde... solo recuerda que el fichero se llamaba whereismypazz.txt
sophia@venus:~$ find ../../ -name "whereismypazz.txt" 2>/dev/null
../../usr/share/whereismypazz.txt
sophia@venus:~$ cd ../../usr/share
sophia@venus:/usr/share$ cat whereismypazz.txt
oh5p9gAABugHBje
sophia@venus:/usr/share$ exit
logout
```

angela@venus:~$ cat mission.txt
################
# MISSION 0x03 #
################

## EN ##
The password of the user emma is in line 4069 of the file findme.txt

## ES ##
La password de la usuaria emma esta en la linea 4069 del fichero findme.txt
angela@venus:~$ cat flagz.txt
8===SjMYBmMh4bk49TKq7PM8===D~~
angela@venus:~$ ls
findme.txt  flagz.txt  mission.txt
angela@venus:~$ sed -n '4069p' findme.txt
fIvltaGaq0OUH8O
angela@venus:~$ exit



Last login: Sun Dec 21 20:17:15 2025 from 103.219.234.203
emma@venus:~$ cat mission.txt
################
# MISSION 0x04 #
################

## EN ##
User mia has left her password in the file -.
## ES ##
La usuaria mia ha dejado su password en el fichero -.
emma@venus:~$ cat flagz.txt
8===0daqdDlmd9XogkiHu4yq===D~~
emma@venus:~$ cat ./-
iKXIYg0pyEH2Hos
emma@venus:~$


cat mission.txt
################
# MISSION 0x05 #
################

## EN ##
It seems that the user camila has left her password inside a folder called hereiam

## ES ##
Parece que la usuaria camila ha dejado su password dentro de una carpeta llamada hereiam
mia@venus:~$ find ../../ -name "hereiam" 2>/dev/null
../../opt/hereiam
mia@venus:~$ cd ../../opt/hereiam
mia@venus:/opt/hereiam$ ls -la
total 12
drwxr-xr-x 2 root root 4096 Apr  5  2024 .
drwxr-xr-x 1 root root 4096 Apr  5  2024 ..
-rw-r--r-- 1 root root   16 Apr  5  2024 .here
mia@venus:/opt/hereiam$ cat .here
F67aDmCAAgOOaOc
mia@venus:/opt/hereiam$


camila@venus:~$ cat mission.txt
################
# MISSION 0x06 #
################

## EN ##
The user luna has left her password in a file inside the muack folder.

## ES ##
La usuaria luna ha dejado su password en algun fichero dentro de la carpeta muack.
camila@venus:~$ cd muack/
camila@venus:~/muack$ find . -type f -readable
./111/111/muack
camila@venus:~/muack$ cd 11
11/  110/ 111/ 112/ 113/ 114/ 115/ 116/ 117/ 118/ 119/
camila@venus:~/muack$ cd 111/111
camila@venus:~/muack/111/111$ ls -la
total 12
drwxr-xr-x   2 root root   4096 Apr  5  2024 .
drwxr-xr-x 152 root root   4096 Apr  5  2024 ..
-rw-r-----   1 root camila   16 Apr  5  2024 muack
camila@venus:~/muack/111/111$ cat muack
j3vkuoKQwvbhkMc
camila@venus:~/muack/111/111$

################
# MISSION 0x07 #
################

## EN ##
The user eleanor has left her password in a file that occupies 6969 bytes.

## ES ##
La usuaria eleanor ha dejado su password en un fichero que ocupa 6969 bytes.
luna@venus:~$ find ../../ -size 6969c 2>/dev/null
../../usr/share/moon.txt
luna@venus:~$ cat "../../usr/share/moon.txt"
UNDchvln6Bmtu7b


################
# MISSION 0x08 #
################

## EN ##
The user victoria has left her password in a file in which the owner is the user violin.

## ES ##
La usuaria victoria ha dejado su password en un fichero en el cual el propietario es el usuario violin.
eleanor@venus:~$ find ../../ -user violin -type f 2>/dev/null
../../usr/local/games/yo
eleanor@venus:~$ find ../../ -user violin -type f 2>/dev/null | cd
eleanor@venus:~$ cat "../../usr/local/games/yo"
pz8OqvJBFxH0cSj
eleanor@venus:~$ cat flagz.txt
8===Iq5vbyiQl4ipNrLDArjD===D~~
eleanor@venus:~$

isla@venus:~$ cat mission.txt
################
# MISSION 0x10 #
################

## EN ##
The password of the user violet is in the line that begins with a9HFX (these 5 characters are not part of her password.).

## ES ##
El password de la usuaria violet esta en la linea que empieza por a9HFX (sin ser estos 5 caracteres parte de su password.).
isla@venus:~$ grep "^a9HFX" passy
a9HFXWKINVzNQLKLDVAc
la contraseña es WKINVzNQLKLDVAc

################
# MISSION 0x11 #
################                                                              
## EN ##
The password of the user lucy is in the line that ends with 0JuAZ (these last 5 characters are not part of her password)

## ES ##
El password de la usuaria lucy se encuentra en la linea que acaba por 0JuAZ (sin ser estos ultimos 5 caracteres parte de su password)
violet@venus:~$ grep "0JuAZ$" end                                             OCmMUjebG53giud0JuAZ
OCmMUjebG53giud0JuAZ

lucy@venus:~$ ls
file.yo  flagz.txt  mission.txt
lucy@venus:~$ cat flagz.txt
8===AdCJ4wl8pmbhi770Xbd3===D~~
lucy@venus:~$ cat mission.txt
################
# MISSION 0x12 #
################

## EN ##
The password of the user elena is between the characters fu and ck

## ES ##
El password de la usuaria elena esta entre los caracteres fu y ck
lucy@venus:~$ grep -oP '(?<=fu).*(?=ck)' file.yo
4xZ5lIKYmfPLg9t
lucy@venus:~$

cat flagz.txt
8===st1pTdqEQ0bvrJfWGwLA===D~~
elena@venus:~$ cat mission.txt
################
# MISSION 0x13 #
################

## EN ##
The user alice has her password is in an environment variable.

## ES ##
La password de alice esta en una variable de entorno.
elena@venus:~$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
elena@venus:~$ echo $SHELL
/bin/bash
elena@venus:~$ echo $
$
elena@venus:~$ echo $SYSM

elena@venus:~$ printenv
SHELL=/bin/bash
PWD=/pwned/elena
LOGNAME=elena
MOTD_SHOWN=pam
HOME=/pwned/elena
LANG=en_US.UTF-8
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=00:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.avif=01;35:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:*~=00;90:*#=00;90:*.bak=00;90:*.old=00;90:*.orig=00;90:*.part=00;90:*.rej=00;90:*.swp=00;90:*.tmp=00;90:*.dpkg-dist=00;90:*.dpkg-old=00;90:*.ucf-dist=00;90:*.ucf-new=00;90:*.ucf-old=00;90:*.rpmnew=00;90:*.rpmorig=00;90:*.rpmsave=00;90:
SSH_CONNECTION=103.219.234.203 6768 172.66.0.10 22
TERM=xterm-256color
USER=elena
PASS=Cgecy2MY2MWbaqt
SHLVL=1
SSH_CLIENT=103.219.234.203 6768 22
PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
SSH_TTY=/dev/pts/6
_=/usr/bin/printenv
elena@venus:~$


alice@venus:~$ cat mission.txt
################
# MISSION 0x14 #
################

## EN ##
The admin has left the password of the user anna as a comment in the file passwd.

## ES ##
El admin ha dejado la password de anna como comentario en el fichero passwd.
alice@venus:~$ cat  /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:998:998:systemd Network Management:/:/usr/sbin/nologin
mysql:x:100:102:MySQL Server,,,:/nonexistent:/bin/false
systemd-timesync:x:997:997:systemd Time Synchronization:/:/usr/sbin/nologin
Debian-exim:x:101:103::/var/spool/exim4:/usr/sbin/nologin
messagebus:x:102:104::/nonexistent:/usr/sbin/nologin
bind:x:103:106::/var/cache/bind:/usr/sbin/nologin
sshd:x:104:65534::/run/sshd:/usr/sbin/nologin
violin:x:1000:1000::/pwned/violin:/bin/bash
executor:x:1001:1001::/pwned/executor:/bin/bash
sophia:x:1002:1002::/pwned/sophia:/bin/bash
angela:x:1003:1003::/pwned/angela:/bin/bash
emma:x:1004:1004::/pwned/emma:/bin/bash
mia:x:1005:1005::/pwned/mia:/bin/bash
camila:x:1006:1006::/pwned/camila:/bin/bash
luna:x:1007:1007::/pwned/luna:/bin/bash
eleanor:x:1008:1008::/pwned/eleanor:/bin/bash
victoria:x:1009:1009::/pwned/victoria:/bin/bash
isla:x:1010:1010::/pwned/isla:/bin/bash
violet:x:1011:1011::/pwned/violet:/bin/bash
lucy:x:1012:1012::/pwned/lucy:/bin/bash
elena:x:1013:1013::/pwned/elena:/bin/bash
alice:x:1014:1014:w8NvY27qkpdePox:/pwned/alice:/bin/bash
anna:x:1015:1015::/pwned/anna:/bin/bash
natalia:x:1016:1016::/pwned/natalia:/bin/bash
eva:x:1017:1017::/pwned/eva:/bin/bash
clara:x:1018:1018::/pwned/clara:/bin/bash
frida:x:1019:1019::/pwned/frida:/bin/bash
eliza:x:1020:1020::/pwned/eliza:/bin/bash
iris:x:1021:1021::/pwned/iris:/bin/bash
eloise:x:1022:1022::/pwned/eloise:/bin/bash
lucia:x:1023:1023::/pwned/lucia:/bin/bash
isabel:x:1024:1024::/pwned/isabel:/bin/bash
freya:x:1025:1025::/pwned/freya:/bin/bash
alexa:x:1026:1026::/pwned/alexa:/bin/bash
ariel:x:1027:1027::/pwned/ariel:/bin/bash
lola:x:1028:1028::/pwned/lola:/bin/bash
celeste:x:1029:1029::/pwned/celeste:/bin/bash
nina:x:1030:1030::/pwned/nina:/bin/bash
kira:x:1031:1031::/pwned/kira:/bin/bash
veronica:x:1032:1032::/pwned/veronica:/bin/bash
lana:x:1033:1033::/pwned/lana:/bin/bash
noa:x:1034:1034::/pwned/noa:/bin/bash
maia:x:1035:1035::/pwned/maia:/bin/bash
gloria:x:1036:1036::/pwned/gloria:/bin/bash
alora:x:1037:1037::/pwned/alora:/bin/bash
julie:x:1038:1038::/pwned/julie:/bin/bash
irene:x:1039:1039::/pwned/irene:/bin/bash
adela:x:1040:1040::/pwned/adela:/bin/bash
sky:x:1041:1041::/pwned/sky:/bin/bash
sarah:x:1042:1042::/pwned/sarah:/bin/bash
mercy:x:1043:1043::/pwned/mercy:/bin/bash


################
# MISSION 0x15 #
################

## EN ##
Maybe sudo can help you to be natalia.

## ES ##
Puede que sudo te ayude para ser natalia.
anna@venus:~$ sudo -l
Matching Defaults entries for anna on venus:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    use_pty

User anna may run the following commands on venus:
    (natalia) NOPASSWD: /bin/bash
anna@venus:~$ /bin/bash
anna@venus:~$ (natalia) NOPASSWD: /bin/bash
bash: syntax error near unexpected token `NOPASSWD:'
anna@venus:~$ (natalia: /bin/bash
> ^C
anna@venus:~$ su
Password:
su: Authentication failure
anna@venus:~$ sudo -u natalia /bin/bash
natalia@venus:/pwned/anna$ ls
ls: cannot open directory '.': Permission denied
natalia@venus:/pwned/anna$ cd ../natalia
natalia@venus:~$ ls
base64.txt  flagz.txt  mission.txt  nataliapass.txt
natalia@venus:~$ cat nataliapass.txt
NMuc4DkYKDsmZ5z
natalia@venus:~$


################
# MISSION 0x16 #
################

## EN ##
The password of user eva is encoded in the base64.txt file

## ES ##
El password de eva esta encodeado en el fichero base64.txt
natalia@venus:~$ echo base64.txt | base64 -d
m��base64: invalid input
natalia@venus:~$ cat base64.txt
dXBzQ0EzVUZ1MTBmREFPCg==
natalia@venus:~$ base64 -d dXBzQ0EzVUZ1MTBmREFPCg==
base64: 'dXBzQ0EzVUZ1MTBmREFPCg==': No such file or directory
natalia@venus:~$ dXBzQ0EzVUZ1MTBmREFPCg== base64
^C                                                                            natalia@venus:~$ dXBzQ0EzVUZ1MTBmREFPCg== base64
^C
natalia@venus:~$ echo dXBzQ0EzVUZ1MTBmREFPCg== | base64 -d
upsCA3UFu10fDAO
natalia@venus:~$ cat flagz.txt
8===JWHa1GQq1AYrBWNXEJrH===D~~
natalia@venus:~$

################
# MISSION 0x17 #
################
                                                                              ## EN ##
The password of the clara user is found in a file modified on May 1, 1968.

## ES ##
La password de la usuaria clara se encuentra en un fichero modificado el 01 de Mayo de 1968.
eva@venus:~$ find / -type f -mtime +18980 2>/dev/null                         /usr/lib/cmdo
eva@venus:~$ cat "/usr/lib/cmdo"                                              39YziWp5gSvgQN9


################
# MISSION 0x19 #
################

## EN ##
The password of eliza is the only string that is repeated (unsorted) in repeated.txt.

## ES ##
La password de eliza es el unico string que se repite (sin estar ordenado) en repeated.txt.

para esta mision se usa el siguiente comando
```bash
uniq -d repeated.txt
Fg6b6aoksceQqB9

```
eliza@venus:~$ cat mission.txt
################
# MISSION 0x20 #
################

## EN ##
The user iris has left me her key.

## ES ##
La usuaria iris me ha dejado su key.
eliza@venus:~$ su iris
Password:
eliza@venus:~$ ls
flagz.txt  mission.txt
eliza@venus:~$ ls -la
total 36
drwxr-x--- 2 root  eliza 4096 Apr  5  2024 .
drwxr-xr-x 1 root  root  4096 Apr  5  2024 ..
-rw-r--r-- 1 eliza eliza  220 Apr 23  2023 .bash_logout
-rw-r--r-- 1 eliza eliza 3526 Apr 23  2023 .bashrc
-rw-r----- 1 root  eliza 2602 Apr  5  2024 .iris_key
-rw-r--r-- 1 eliza eliza  807 Apr 23  2023 .profile
-rw-r----- 1 root  eliza   31 Apr  5  2024 flagz.txt
-rw-r----- 1 root  eliza  143 Apr  5  2024 mission.txt

eliza@venus:~$ eval "$(ssh-agent -s)"
Agent pid 2058542
eliza@venus:~$ ssh-add ~/.iris_key
Identity added: /pwned/eliza/.iris_key (teste@deb11)
eliza@venus:~$ ssh iris@venus.hackmyvm.eu -p 500
ssh: connect to host venus.hackmyvm.eu port 500: Connection refused
eliza@venus:~$ ssh iris@venus.hackmyvm.eu -p 5000
