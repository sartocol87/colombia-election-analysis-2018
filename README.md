# Colombia Election Analysis 2018

Análisis exploratorio y territorial de la primera vuelta de las elecciones presidenciales de Colombia de 2018.

## Contenido

- limpieza y clasificación de registros;
- resultados nacionales y porcentajes;
- análisis por departamento y municipio;
- márgenes de victoria;
- detección exploratoria de valores atípicos;
- exportación de tablas y visualizaciones;
- dashboard interactivo con Streamlit.

## Estructura

```text
colombia-election-analysis-2018-completo/
├── data/
│   ├── 2018_presidencia_primera_vuelta.dta.csv
│   └── processed/
├── dashboard/
│   └── app.py
├── images/
├── notebooks/
│   └── 02_analisis_electoral_completo.ipynb
├── .gitignore
├── README.md
└── requirements.txt
```

## Instalación

```bash
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

1. Abra y ejecute el notebook.
2. Después ejecute el dashboard:

```bash
streamlit run dashboard/app.py
```

## Advertencia

Los valores atípicos identificados por métodos estadísticos son señales exploratorias. No constituyen evidencia de fraude ni de irregularidad electoral.
