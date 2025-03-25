# Gestion de Eventos API

## Descripción
La **Gestion de Eventos API** es una aplicación desarrollada con Django REST Framework (DRF) que permite la gestión integral de eventos. La API incluye:
- **Autenticación basada en tokens** mediante TokenAuthentication.
- **Documentación interactiva** generada con Swagger.
- CRUD completo para la gestión de eventos.
- Sistema de registro y cancelación de asistencia a eventos.
- CRUD para la gestión de comentarios en eventos.
- Sistema de calificación de eventos.
- Gestión del perfil de usuario con opciones para actualizar y eliminar el perfil.

## Requisitos del sistema
- **Python 3.11.4**
- **Django 5.0.6**
- **Django REST Framework 3.15.1**
- **PostgreSQL** (la configuración de la base de datos debe realizarse en el archivo `settings.py` en la sección `DATABASES`, especificando la URL de tu base de datos)

## Instalación
1. Clona el repositorio del proyecto:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_PROYECTO>
   ```
2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Linux/MacOS
   .\venv\Scripts\activate    # En Windows
   ```
3. Instala las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```
4. Realiza las migraciones para configurar la base de datos:
   ```bash
   python manage.py migrate
   ```
5. Crea un superusuario (opcional, para acceder al panel de administración):
   ```bash
   python manage.py createsuperuser
   ```
6. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Uso de la API
### Autenticación
- El sistema utiliza **TokenAuthentication**. Para obtener un token, inicia sesión en la ruta correspondiente (`/user/login/`).
- En cada solicitud protegida, deberás incluir el token en el encabezado:
  ```http
  Authorization: Token <tu_token>
  ```

### Endpoints
#### **Eventos**
- **`POST /events/`** - Crear un evento.
- **`GET /events/`** - Listar todos los eventos.
- **`GET /events/<int:event_id>/`** - Consultar detalles de un evento.
- **`PUT /events/<int:event_id>/`** - Actualizar un evento.
- **`DELETE /events/<int:event_id>/`** - Eliminar un evento.
- **`POST /events/<int:event_id>/register/`** - Registrarse en un evento.
- **`DELETE /events/<int:event_id>/register/`** - Cancelar la inscripción a un evento.
- **`POST /events/<int:event_id>/comments/`** - Crear un comentario en un evento.
- **`GET /events/<int:event_id>/comments/`** - Listar comentarios de un evento.
- **`PUT /events/<int:event_id>/comments/<int:comment_id>/`** - Actualizar un comentario.
- **`DELETE /events/<int:event_id>/comments/<int:comment_id>/`** - Eliminar un comentario.
- **`POST /events/<int:event_id>/ratings/`** - Calificar un evento.
- **`PUT /events/<int:event_id>/ratings/<int:rating_id>/`** - Actualizar una calificación.

#### **Usuarios**
- **`POST /user/register/`** - Registrar un nuevo usuario.
- **`POST /user/login/`** - Iniciar sesión y obtener un token.
- **`POST /user/logout/`** - Cerrar sesión y revocar el token.
- **`GET /user/profile/`** - Consultar el perfil del usuario.
- **`PUT /user/profile/`** - Actualizar el perfil del usuario.
- **`DELETE /user/profile/`** - Eliminar el perfil del usuario.
- **`GET /user/profile/registrations/`** - Listar los eventos a los que está registrado el usuario.
- **`GET /users/`** - Listar todos los usuarios (solo para administradores).

## Estructura del Proyecto
El proyecto está organizado en tres carpetas principales:
- **`core/`**: Contiene la configuración general del proyecto, incluyendo el archivo `settings.py` y las rutas principales (`urls.py`).
- **`events/`**: Incluye los modelos, vistas, serializadores, rutas y configuraciones relacionadas con la gestión de eventos.
- **`users/`**: Similar a la carpeta `events`, pero enfocada en la gestión de usuarios.

## Autor
**Joel Rázuri**  
Estudiante de **Licenciatura en Informática** y desarrollador backend.   
**Linkedin:** [https://www.linkedin.com/in/joelrazuri/](#)





