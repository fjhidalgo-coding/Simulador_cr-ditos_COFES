# ...existing code...
import streamlit as st

# ----------------------------------------------------------------------------------------------------------------------
# Configuración de la página
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="Utilidades de simulación para pruebas y generación de ejemplos",
    page_icon=":material/calculate:",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ----------------------------------------------------------------------------------------------------------------------
# Estilos personalizados
# ----------------------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 250px !important;
        }

        .table-right td, .table-right th {
            text-align: right !important;
        }

        .hero-box {
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 100%);
            border-radius: 1rem;
            padding: 2rem 2rem;
            color: white;
            margin-bottom: 1.5rem;
        }

        .feature-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.8rem;
            padding: 1.2rem;
            height: 100%;
        }

        .feature-card h4 {
            margin-top: 0;
            margin-bottom: 0.5rem;
            color: #0f172a;
        }

        .feature-card p {
            margin-bottom: 0;
            color: #334155;
            line-height: 1.6;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# ----------------------------------------------------------------------------------------------------------------------
# Página de bienvenida
# ----------------------------------------------------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <h2 style="margin: 0 0 0.5rem 0;">🏦 Simulador de operaciones</h2>
        <p style="margin: 0; font-size: 1rem; line-height: 1.7;">
            Esta aplicación reúne un conjunto de herramientas para <b>simular escenarios de crédito</b>,
            <b>generar ejemplos de prueba</b> y <b>validar resultados antes de su uso real</b>.
            Aquí puedes explorar distintos casos, comparar condiciones y analizar el impacto de variables
            clave como monto, tasa, plazo y estructura de pago.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.info(
    "Utiliza la barra lateral para acceder a las funcionalidades disponibles y comenzar con el tipo de producto que necesites."
)
st.markdown("### ¿Qué puedes hacer aquí?")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="feature-card">
            <h4>📊 Simulaciones</h4>
            <p>
                Evalúa diferentes escenarios de financiación para entender cómo cambian cuota,
                intereses, plazo y saldo en función de las condiciones del crédito.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="feature-card">
            <h4>🧪 Generación de ejemplos</h4>
            <p>
                Crea casos de prueba con combinaciones típicas para apoyar análisis, validaciones
                y documentación técnica de operaciones de crédito.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="feature-card">
            <h4>✅ Validación</h4>
            <p>
                Comprueba resultados, compara supuestos y revisa que los cálculos se ajusten a la lógica
                esperada antes de aplicar decisiones o escenarios reales.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ---------------------------------------------------------------------------------------------------------------------- 