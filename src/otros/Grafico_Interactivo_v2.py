import streamlit as st
import pandas as pd
import io

from xlsxwriter import Workbook


# Configuración general
st.set_page_config(page_title="Eventos Relevantes", layout="wide")

# Reducir espacio superior con CSS
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Logo e encabezado
st.markdown("""
<div style='text-align: center;'>
    <h1>📄 Eventos Relevantes</h1>
    <h4 style='color: gray;'>Sistema de consulta de avisos corporativos con filtros dinámicos</h4>
</div>
""", unsafe_allow_html=True)

# Imagen corporativa
st.image("https://www.tda-sgft.com/TdaWeb/images/logotipo.gif", width=150)

# Cargar datos
df = pd.read_excel(
    "C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\HISTORICO_EMISORES_DATA_v2.xlsx",
    sheet_name="HIST"
)
df['FECHA'] = pd.to_datetime(df['FECHA'])

# SIDEBAR
with st.sidebar:
    st.header("🔎 Filtros")

    claves = st.multiselect(
        "CLAVE",
        options=sorted(df['CLAVE'].dropna().unique()),
        default=[]
    )

    fechas = st.date_input("Rango de FECHAS", [])

    origenes = st.multiselect(
        "ORIGEN",
        options=sorted(df['ORIGEN'].dropna().unique()),
        default=sorted(df['ORIGEN'].dropna().unique())
    )

    t_valores = st.multiselect(
        "T",
        options=sorted(df['T'].dropna().unique()),
        default=sorted(df['T'].dropna().unique())
    )

    filtro_valores = st.multiselect(
        "FILTRO",
        options=sorted(df['FILTRO'].dropna().unique()),
        default=sorted(df['FILTRO'].dropna().unique())
    )

    st.markdown("---")
    st.markdown("### ℹ️ Instrucciones")
    st.markdown("""
    - Selecciona una o más claves para comenzar.
    - Filtra por fecha u otros campos si lo necesitas.
    - Haz clic en 📎 para ver el documento o detalle.
    """)

# Mostrar resultados solo si hay CLAVES seleccionadas
if claves:
    df_filtrado = df[df['CLAVE'].isin(claves)]

    if fechas:
        if len(fechas) == 1:
            df_filtrado = df_filtrado[df_filtrado['FECHA'].dt.date == fechas[0]]
        elif len(fechas) == 2:
            df_filtrado = df_filtrado[
                (df_filtrado['FECHA'].dt.date >= fechas[0]) &
                (df_filtrado['FECHA'].dt.date <= fechas[1])
            ]

    df_filtrado = df_filtrado[
        df_filtrado['ORIGEN'].isin(origenes) &
        df_filtrado['T'].isin(t_valores) &
        df_filtrado['FILTRO'].isin(filtro_valores)
    ]


    df_mostrar = df_filtrado.copy()

    st.markdown("### 📋 Resultados")
    st.write(f"Se encontraron **{len(df_mostrar)}** registros filtrados.")

    # Tabla interactiva con st.dataframe
    st.dataframe(
        df_mostrar[['FECHA', 'CLAVE', 'SECCION', 'ASUNTO', 'ARCHIVO', 'URL']]
        .sort_values(by="FECHA", ascending=False),
        use_container_width=True
    )

    # Botón de descarga CSV
    def to_csv(dataframe):
        return dataframe.to_csv(index=False).encode('utf-8')

    # Botón de descarga Excel
    def to_excel(dataframe):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Avisos')
        return output.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Descargar CSV",
            data=to_csv(df_filtrado),
            file_name="avisos_filtrados.csv",
            mime="text/csv"
        )
    with col2:
        st.download_button(
            label="📥 Descargar Excel",
            data=to_excel(df_filtrado),
            file_name="avisos_filtrados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    st.info("👈 Selecciona al menos una CLAVE para ver resultados.")

# PIE DE PÁGINA
st.markdown("""
<hr>
<div style='text-align: center; font-size: 13px; color: gray;'>
    Herramienta desarrollado por <strong>Steve Carpio - Python Streamlit</strong><br>
    Contacto: <a href="mailto:carpios@tda-sgft.com">carpios@tda-sgft.com</a><br>
    ⚠️ Solo para uso interno - No difundir fuera de la organización.
</div>
""", unsafe_allow_html=True)
