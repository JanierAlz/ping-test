# Requirements

Python 3.11.0 es requerido para iniciar este proyecto.

# Project execution

Para ejecutar el proyecto, primero debes crear un entorno virtual de python, si no tienes virtualenv instalado ejecuta el siguiente comando:
```shell
$ pip install virtualenv
```

Luego ejecuta el comando:
```shell
$ python -m venv venv
```

Luego de activar el entorno virtual, ejecuta el siguiente comando para instalar las dependencias:
```shell
$ pip install -r requirements.txt
```

Por ultimo, para iniciar el proyecto, ejecuta el comando:
 ```shell
$ flask --app flaskr run
```

# Docker

De manera alternativa, se puede ejecutar el proyecto utilizando docker, en la raiz del proyecto ejecutar el comando:

 ```shell
$ docker compose -p <app_name> up -d
```
donde app_name, es el nombre que le quieras dar al container


Una vez iniciado el proyecto, dirigete a la url ```http://localhost:5000```
