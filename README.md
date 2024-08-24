# Proyecto Django - Desarrollo con Docker

Este es el README para un proyecto Django en desarrollo utilizando Docker. Aquí encontrarás las instrucciones necesarias para configurar y ejecutar el entorno de desarrollo.

## Estructura del Proyecto

```bash
.
├── apps/
├── jelly_backend/
│   ├── celelery/
│   ├── docs/
│   ├── one_signal/
├── nginx/
├── staticfiles/
├── .Dockerignore
├── .env
├── .gitignore
├── CACHE.md
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
└── robots.txt
```

## Tecnologías Utilizadas

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryproject.org/en/stable/)
- [Redis](https://redis.io/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Nginx](https://www.nginx.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Swagger](https://swagger.io/)
- [OneSignal](https://onesignal.com/)

## Requisitos Previos

Asegúrate de tener instalados los siguientes programas:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuración del Entorno de Desarrollo

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/tu_proyecto.git
   cd tu_proyecto

2. **Crear un archivo .env en el directorio raíz del proyecto y añadir las siguientes variables de entorno:**

   ```bash
   DJANGO_ENV=development
    SECRET_KEY=tu_clave_secreta
    DATABASE_URL_DEV=postgres://usuario:contraseña@localhost:5432/tu_base_de_datos
    REDIS_URL_DEV=redis://localhost:6379
    RABBITMQ_DEFAULT_USER_DEV=tu_usuario
    RABBITMQ_DEFAULT_PASS_DEV=tu_contraseña
    CELERY_BROKER_URL_DEV=amqp://tu_usuario:tu_contraseña@localhost:5672/

3. **Construir y levantar los servicios:**

   ```bash
   docker-compose up --build

4. **Ejecutar las migraciones:**

   ```bash
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate

5. **El proyecto estará disponible en la dirección http://localhost:8000/**

6. **El proyecto posee swagger para la documentación de la API, la cual estará disponible en la dirección http://localhost:8000/swagger/**

7. **Detener los servicios:**

   ```bash
   docker-compose down

8. **Volver a levantar los servicios:**

   ```bash
   docker-compose up