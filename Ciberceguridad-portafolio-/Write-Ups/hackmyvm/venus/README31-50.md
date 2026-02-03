################
# MISSION 31 #
################

## EN ##
The user veronica visits a lot http://localhost/waiting.php

## ES ##
La usuaria veronica visita mucho http://localhost/waiting.php
kira@venus:~$ curl http://localhost/waiting.php -v
*   Trying 127.0.0.1:80...
* Connected to localhost (127.0.0.1) port 80 (#0)
> GET /waiting.php HTTP/1.1
> Host: localhost
> User-Agent: curl/7.88.1
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: nginx/1.22.1
< Date: Wed, 28 Jan 2026 13:57:20 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
<

Im waiting for the user-agent PARADISE.
* Connection #0 to host localhost left intact
kira@venus:~$ curl -A "PARADISE" http://localhost/waiting.php -v
*   Trying 127.0.0.1:80...
* Connected to localhost (127.0.0.1) port 80 (#0)
> GET /waiting.php HTTP/1.1
> Host: localhost
> User-Agent: PARADISE
> Accept: */*
>
< HTTP/1.1 200 OK
< Server: nginx/1.22.1
< Date: Wed, 28 Jan 2026 13:58:48 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
<

QTOel6BodTx2cwX


################
# MISSION 0x32 #
################

## EN ##
The user veronica uses a lot the password from lana, so she created an alias.

## ES ##
La usuaria veronica usa mucho la password de lana, asi que ha creado un alias.
veronica@venus:~$ alias
alias lanapass='UWbc0zNEVVops1v'
alias ls='ls --color=auto



################
# MISSION 0x33 #
################

## EN ##
The user noa loves to compress her things.

## ES ##
A la usuaria noa le gusta comprimir sus cosas.
lana@venus:~$ ls
flagz.txt  mission.txt  zip.gz
lana@venus:~$ tar -xvf zip.gz -C /var/tmp
pwned/lana/zip
lana@venus:~$ cd /var/tmp/pwned/lana
lana@venus:/var/tmp/pwned/lana$ ls
zip
lana@venus:/var/tmp/pwned/lana$ cat zip
9WWOPoeJrq6ncvJ

################
# MISSION 0x34 #
################

## EN ##
The password of maia is surrounded by trash

## ES ##
La password de maia esta rodeada de basura

noa@venus:~$ strings trash
b;pK
*&dv
 |.-
wsG9
D55-
\|gu
1q#^
YV!)}
f}nP
T735
5GOj'
g3-5v)S~hK
{Xu7
O;rTl,
]Bokc
04`0
X:Uf
;Vtr3
`vr)
k`      I
<(;pQ
@$LiJ
u7TI
*Q{r%
;%gzDB
b%/*
3g?d
=I+"
xfFN
\nh1hnDPHpydEjoEN
!       2L~8
JmN8
@%`j
,       ^,
e&xvN2
_cKn
.c|0
)|hd&
hl(p
fEr:
OdBb
?OsP
dnN9
J7e(
JL6(
wI;%vz
apPD
a5qi
|otr
4TTm
toyi
*f|F
.%J`t
noa@venus:~$ h1hnDPHpydEjoEN #se elemina el salto de linea
-bash: h1hnDPHpydEjoEN: command not found
noa@venus:~$ su maia
Password:
maia@venus:/pwned/noa$
