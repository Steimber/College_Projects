# Miniproyecto Geant4: Lluvias de Partículas Atmosféricas

Este repositorio contiene la configuración en Docker y el código fuente en C++ para simular la producción y propagación de lluvias de partículas atmosféricas generadas por rayos cósmicos utilizando Geant4.

# 1. Descargar desde Docker Hub
La imagen Docker ya incluye Geant4 instalado, el entorno configurado y el código fuente. Para descargar la imagen pública, ejecuta el siguiente comando:
```bash
docker pull ivannacasanova/imagen-geant4:latest
```
# 2. Cómo CONSTRUIR el proyecto
Para construir la imagen Docker de manera local utilizando los archivos del repositorio, abre una terminal en la carpeta raíz del proyecto donde se encuentra el archivo Dockerfile y ejecuta el siguiente comando:
```bash
docker build -t ivannacasanova/imagen-geant4:latest .
```
# 3. Cómo EJECUTAR el contenedor
Para iniciar el contenedor y habilitar el entorno gráfico (X11) necesario para visualizar la geometría y las trayectorias de las partículas, ejecuta:
```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0.0 -v /tmp/.X11-unix:/tmp/.X11-unix ivannacasanova/imagen-geant4:latest
```
# 4. Cómo UTILIZAR el proyecto
Una vez dentro del directorio /geant4lab del contenedor, sigue estos pasos para correr la simulación de lluvias cósmicas:
# A. Compilar el código fuente:
Utiliza el script global personalizado configurado en el entorno para compilar el proyecto:
```bash
cd proyecto_lluvias_cosmicas
```
```bash
geant4make.sh
```
# B. Iniciar la simulación:
```bash
cd build
```
```bash
./sim
```
# C. Interacción y Visualización:
Al ejecutarse el programa, se abrirá la interfaz gráfica 3D. En la barra de comandos de la interfaz, ingresa lo siguiente para disparar partículas primarias (rayos cósmicos) hacia la atmósfera:
```bash
/run/beamOn 10
```
Esto generará la cascada de partículas secundarias y mostrará en la terminal los resultados registrados por el detector sensible a nivel del suelo.
