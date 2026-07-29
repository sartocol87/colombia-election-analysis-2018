# Análisis de las elecciones presidenciales de Colombia de 2018

Proyecto de análisis exploratorio y territorial de los resultados de la primera vuelta presidencial de Colombia de 2018.

## Objetivo

Analizar la distribución de los votos por candidato, departamento y municipio, identificar territorios competitivos y examinar concentraciones elevadas del voto sin atribuirles causas que no puedan demostrarse con el conjunto de datos.

## Estructura del proyecto

```text
analisis-elecciones-colombia-2018/
│
├── data/
│   ├── raw/               Datos originales sin modificar
│   └── processed/         Tablas generadas por el análisis
│
├── notebooks/
│   └── analisis_electoral_2018.ipynb
│
├── dashboard/
│   ├── streamlit/         Aplicación interactiva
│   └── powerbi/           Dashboard de Power BI
│
├── reports/
│   └── figures/           Gráficas exportadas
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Tecnologías

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Streamlit
- Power BI

## Ejecución

### 1. Crear y activar el entorno virtual

En PowerShell:

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### 2. Instalar las dependencias

```powershell
pip install -r requirements.txt
```

### 3. Ejecutar el análisis

Abrir en VS Code o Jupyter el archivo:

```text
notebooks/analisis_electoral_2018.ipynb
```

Ejecutar todas las celdas desde el inicio.

El notebook:

- carga los datos desde `data/raw/`;
- guarda las tablas procesadas en `data/processed/`;
- exporta las gráficas a `reports/figures/`.

### 4. Ejecutar el dashboard de Streamlit

Después de ejecutar el notebook y generar las tablas procesadas:

```powershell
streamlit run dashboard/streamlit/app.py
```

## Alcance metodológico

Los resultados muestran patrones descriptivos de votación. Una concentración elevada del voto en un candidato no constituye por sí sola evidencia de una irregularidad electoral.

El conjunto de datos no incluye el potencial electoral municipal. Por esta razón, no permite calcular correctamente la tasa de participación ni identificar municipios donde votó menos del 25 % del censo electoral.

Las conclusiones del proyecto se limitan a los patrones observados en los resultados electorales disponibles.

## Fuente de datos

Datos obtenidos del Centro de Estudios en Democracia y Asuntos Electorales — CEDAE:

https://cedae.datasketch.co/

Archivo utilizado:

```text
data/raw/2018_presidencia_primera_vuelta.dta.csv
```


## Dashboard interactivo en Streamlit

La aplicación permite consultar los resultados nacionales y explorar la información por departamento, municipio y ciudades principales.

![Dashboard de Streamlit](reports/figures/dashboard_streamlit.png)