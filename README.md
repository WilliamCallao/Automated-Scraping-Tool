
# Proyecto de Big Data: Recolección y Limpieza de Datos

Este proyecto tiene como objetivo recolectar y limpiar datos de tres sitios web diferentes utilizando web scraping. Los datos recolectados se utilizarán para análisis y estudios de mercado en los sectores inmobiliarios y de servicios de internet.

## Sitios Objetivo
1. **LosTiempos - Sección de Inmuebles**
2. **Zillow - Sitio de Bienes Raíces**
3. **ATT - Paquetes de Internet**

## Estructura del Proyecto

```plaintext
.
├── ATT_Tarifas
│   ├── ATT_scraper.py
│   ├── Programa.py
│   └── requirements.txt
├── LosTiempos_Inmuebles
│   ├── DataCleaner.py
│   ├── requirements.txt
│   └── Scraper.py
└── Zillow_Inmuebles
    ├── requirements.txt
    └── Scraper.py
```

## Instalación

### Requisitos
- Python 3.x
- Virtualenv (opcional, pero recomendado)

### Pasos

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. Crear un entorno virtual (opcional):
   ```sh
   python -m venv env
   source env/bin/activate  # En Windows: env\Scripts\activate
   ```

3. Instalar las dependencias para cada subproyecto:
   ```sh
   cd ATT_Tarifas
   pip install -r requirements.txt
   cd ../LosTiempos_Inmuebles
   pip install -r requirements.txt
   cd ../Zillow_Inmuebles
   pip install -r requirements.txt
   ```

## Uso

### AT&T Tarifas
Para ejecutar el script de scraping de AT&T:
```sh
cd ATT_Tarifas
python ATT_scraper.py
```

### Los Tiempos Inmuebles
Para ejecutar el script de scraping de Los Tiempos:
```sh
cd LosTiempos_Inmuebles
python Scraper.py
```

Para limpiar los datos:
```sh
python DataCleaner.py
```

### Zillow Inmuebles
Para ejecutar el script de scraping de Zillow:
```sh
cd Zillow_Inmuebles
python Scraper.py
```

## Contribuciones
Si deseas contribuir a este proyecto, por favor abre un issue o envía un pull request.

## Licencia
Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.
