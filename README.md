# Gestion-de-Eventos-DRF

REQUERIMIENTOS

Tabla 1: Funcionalidades de Usuario
ID	Requerimiento	Descripción	Endpoint	Método HTTP	Estado
U1	Registro de usuario	Crear una cuenta nueva.	/api/user/register/	POST	✅ Implementado
U2	Iniciar sesión	Obtener token de autenticación.	/api/user/login/	POST	✅ Implementado
U3	Cerrar sesión	Invalidar token de autenticación.	/api/user/logout/	POST	✅ Implementado
U4	Ver perfil de usuario	Obtener datos del usuario autenticado.	/api/user/profile/	GET	✅ Implementado
U5	Ver eventos registrados	Listar eventos en los que el usuario se ha inscrito.	/api/user/profile/registrations/	GET	✅ Implementado
U6	Actualizar perfil*	Modificar datos del usuario (ej: nombre, email).	No implementado	PUT/PATCH	❌ Pendiente
U7	Eliminar cuenta*	Eliminar la cuenta del usuario.	No implementado	DELETE	❌ Pendiente
U8	Listar todos los usuarios*	Administradores pueden ver todos los usuarios.	No implementado	GET	❌ Pendiente

Tabla 2: Funcionalidades de Eventos
ID	Requerimiento	Descripción	Endpoint	Método HTTP	Estado
E1	Crear evento	Crear un nuevo evento (requiere autenticación).	/api/events/	POST	✅ Implementado
E2	Listar eventos	Obtener lista de eventos (con posibles filtros).	/api/events/	GET	✅ Implementado
E3	Detalles de evento	Ver información completa de un evento.	/api/events/<int:event_id>/	GET	✅ Implementado
E4	Actualizar evento	Modificar un evento (solo creador o administrador).	/api/events/<int:event_id>/	PUT	✅ Implementado
E5	Eliminar evento	Borrar un evento (solo creador o administrador).	/api/events/<int:event_id>/	DELETE	✅ Implementado
E6	Registrarse en evento	Unirse a un evento.	/api/events/<int:event_id>/register/	GET*	✅ Implementado*
E7	Cancelar registro en evento	Abandonar un evento.	/api/events/<int:event_id>/register/	DELETE	✅ Implementado
E8	Crear comentario	Añadir un comentario a un evento.	/api/events/<int:event_id>/comments/	POST	✅ Implementado
E9	Listar comentarios	Ver todos los comentarios de un evento.	/api/events/<int:event_id>/comments/	GET	✅ Implementado
E10	Gestionar comentario	Editar o eliminar un comentario (solo autor o administrador).	/api/events/<int:event_id>/comments/<int:comment_id>/	PUT, DELETE	✅ Implementado
E11	Crear puntuación	Añadir una valoración al evento (ej: 1-5 estrellas).	/api/events/<int:event_id>/ratings/	POST	✅ Implementado
E12	Ver puntuaciones	Listar todas las valoraciones del evento.	/api/events/<int:event_id>/ratings/	GET	✅ Implementado
E13	Actualizar puntuación*	Modificar una valoración existente.	No implementado	PUT	❌ Pendiente