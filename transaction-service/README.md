# Transaction service (API REST & Event-Driven)

Este proyecto se compone de un microservicio REST API(sanic server) diseñado para la creacion de transacciones de dinero. 
Estas transacciones seran dirigidas a un servicio adicional (worker) donde se finalizara la transaccion, actualizando las cuentas de los usuarios involucrados en el mismo. 

La idea consiste en que estos servicios se comuniquen mediante una cola de mensajeria (RabbitMQ), generando eventos de transacciones asincronas.

Tambien se usara mongodb para almacenar los datos de las transacciones.

## Stack Tecnologico

* REST API
* Event-Driven
* RabbitMQ
* MongoDB
* Sanic (python)
* Mongoengine (python)
* Pika (python)
* Docker

## Requisitos

* [Python ^3.10](https://www.python.org/downloads/)
* [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)


## Instalacion

1. Clonar el proyecto de gitlab mediante SSH o HTTP:

   ```
   git clone git@gitlab.com:tach-arg/challenge-python-sanic.git 
   ```
   ```
   git clone https://gitlab.com/tach-arg/challenge-python-sanic.git
   ```
2. Una vez clonado el repositorio con el codigo, dirigase a transaction-service/ dentro del directorio del proyecto:
    ```
    cd challenge-python-sanic/transaction-service
    ```
3. Instalacion de las dependencies con poetry:

    ```
    poetry install
    ```

## Ejecutar Test:
   * Ejecucion simple
      ```
      poetry run pytest tests
      ```
   * Ejecucion con reporte html
      ```
      poetry run pytest --html=report.html --self-contained-html tests
      ```

## Ejecutar Servicios

* En el directorio de `transaction-service/` ejecute el comando de docker compose:
   ```
   docker compose up
   ```
   Si es la primera vez que lo ejecuta, docker compose creara las imagenes para los contenedores,
   una vez contruidas las imagenes ejecutara los servicios.


* Si usted necesita actualizar las imagenes docker de los servicios puede utilizar el siguiente comando:
   ```
   docker compose build
   ```
   Los servicios estan sincronizados con el codigo, por lo que si realiza algun cambio deberia 
   reflejarse en los servicios que estan ejecutandose.


* Para detener los servicios puede ejecutar el siguiente comando:
   ```
   docker compose stop
   ```
   
* Si desea limpiar todos los datos guardados en MongoDB puede eliminar los volumenes de docker:
   ```
   docker compose down -v
   ```

***Puedes ver la configuracion de la ejecucion docker en el archivo `docker-compose.yml`.***
***Tambien puedes revisar todos los comandos disponibles de [docker compose](https://docs.docker.com/compose/reference/).***

