import streamlit as st
import pandas as pd
import io

# Configuración general
st.set_page_config(page_title="Eventos Relevantes", layout="wide")

# Logo e encabezado
st.markdown("""
<div style='text-align: center;'>
    <h1>📄 Eventos Relevantes</h1>
    <h4 style='color: gray;'>Sistema de consulta de avisos corporativos con filtros dinámicos</h4>
</div>
""", unsafe_allow_html=True)

# Imagen corporativa (puedes cambiarla por un archivo real)
st.image("	https://www.tda-sgft.com/TdaWeb/images/logotipo.gif", width=150)

# Cargar datos
df = pd.read_excel("C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\HISTORICO_EMISORES_DATA_v2.xlsx",sheet_name="HIST")
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

    def make_clickable(link):
        if pd.notna(link) and str(link).strip() != "":
            return f'<a href="{link}" target="_blank">📎 Abrir</a>'
        else:
            return ""

    df_mostrar = df_filtrado.copy()
    df_mostrar['ARCHIVO'] = df_mostrar['ARCHIVO'].apply(make_clickable)
    df_mostrar['URL'] = df_mostrar['URL'].apply(make_clickable)

    st.markdown("### 📋 Resultados")
    st.write(f"Se encontraron **{len(df_mostrar)}** registros filtrados.")

    st.write(
        df_mostrar[['FECHA', 'CLAVE', 'SECCION', 'ASUNTO', 'ARCHIVO', 'URL']]
        .sort_values(by="FECHA", ascending=False)
        .to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    # Botón de descarga
    def to_csv(dataframe):
        return dataframe.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Descargar resultados como CSV",
        data=to_csv(df_filtrado),
        file_name="avisos_filtrados.csv",
        mime="text/csv"
    )
else:
    st.info("👈 Selecciona al menos una CLAVE para ver resultados.")

# PIE DE PÁGINA
st.markdown("""
<hr>
<div style='text-align: center; font-size: 13px; color: gray;'>
    Herramienta desarrollado por <strong>Steve Carpio - Python Streamlit </strong><br>Contacto: <a href="mailto:carpios@tda-sgft.com"> carpios@tda-sgft.com</a> <br>
    ⚠️ Solo para uso interno - No difundir fuera de la organización.
</div>
""", unsafe_allow_html=True)

