# Inmuebles Scraper

Este proyecto es un scraper de anuncios de inmuebles que extrae información de la página clasificados de Los Tiempos. Guarda los anuncios en un archivo `.pickle` para un fácil acceso y manipulación de datos posteriormente. Este scraper está diseñado para ejecutarse periódicamente, identificando y almacenando solo los nuevos anuncios desde la última ejecución.

Además, incluye un visualizador para mostrar de manera amigable los anuncios capturados directamente desde la consola. Esto facilita la revisión rápida de los nuevos anuncios sin necesidad de acceder directamente al archivo `.pickle`.

## Prerrequisitos

Antes de comenzar, asegúrate de tener Python instalado en tu sistema. Este proyecto ha sido probado con Python 3.8+.

## Configuración del entorno

Primero, clona este repositorio en tu máquina local:

```bash
git clone https://github.com/tu-usuario/inmuebles-scraper.git
cd inmuebles-scraper
```

Luego, instala las dependencias necesarias:

```bash
pip install requests beautifulsoup4
```

## Ejecución del Scraper

Para iniciar el scraper y extraer los anuncios, simplemente ejecuta:

```bash
python scraper.py
```

## Uso del Visualizador

Para visualizar los anuncios almacenados en el archivo `.pickle`, ejecuta:

```bash
python visualizer.py
```

Este comando imprimirá los anuncios capturados en la consola, incluyendo detalles como el título, fecha, descripción, y más.
