# Taller de Motos - API

Esta es una API desarrollada con Django y Django REST Framework para gestionar servicios en un taller de motos.

## Instalación

1. Clonar el repositorio:

   ```
   git clone
   
   ```

2. Crear y activar un entorno virtual:

   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows usar: venv\Scripts\activate
   ```

3. Instalar las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

4. Aplicar migraciones:

   ```sh
   python manage.py migrate
   ```

5. Crear un superusuario (opcional para acceso al panel de administración):

   ```sh
   python manage.py createsuperuser
   ```

6. Ejecutar el servidor:

   ```sh
   python manage.py runserver
   ```

## Endpoints principales

La API expone los siguientes endpoints principales:

- **Servicios** (`/api/servicios/`)
  - `GET /api/servicios/` - Obtener la lista de servicios
  - `POST /api/servicios/` - Crear un nuevo servicio
  - `GET /api/servicios/{id}/` - Obtener detalles de un servicio
  - `PUT /api/servicios/{id}/` - Actualizar un servicio
  - `DELETE /api/servicios/{id}/` - Eliminar un servicio

## Notas

- Asegúrate de que el servidor esté en ejecución antes de realizar peticiones.
- Puedes probar la API con ThunderClient.

##

