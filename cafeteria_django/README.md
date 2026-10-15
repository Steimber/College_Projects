# Cafetería en Django (Apps: `servicios` y `blog`)

Proyecto universitario desarrollado en **Python + Django**, optimizado para la cuenta gratuita de **PythonAnywhere** (sin dependencias pesadas, uso mínimo de disco y CPU, base de datos SQLite lista).

## Características cumplidas
1. **Dos aplicaciones separadas**:
   - `servicios`: Catálogo de productos de la cafetería (`Servicio`) + **Pasarela Simple de Pedidos** (`Pedido` y `DetallePedido`) donde el cliente elige cantidades, modalidad y método de pago, guardándose en la base de datos.
   - `blog`: Publicaciones (`Post`) filtrables por categorías (`Categoria`: *Ofertas*, *Promociones 2x1*, *Novedades y Menú*).
2. **Auditoría `created` y `updated` con fecha y hora**:
   - Todos los modelos (`Servicio`, `Pedido`, `DetallePedido`, `Categoria`, `Post`) tienen `created = models.DateTimeField(auto_now_add=True)` y `updated = models.DateTimeField(auto_now=True)`.
3. **Botón en el Header `Modificar Página (Admin)`**:
   - Permite ver los pedidos que llegan de la pasarela, cambiar su estado, crear/modificar/eliminar productos y publicar nuevas ofertas en el blog directamente desde la web, además de enlazar a `/admin/` (`admin` / `admin1234`).

---

## Cómo ejecutar en local
```bash
.\.venv\Scripts\python manage.py runserver
```
Abre `http://127.0.0.1:8000/` en el navegador.

---

## Cómo subir a PythonAnywhere (Versión Gratis)

1. Sube esta carpeta a GitHub (o comprímela en `.zip` y súbela desde la pestaña **Files** de PythonAnywhere).
2. En la consola **Bash** de PythonAnywhere ejecuta:
```bash
mkvirtualenv --python=/usr/bin/python3.10 venv
pip install Django
cd ~/cafeteria_django
python manage.py migrate
python seed.py
python manage.py collectstatic --noinput
```
3. En la pestaña **Web** de PythonAnywhere:
   - Crea una nueva Web App -> **Manual configuration** -> **Python 3.10**.
   - En **Virtualenv**, pon: `/home/TU_USUARIO/.virtualenvs/venv`
   - En **Static files**, agrega:
     - URL: `/static/` -> Directory: `/home/TU_USUARIO/cafeteria_django/staticfiles`
   - Abre el **WSGI configuration file** y deja únicamente:
```python
import os
import sys

path = '/home/TU_USUARIO/cafeteria_django'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'cafeteria_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```
4. Haz clic en el botón verde **Reload** y listo.
