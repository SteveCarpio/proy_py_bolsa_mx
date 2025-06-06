import streamlit as st
import pandas as pd
import io
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import hashlib
from xlsxwriter import Workbook

# ---------------- CONFIGURACIÓN INICIAL ---------------- #
st.set_page_config(page_title="Eventos Relevantes", layout="wide")
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; }
    </style>
""", unsafe_allow_html=True)

# ---------------- FUNCIONES DE LOGIN ---------------- #
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USUARIOS_AUTORIZADOS = {
    "admin": hash_password("1234"),
    "tda": hash_password("1234")
}

def login():
    st.markdown("## 🔐 Acceso restringido")
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if usuario in USUARIOS_AUTORIZADOS:
            if hash_password(contraseña) == USUARIOS_AUTORIZADOS[usuario]:
                st.session_state["logueado"] = True
                st.session_state["usuario"] = usuario
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta")
        else:
            st.error("❌ Usuario no válido")

# ---------------- BLOQUEO SI NO ESTÁ LOGUEADO ---------------- #
if "logueado" not in st.session_state or not st.session_state["logueado"]:
    login()
    st.stop()

# ---------------- ENCABEZADO Y LOGO ---------------- #
st.markdown("""
<div style='text-align: center;'>
    <h1>📄 Eventos Relevantes</h1>
    <h4 style='color: gray;'>Sistema de consulta de avisos corporativos con filtros dinámicos</h4>
</div>
""", unsafe_allow_html=True)

st.image("https://www.tda-sgft.com/TdaWeb/images/logotipo.gif", width=150)

# ---------------- CARGAR DATOS ---------------- #
df = pd.read_excel(
    "C:\\Users\\scarpio\\Documents\\GitHub\\proy_py_bolsa_mx\\excel\\HISTORICO_EMISORES_DATA_v2.xlsx",
    sheet_name="HIST"
)
df['FECHA'] = pd.to_datetime(df['FECHA'])

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.header("🔎 Filtros")

    claves = st.multiselect("CLAVE", options=sorted(df['CLAVE'].dropna().unique()), default=[])
    fechas = st.date_input("Rango de FECHAS", [])
    origenes = st.multiselect("ORIGEN", options=sorted(df['ORIGEN'].dropna().unique()), default=sorted(df['ORIGEN'].dropna().unique()))
    t_valores = st.multiselect("T", options=sorted(df['T'].dropna().unique()), default=sorted(df['T'].dropna().unique()))
    filtro_valores = st.multiselect("FILTRO", options=sorted(df['FILTRO'].dropna().unique()), default=sorted(df['FILTRO'].dropna().unique()))

    st.markdown("---")
    if st.button("🚪 Cerrar sesión"):
        st.session_state.clear()
        st.rerun()
    st.markdown("---")
    st.markdown("### ℹ️ Instrucciones")
    st.markdown("""
    - Selecciona una o más claves para comenzar.
    - Filtra por fecha u otros campos si lo necesitas.
    - Haz clic en 📎 para ver el documento o detalle.
    """)



# ---------------- FILTRADO Y TABLA ---------------- #
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

    columnas_mostrar = ['FECHA', 'CLAVE', 'SECCION', 'ASUNTO', 'ARCHIVO', 'URL']
    df_mostrar = df_filtrado[columnas_mostrar].sort_values(by='FECHA', ascending=False)
    df_mostrar['FECHA'] = df_mostrar['FECHA'].dt.strftime('%Y-%m-%d')


    st.markdown("### 📋 Resultados")
    st.write(f"Se encontraron **{len(df_mostrar)}** registros filtrados.")

    # ---------------- CONFIGURACIÓN AGGRID ---------------- #
    link_renderer = JsCode("""
    class UrlCellRenderer {
        init(params) {
            this.eGui = document.createElement('div');
            if (params.value && params.value !== 'null' && params.value !== '') {
                const link = document.createElement('a');
                link.href = params.value;
                link.innerText = "📎 Abrir";
                link.target = "_blank";
                link.style.textDecoration = "none";
                this.eGui.appendChild(link);
            } else {
                this.eGui.innerText = "Sin archivo";  // o simplemente deja vacío con ""
            }
        }
        getGui() {
            return this.eGui;
        }
    }
    """)


    gb = GridOptionsBuilder.from_dataframe(df_mostrar)
    gb.configure_default_column(filter=True, sortable=True, resizable=True)
    gb.configure_grid_options(domLayout='normal', quickFilter=True)
    #gb.configure_column("ARCHIVO", cellRenderer=link_renderer)
    #gb.configure_column("URL", cellRenderer=link_renderer)

    # Configurar columnas con anchos personalizados
    gb.configure_column("FECHA", width=100)
    gb.configure_column("CLAVE", width=100)
    gb.configure_column("SECCION", width=250, wrapText=True, autoHeight=True)
    gb.configure_column("ASUNTO", width=400, wrapText=True, autoHeight=True)
    gb.configure_column("ARCHIVO", cellRenderer=link_renderer, width=100)
    gb.configure_column("URL", cellRenderer=link_renderer, width=100)


    AgGrid(
        df_mostrar,
        gridOptions=gb.build(),
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        height=450
    )

    # ---------------- DESCARGAS ---------------- #
    def to_csv(dataframe):
        return dataframe.to_csv(index=False).encode('utf-8')

    def to_excel(dataframe):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name='Avisos')
        return output.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("📥 Descargar CSV", data=to_csv(df_filtrado), file_name="avisos_filtrados.csv", mime="text/csv")
    with col2:
        st.download_button("📥 Descargar Excel", data=to_excel(df_filtrado), file_name="avisos_filtrados.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

else:
    st.info("👈 Selecciona al menos una CLAVE para ver resultados.")

# ---------------- PIE DE PÁGINA ---------------- #
#st.markdown("""
#<hr>
#<div style='text-align: center; font-size: 13px; color: gray;'>
#    Herramienta desarrollada por <strong>Steve Carpio - Python Streamlit</strong><br>
#    PaContacto: <a href="mailto:carpios@tda-sgft.com">carpios@tda-sgft.com</a><br>
#    ⚠️ Solo para uso interno - No difundir fuera de la organización.
#</div>
#""", unsafe_allow_html=True)
st.markdown("""
<hr>
<div style='text-align: center; font-size: 13px; color: gray;'>
    ⚠️ Solo para uso interno - No difundir fuera de la organización.
</div>
""", unsafe_allow_html=True)
