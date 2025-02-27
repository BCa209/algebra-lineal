import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Combinaciones Lineales", 
    page_icon="📚"
)
def combinaciones_lineales(vectores, coeficientes):
    vectores = np.array(vectores)
    coeficientes = np.array(coeficientes).reshape(-1, 1)
    resultado = vectores.T @ coeficientes
    return resultado.flatten()

def genera_Rn(vectores, n):
    """
    Verifica si un conjunto de vectores genera R^n.
    Retorna True si los vectores son linealmente independientes y generan R^n, False en caso contrario.
    """
    matriz = np.array(vectores).T  # Construimos la matriz con los vectores como columnas
    rango = np.linalg.matrix_rank(matriz)  # Calculamos el rango de la matriz
    
    return rango == n  # Los vectores generan R^n si el rango es igual a la dimensión

def graficar_vectores(vectores, resultado):
    dim = len(vectores[0])
    fig = go.Figure()
    colores = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']
    
    for i, v in enumerate(vectores):
        if dim == 2:
            fig.add_trace(go.Scatter(x=[0, v[0]], y=[0, v[1]], mode='lines+markers',
                                    name=f"v{i+1}",
                                    line=dict(color=colores[i % len(colores)], width=3)))
        elif dim == 3:
            fig.add_trace(go.Scatter3d(x=[0, v[0]], y=[0, v[1]], z=[0, v[2]], mode='lines+markers',
                                    name=f"v{i+1}",
                                    line=dict(color=colores[i % len(colores)], width=5)))

    # Agregar el vector resultante en color negro
    if dim == 2:
        fig.add_trace(go.Scatter(x=[0, resultado[0]], y=[0, resultado[1]], mode='lines+markers',
                                name="Resultado", line=dict(color='black', width=4, dash="dash")))
    elif dim == 3:
        fig.add_trace(go.Scatter3d(x=[0, resultado[0]], y=[0, resultado[1]], z=[0, resultado[2]], mode='lines+markers',
                                name="Resultado", line=dict(color='black', width=6, dash="dash")))

    # Ajustar el rango dinámicamente
    valores = np.array(vectores + [resultado.tolist()])
    min_val, max_val = valores.min() - 1, valores.max() + 1

    fig.update_layout(scene=dict(
        xaxis=dict(range=[min_val, max_val]),
        yaxis=dict(range=[min_val, max_val]),
        zaxis=dict(range=[min_val, max_val]) if dim == 3 else {}
    ), title="Gráfica Interactiva de Vectores", margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig)

def main():
    st.title("Combinaciones Lineales en Álgebra Lineal")
    input_text = st.text_area("Introduce los vectores separados por comas y líneas (ejemplo: '1,2' en una línea y '3,4' en otra):")
    input_coef = st.text_input("Introduce los coeficientes separados por comas (ejemplo: '0.5, 2'):")
    input_dim = st.number_input("Determina si genera R^n (ingresa n):", min_value=1, step=1)
    
    col1, col2 = st.columns(2)
    with col1:
        calcular_btn = st.button("Calcular Combinación Lineal")
    with col2:
        determinar_btn = st.button("Determinar")
    
    if calcular_btn:
        try:
            # Procesar la entrada
            lineas = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
            vectores = [list(map(float, line.split(','))) for line in lineas]
            coeficientes = list(map(float, input_coef.split(',')))
            
            # Validación de dimensiones
            dimensiones = {len(v) for v in vectores}
            if len(dimensiones) > 1:
                st.error("Error: Todos los vectores deben tener la misma cantidad de dimensiones.")
                return
            
            # Validación de número de coeficientes
            if len(coeficientes) != len(vectores):
                st.error("Error: La cantidad de coeficientes debe coincidir con la cantidad de vectores.")
                return
            
            # Calcular la combinación lineal
            resultado = combinaciones_lineales(vectores, coeficientes)
            st.write("Resultado de la combinación lineal:", resultado)
            
            # Graficar si es 2D o 3D
            if len(vectores[0]) in [2, 3]:
                graficar_vectores(vectores, resultado)
        except ValueError:
            st.error("Error: Asegúrate de que todos los valores sean números y estén correctamente separados por comas.")
        except Exception as e:
            st.error(f"Error inesperado: {e}")
    
    if determinar_btn:
        try:
            lineas = [line.strip() for line in input_text.strip().split('\n') if line.strip()]
            vectores = [list(map(float, line.split(','))) for line in lineas]
            
            if genera_Rn(vectores, input_dim):
                st.markdown(f'<div style="background-color:#0D6719;padding:10px;border-radius:5px;">Los vectores generan R^{int(input_dim)}.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color:#7F0000;padding:10px;border-radius:5px;">Los vectores NO generan R^{int(input_dim)}.</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
