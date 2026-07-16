# Colombia Election Analysis 2018

Análisis exploratorio y territorial de la primera vuelta de las elecciones presidenciales de Colombia de 2018.

## Contenido

- Limpieza y clasificación de registros.
- Resultados nacionales y porcentajes.
- Análisis por departamento y municipio.
- Márgenes de victoria.
- Detección exploratoria de valores atípicos.
- Exportación de tablas y visualizaciones.
- Dashboard interactivo con Streamlit.

## Estructura

```text
colombia-election-analysis-2018/
├── data/
│   ├── 2018_presidencia_primera_vuelta.dta.csv
│   └── processed/
├── dashboard/
│   └── app.py
├── images/
├── notebooks/
│   └── analisis_electoral_2018.ipynb
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

1. Abra y ejecute todo el notebook.
2. Después ejecute el dashboard desde la raiz:

```bash
streamlit run dashboard/app.py
```

## Advertencia

Los valores atípicos identificados por métodos estadísticos son señales exploratorias. No constituyen evidencia de fraude ni de irregularidad electoral.
