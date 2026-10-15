FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema y GUI (X11/Qt/OpenGL)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    libx11-dev \
    libxmu-dev \
    libexpat1-dev \
    libxerces-c-dev \
    && rm -rf /var/lib/apt/lists/*

# Descargar y compilar Geant4
WORKDIR /opt/geant4_install
RUN wget https://geant4-data.web.cern.ch/releases/geant4-v11.2.1.tar.gz && \
    tar -xzf geant4-v11.2.1.tar.gz && \
    mkdir build && cd build && \
    cmake -DGEANT4_INSTALL_DATA=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_QT=ON -DCMAKE_INSTALL_PREFIX=/usr/local/geant4 ../geant4-v11.2.1 && \
    make -j$(nproc) && make install && \
    rm -rf /opt/geant4_install

# Configurar entorno de Geant4
ENV PATH="/usr/local/geant4/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/geant4/lib:${LD_LIBRARY_PATH}"
RUN echo "source /usr/local/geant4/bin/geant4.sh" >> ~/.bashrc

# Configurar el laboratorio y copiar los archivos del proyecto
WORKDIR /geant4lab
COPY geant4make.sh /usr/local/bin/geant4make.sh
RUN chmod +x /usr/local/bin/geant4make.sh
COPY proyecto_lluvias_cosmicas /geant4lab/proyecto_lluvias_cosmicas

# Configurar variables de entorno X11 para la interfaz gráfica
ENV DISPLAY=host.docker.internal:0.0

CMD ["/bin/bash"]
