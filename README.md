# Simulador de cadenas de Markov

Aplicación Streamlit para definir transiciones entre estados, generar una trayectoria aleatoria y comparar las frecuencias observadas con la distribución estacionaria.

## Funciones

- Edita los pesos de transición entre Sol, Nublado y Lluvia.
- Normaliza cada fila para convertir los pesos en probabilidades.
- Simula hasta 20 000 transiciones con una semilla reproducible.
- Grafica la trayectoria y compara frecuencia empírica con distribución estacionaria.

## Estructura

```text
.
├── backend.py       # Cadena, normalización y simulación
├── frontend.py      # Interfaz Streamlit
├── requirements.txt
└── README.md
```

## Instalación y ejecución

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run frontend.py
```

En macOS o Linux, usa `source .venv/bin/activate` para activar el entorno virtual.

## Uso

1. Edita cada fila de la tabla de transición. Los valores pueden ser probabilidades o pesos relativos.
2. Selecciona el estado inicial, el número de transiciones y la semilla.
3. Compara la frecuencia de la trayectoria con la distribución estacionaria.

La distribución estacionaria se estima por iteración de potencia. En cadenas no ergódicas, el resultado puede depender de la distribución inicial usada para ese cálculo.
