# Smart Fridge

**Smart Fridge** es una aplicacion de codigo abierto diseada para gestionar y optimizar la compra de alimentos en refrigeradores comunitarios ubicados en reas de alta afluencia. A travs de la aplicacion, los usuarios pueden adquirir productos dentro del refrigerador mediante una plataforma de Ecommerce. Una vez completada la compra, el refrigerador se desbloquea, permitiendo el acceso al artculo adquirido. Utilizamos un sistema de cmaras y tecnologa de inteligencia artificial para monitorear las extracciones y garantizar que coincidan con las compras realizadas, lo que permite el debito automatico en la tarjeta del usuario por el producto retirado.


Este proyecto fue continuado por **Carla Tarifa**, **Jose Pernalete**, **Sebastian Butcovich**. El backend est desarrollado en **Django Rest Framework** y el frontend utiliza **Next.js** con **React**.

---

## Instalacion

### Requisitos previos
- Python 3.8+
- Node.js 14+
- Django Rest Framework
- Next.js

---

### Instalacion del Backend (Django Rest Framework)

1. Clonar el repositorio. Abrir una terminal y ubicarse en la raiz del proyecto para luego acceder a /Backend/ con el comando: 
	cd Backend
2. Crear un entorno virtual

Si es Linux/MacOs

    python3 -m venv venv

    source venv/bin/activate
    
Si es Windows

    python -m venv venv

    venv\Scripts\activate

3. Mover hacia rest_api e instalar dependencias

    cd /Backend/rest_api

    pip install -r requeriments.txt   

4. Crear base de datos con docker

    docker run --name some-postgres -e POSTGRES_DB=smartfridgebd -e POSTGRES_USER=smart -e POSTGRES_PASSWORD=fridge -p 5432:5432 -d postgres

5. Realizar las migraciones de la base de datos

    python manage.py migrate
    
En caso de que ocurra algún problema en la migración utilice

    py manage.py makemigrations agregando cada app (authentication, CreditCard, fridge)
    python manage.py migrate

6. Crear un superusuario para el panel de administración

    python manage.py createsuperuser
    
7. Ejecutar el servidor en Django
    
    python manage.py runserver
    
8. El servidor de Django estaría corriendo en la dirección http://localhost:8000

## Instalacion del Frontend (Next.js con React)

1. Ve al directorio del frontend:
        cd Frontend

2. Instala las dependencias de Node.js:
       npm install
3. Configura las variables de entorno: Crea un archivo .env en la raíz del proyecto con las siguientes variables:
    NEXT_PUBLIC_API_URL=http://localhost:8000/


4. Ejecuta el servidor de desarrollo de Next.js:
            npm run dev

El frontend estará corriendo en http://localhost:3000/.

## Uso

Una vez que tanto el backend como el frontend estan en funcionamiento, puedes acceder a la aplicacion desde http://localhost:3000. Si necesitas acceder al panel de administracion de Django, ve a http://localhost:8000/admin e inicia sesion con el superusuario que creaste.


## Contribucion

Este proyecto es de codigo abierto. Si quieres contribuir, por favor crea un fork del repositorio, realiza tus cambios y enva un pull request. Las contribuciones son bienvenidas.

## Licencia

Smart Fridge es un proyecto de codigo abierto bajo la licencia MIT.
