# Plantilla de proyecto

Este repositorio es una plantilla de proyecto para lanzar scripts con Docker (con o sin GPU).

## Ficheros necesarios

```
project
  ├── logs/                       # Directorio donde almacenar los logs (salida de los scripts)
  │     └── MY_SCRIPT.log
  ├── configs/                    # Directorio donde almacenar los parámetros (json)
  ├── data/                       # Directorio donde almacenar los datos
  ├── cache/                      # Directorio donde almacenar datos temporales (limpiar a menudo)
  ├── Dockerfile
  ├── docker-compose.yml
  ├── MY_SCRIPT.py
  ├── .env
  ├── README.md
  └── requirements.txt
```
- `.env` Definir las variables de entorno que sean necesarias dentro del contendor

- `Dockerfile` Genera la imagen docker para ejecutar scripts.
    1. Seleccionar la imagen base (`nvidia/cuda:11.8.0-base-ubuntu22.04`, `python:3.11-slim`, etc.).
    2. [OPCIONAL] Instalar dependencias (`python3`, `python3-pip`, etc).
    3. Seleccionar espacio de trabajo dentro del contenedor (`/home`, por ejemplo).
    4. Las dependencias python del `requirements.txt` se instalarán automáticamente dentro de la imagen.


- `docker-compose.yml` Crea un contendor a partir de la imagen y ejecuta el script en segundo plano de forma automática. Dentro de este fichero se especifican los servicios que se deseen (uno por cada script que se desee ejecutar).
    1. Poner nombre del script como nombre del servicio (`MY_SCRIPT`).
    2. Seleccionar nombre de la imagen (`MY_IMAGE`).
    3. Seleccionar nombre del contenedor (`MY_CONTAINER`).
    4. [OPCIONAL] Habilitar GPUs (aunque se habiliten se pueden no usar especificándolo desde el propio script).
    5. Cargar proyecto como volumen (`.:/home`) en el espacio de trabajo del contenedor (establecido en el paso "iii" del `Dockerfile`).
    6. Configurar el path al script y a los logs (`python3 MY_SCRIPT.py > /home/logs/MY_SCRIPT.log 2>&1`).

- `MY_SCRIPT.py` Código python a ejecutar.

- `requirements.txt` Dependencias python necesarias.

## Ejemplo de uso:

Ejecutar todos los comandos desde el path del proyecto (`cd project/`).

### Crear imagen con las dependencias necesarias:
   ```
   docker build -t MY_IMAGE .
   ```
- Elegir el nombre de la imagen (`MY_IMAGE`).
- Puede tardar varios minutos según el número de dependencias y el peso la imagen base.
- Tras crearla se verá al ejecutar: `docker images`.
- Eliminar la imagen al finalizar el proyecto: `docker rmi <IMAGE_ID>` (puede ocupar muchos GB).
       
### Ejecutar script:

#### Opción 1: El contenedor no se elimina tras la ejecución
   ```
   docker compose up -d MY_SCRIPT
   ```
- Elegir el nombre del servicio (establecido en el paso "i" del `docker-compose.yml`).
- El script se ejecutará en segundo plano.
- El contenedor se eliminará automáticamente al detenerlo.
- Para comprobar si el contenedor sigue en pie: `docker ps`.
- El contenedor NO se detendrá al terminar la ejecución.

#### Opción 2 (recomendado): El contenedor se elimina tras la ejecución
   ```
   docker compose run --rm -d MY_SCRIPT
   ```
   o
   ```
   docker compose run --rm MY_SCRIPT &
   ```
- Elegir el nombre del servicio (establecido en el paso "i" del `docker-compose.yml`).
- El script se ejecutará en segundo plano.
- El contenedor se eliminará automáticamente al detenerlo.
- Para comprobar si el contenedor sigue en pie: `docker ps`.
- El contenedor se detendrá al terminar la ejecución (es posible que esto no suceda en caso de error en el script).
  

### Ver logs de la ejecución en directo:
   ```
   tail -f logs/MY_SCRIPT.log
   ```
- Seleccionar nombre del fichero .log

### Ver logs del contenedor:
   ```
   docker logs <CONTAINER_ID>
   ```

### Detener ejecución:
   ```
   docker compose down -d MY_SCRIPT
   ```

### Borrar contenedor manualmente

Si la ejecución se para y el contenedor no se elimina, detener manualmente.

#### 1. Consultar ID del contenedor:
   ```
   docker ps -a
   ```
#### 2. Detener contendor:
   ```
   docker rm <CONTAINER_ID>
   ```

### Extra

Los ficheros/directorios generados durante la ejecución tienen propietario `root`, por lo que no se podrá modificar desde fuera del contenedor.

Para poder modificarlo o eliminarlo se hará desde dentro del contenedor.

#### Crear un contenedor y entrar para lanzar comandos:
   ```
   docker run --name MY_CONTAINER -v ${PWD}:/home -w /home --rm -it MY_IMAGE /bin/bash
   ```
- Elegir nombre del contenedor a generar y de la imagen generada.
- Se abrirá una terminal iteractiva para poder ejecutar comandos bash dentro del contenedor.
- El contenedor se eliminará tras abandonarlo con el comando `exit`.

