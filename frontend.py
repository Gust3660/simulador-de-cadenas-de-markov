"""Interfaz Streamlit para simular una cadena de Markov finita."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from backend import normalize_transition, simulate_chain


st.set_page_config(page_title="Cadenas de Markov", page_icon="🔁", layout="wide")
st.title("Simulador de cadenas de Markov")
st.write("Edita los pesos de transición, ejecuta una trayectoria y compara su frecuencia con la distribución estacionaria.")

states = ["Sol", "Nublado", "Lluvia"]
default_matrix = [[0.65, 0.25, 0.10], [0.30, 0.45, 0.25], [0.20, 0.35, 0.45]]
matrix_frame = pd.DataFrame(default_matrix, columns=states)
matrix_frame.insert(0, "Desde", states)
st.subheader("Pesos de transición")
edited = st.data_editor(
    matrix_frame,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Desde": st.column_config.TextColumn(disabled=True),
        **{state: st.column_config.NumberColumn(min_value=0.0, step=0.05) for state in states},
    },
)

with st.sidebar:
    st.header("Simulación")
    initial_label = st.selectbox("Estado inicial", states)
    steps = st.slider("Transiciones", min_value=10, max_value=20000, value=2000, step=10)
    seed = st.number_input("Semilla aleatoria", min_value=0, value=42, step=1)

try:
    transition = normalize_transition(edited[states].to_numpy())
    initial_state = states.index(initial_label)
    result = simulate_chain(transition, steps, initial_state, int(seed))
except ValueError as error:
    st.error(str(error))
    st.stop()

left, right = st.columns([1, 2])
with left:
    st.subheader("Distribución de estados")
    comparison = pd.DataFrame(
        {
            "Estado": states,
            "Frecuencia simulada": result.empirical_probabilities,
            "Estacionaria": result.stationary_probabilities,
        }
    ).set_index("Estado")
    st.bar_chart(comparison)
    st.caption("La matriz se normaliza por fila; los valores editados pueden ser pesos relativos.")
with right:
    st.subheader("Trayectoria")
    interval = max(1, len(result.states) // 2000)
    trajectory = pd.DataFrame(
        {"Paso": range(0, len(result.states), interval),
         "Índice del estado": result.states[::interval]}
    ).set_index("Paso")
    st.line_chart(trajectory)
    st.caption("Índices: 0 = Sol, 1 = Nublado, 2 = Lluvia.")
    st.dataframe(
        pd.DataFrame(result.transition_matrix, index=states, columns=states),
        use_container_width=True,
    )
