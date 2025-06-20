# ----------------------------------------------------------------------------------------
#  PASO5: ENVIÓ DE EMAIL
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BOLSAS_variables as sTv
from   cfg.BOLSAS_librerias import *

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------


# Función para cambiar los colores en las etiquetas TR HTML
def aplicar_colores_alternos(tabla_html):
    soup = BeautifulSoup(tabla_html, "html.parser")
    filas = soup.find_all("tr")
    for i, fila in enumerate(filas[1:]):  # saltamos la cabecera (filas[0])
        color = "#f2f2f2" if i % 2 == 0 else "#ffffff"  # (gris=f2f2f2 verdeAgua=f2fff3)
        estilo_existente = fila.get("style", "")
        fila["style"] = f"{estilo_existente} background-color: {color};"
    return str(soup)

# Función envió de Email
def enviar_email_con_adjunto(destinatarios_to, destinatarios_cc, asunto, cuerpo1, cuerpo2, ruta, nombre_archivo, df1, df2):

    # Compruebo si hay valores de las bolsas
    if df1.iloc[0]['CLAVE'] == 'none':
        v_df1 = 0
    else:
        v_df1 = 1
    if df2.iloc[0]['CLAVE'] == 'none':
        v_df2 = 0
    else:
        v_df2 = 1
    v_df = v_df1 + v_df2

    # Si no hay registros de la bolsa no se manda email, creado por los fines de semana que manda email vacíos
    if v_df == 0:
        print("No se enviará un email, parece que no hay registros de las bolsas de BIVA y BMV")
    else:

        # Configuración del servidor SMTP (Zimbra)
        smtp_server = 'zimbra.tda-sgft.com'
        smtp_port = 25  
        correo_remitente = 'publicacionesbolsasmx@tda-sgft.com'  
        contrasenia = 'tu_contraseña'  # no procede

        # Crear el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = correo_remitente
        mensaje['To'] = ", ".join(destinatarios_to)
        mensaje['Cc'] = ", ".join(destinatarios_cc)
        mensaje['Subject'] = asunto
        
        # Combinar destinatarios principales y en copia
        todos_destinatarios = destinatarios_to + destinatarios_cc 

        # Convertir el DataFrame a HTML - escape=False para que tenga en cuenta las etiquetas HMTL
        #tabla_html1 = df1.to_html(index=True, escape=False)  # index=True, con el índice
        #tabla_html2 = df2.to_html(index=True, escape=False)  # index=True, con el índice

        tabla_html1 = aplicar_colores_alternos(df1.to_html(index=True, escape=False))
        tabla_html2 = aplicar_colores_alternos(df2.to_html(index=True, escape=False))

        # Cuerpo del correo usando HTML y CSS
        cuerpo_html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                }}
                .content {{
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                h2 {{
                    color: #70B692;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    padding: 8px 12px;
                    text-align: left;
                    border: 1px solid #ddd;
                }}
                th {{
                    background-color: #59a62c;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                tr:nth-child(odd) {{
                    background-color: #ffffff;
                }}
            </style>
        </head>
        <body>
            <div class="content">
                
                <h2>EVENTOS RELEVANTES Y COMUNICADOS - BIVA</h2>
                <p>{cuerpo1}</p>
                {tabla_html1}  <!-- Aquí se inserta el DF convertido a HTML  -->
                <p></p><br><p></p>

                <h2>EVENTOS RELEVANTES Y COMUNICADOS - BMV</h2>
                <p>{cuerpo2}</p> 
                {tabla_html2}  <!-- Aquí se inserta el DF convertido a HTML  -->
                <p></p><br><p></p>
                
                <p>  </p><br><p></p>
                <i> ** Este correo electrónico fue enviado desde TdA mediante un proceso automático. Por favor, no responda a este mensaje  ** </i>
                
                
                    <p>
                        <br><br>
                        <br><br>
                        <br><br>
                        <br><br>

                        <table style="border: none; padding: 10px; border-spacing: 2px; width: 600px; table-layout: fixed;">
                            <tr>
                                <td style="width: 150px; padding-right: 10px; vertical-align: middle; border: 1px solid white;">
                                    <img src="https://www.tda-sgft.com/TdaWeb/images/logotipo.gif" alt="Titulización de Activos S.G.F.T., S.A" style="vertical-align: middle;">
                                </td>
                                <td style="width: 450px; padding-left: 10px; vertical-align: middle; border: 1px solid white;">
                                    <pre>
    Titulización de Activos S.G.F.T., S.A.
    C/Orense, 58 - 5ª Planta
    28020 Madrid
    Tel.: 91 702 08 08
    Fax:  91 308 68 54             
    e-mail: publicacionesbolsasmx@tda-sgft.com
    http://www.tda-sgft.com       </pre>
                                </td>
                            </tr>
                        </table>
                    </p>
                
                
            </div>
        </body>
        </html>
        """
        # El cuerpo del mensaje en formato: html
        mensaje.attach(MIMEText(cuerpo_html, 'html'))

        # El cuerpo del mensaje en formato: TXT
        #mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Combinar la ruta con el nombre del archivo
        # archivo_completo = os.path.join(ruta, nombre_archivo)

        # Adjuntar el archivo Excel  --- HEMOS DECIDIDO NO MANDAR EL EXCEL
        #try:
        #    with open(archivo_completo, 'rb') as archivo:
        #        # Crear el objeto MIME para el archivo adjunto
        #        adjunto = MIMEApplication(archivo.read(), _subtype='xlsx')
        #        adjunto.add_header('Content-Disposition', 'attachment', filename=nombre_archivo)
        #        mensaje.attach(adjunto)
        #except Exception as e:
        #    print(f"Error al adjuntar el archivo: {e}")

        # Enviar el correo
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as servidor:
                servidor.sendmail(correo_remitente, todos_destinatarios, mensaje.as_string())
            print(f"- Correo enviado exitosamente a: {', '.join(todos_destinatarios)}")
        except Exception as e:
            print(f"- Error al enviar el correo: {e}")

# Función Leer excel y convertirlos en DataFrame
def sTv_paso4_lee_DF(ruta, bolsa, var_Fechas2):

    # Verificar si el archivo existe
    if os.path.exists(ruta):
        try:
            # Si existe, leer el archivo Excel a un DataFrame
            df = pd.read_excel(ruta, index_col=0)
            print(f"- Archivo encontrado: {ruta}")
            if bolsa == "BMV":
                df['ARCHIVO'] = '<a href=" ' + df['ARCHIVO'] + ' " target="_blank" > Abrir Archivo </a>'

            df['URL'] = '<a href=" ' + df['URL'] + ' " target="_blank" > Abrir URL </a>'

            return df
        except Exception as e:
            print(f"- Error al leer el archivo: {e} - {ruta} - {bolsa}")
            return None
    else:
        # Si no existe, crear un DataFrame con las columnas predefinidas
        print(f"- El archivo no se encuentra en {ruta}. Creando DataFrame por defecto para {bolsa}.")
        df = pd.DataFrame({
            'CLAVE': ["none"],
            'CODIGO': [bolsa],
            'INFO': [f'No existen datos con la fecha de búsqueda: {var_Fechas2}']
        })  
        return df

# ----------------------------------------------------------------------------------------
#                               INICIO PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso4(var_NombreSalida, var_Fechas2, var_Fechas3, var_SendEmail, var_Entorno):
    
    # Ruta del archivo Excel
    ruta_excel1 = f"{sTv.var_RutaInforme}BIVA_{var_Fechas3}_M.xlsx"
    ruta_excel2 = f"{sTv.var_RutaInforme}BIVA_{var_Fechas3}_P.xlsx"
    ruta_excel5 = f"{sTv.var_RutaInforme}BIVA_{var_Fechas3}_X.xlsx"
    ruta_excel3 = f"{sTv.var_RutaInforme}BMV_{var_Fechas3}_M.xlsx"
    ruta_excel4 = f"{sTv.var_RutaInforme}BMV_{var_Fechas3}_P.xlsx"
    ruta_excel6 = f"{sTv.var_RutaInforme}BMV_{var_Fechas3}_X.xlsx"
    

    # Leer el archivo o crear el DataFrame por defecto
    df_BIVA_M = sTv_paso4_lee_DF(ruta_excel1, "BIVA", var_Fechas2)
    df_BIVA_P = sTv_paso4_lee_DF(ruta_excel2, "BIVA", var_Fechas2)
    df_BIVA_X = sTv_paso4_lee_DF(ruta_excel5, "BIVA", var_Fechas2)
    df_BMV_M = sTv_paso4_lee_DF(ruta_excel3,  "BMV",  var_Fechas2)
    df_BMV_P = sTv_paso4_lee_DF(ruta_excel4,  "BMV",  var_Fechas2)
    df_BMV_X = sTv_paso4_lee_DF(ruta_excel6,  "BMV",  var_Fechas2)

    # Lista de emisores distintos
    lst_emisores_m1 = ', '.join(df_BIVA_M['CLAVE'].unique())
    lst_emisores_m2 = ', '.join(df_BMV_M['CLAVE'].unique())
    lst_emisores_p1 = ', '.join(df_BIVA_P['CLAVE'].unique())
    lst_emisores_p2 = ', '.join(df_BMV_P['CLAVE'].unique())
    lst_emisores_x1 = ', '.join(df_BIVA_X['CLAVE'].unique())
    lst_emisores_x2 = ', '.join(df_BMV_X['CLAVE'].unique())

    # BIVA: Numero de emisores y eventos distintos
    if lst_emisores_m1 == "none":
        num_emisores_m1 = 0
        num_eventos_m1 = 0
        lst_emisores_m1 = ""
    else:
        num_emisores_m1 = len(df_BIVA_M['CLAVE'].unique())
        num_eventos_m1 = len(df_BIVA_M)

    if lst_emisores_m2 == "none":
        num_emisores_m2 = 0
        num_eventos_m2 = 0
        lst_emisores_m2 = ""
    else:
        num_emisores_m2 = len(df_BMV_M['CLAVE'].unique())
        num_eventos_m2 = len(df_BMV_M)

    # BMV: Numero de emisores y eventos distintos
    if lst_emisores_p1 == "none":
        num_emisores_p1 = 0
        num_eventos_p1 = 0
        lst_emisores_p1 = ""
    else:
        num_emisores_p1 = len(df_BIVA_P['CLAVE'].unique())
        num_eventos_p1 = len(df_BIVA_P)
        
    if lst_emisores_p2 == "none":
        num_emisores_p2 = 0
        num_eventos_p2 = 0
        lst_emisores_p2 = ""
    else:
        num_emisores_p2 = len(df_BMV_P['CLAVE'].unique())
        num_eventos_p2 = len(df_BMV_P)

    # EXCLUIDOS: Numero de emisores y eventos distintos
    if lst_emisores_x1 == "none":
        num_emisores_x1 = 0
        num_eventos_x1 = 0
        lst_emisores_x1 = ""
    else:
        num_emisores_x1 = len(df_BIVA_X['CLAVE'].unique())
        num_eventos_x1 = len(df_BIVA_X)
        
    if lst_emisores_x2 == "none":
        num_emisores_x2 = 0
        num_eventos_x2 = 0
        lst_emisores_x2 = ""
    else:
        num_emisores_x2 = len(df_BMV_X['CLAVE'].unique())
        num_eventos_x2 = len(df_BMV_X)

    print(f"\n- Lista de lst_emisores_m1: {lst_emisores_m1}")
    print(f"- Lista de lst_emisores_m2: {lst_emisores_m2}")
    print(f"- Lista de lst_emisores_p1: {lst_emisores_p1}")
    print(f"- Lista de lst_emisores_p2: {lst_emisores_p2}")
    print(f"- Lista de lst_emisores_x1: {lst_emisores_x1}")
    print(f"- Lista de lst_emisores_x2: {lst_emisores_x2}")

    # Extraer los destinatarios de correo del excel
    df_email = pd.read_excel(f'{sTv.var_RutaConfig}{sTv.var_NombreEmisores}_{var_Entorno}.xlsx')
    # to
    valor_to_m1 = df_email.loc[df_email['GRUPO'] == 'M', 'TO'].iloc[0]
    valor_to_m = str(valor_to_m1)
    valor_to_p1 = df_email.loc[df_email['GRUPO'] == 'P', 'TO'].iloc[0]
    valor_to_p = str(valor_to_p1)
    # cc
    valor_cc_m1 = df_email.loc[df_email['GRUPO'] == 'M', 'CC'].iloc[0]
    valor_cc_m = str(valor_cc_m1)
    valor_cc_p1 = df_email.loc[df_email['GRUPO'] == 'P', 'CC'].iloc[0]
    valor_cc_p = str(valor_cc_p1)

    print(f"\n- Email valor_to_m: {valor_to_m}")
    print(f"- Email valor_to_p: {valor_to_p}")
    print(f"- Email valor_cc_m: {valor_cc_m}")
    print(f"- Email valor_cc_p: {valor_cc_p}")

    # Mandar Email ------------------------------------------------------
    destinatarios_cc_m = [elemento.strip("'") for elemento in valor_cc_m.split(",")]
    destinatarios_cc_p = [elemento.strip("'") for elemento in valor_cc_p.split(",")]
    destinatarios_to_m = [elemento.strip("'") for elemento in valor_to_m.split(",")]
    destinatarios_to_p = [elemento.strip("'") for elemento in valor_to_p.split(",")]
    destinatarios_cc_x = ['carpios@tda-sgft.com']
    destinatarios_to_x = ['talavanf@tda-sgft.com','blancod@tda-sgft.com']
    #------------------
    #destinatarios_cc_m = ['carpios@tda-sgft.com']
    #destinatarios_cc_p = ['carpios@tda-sgft.com']
    #destinatarios_to_m = ['talavanf@tda-sgft.com']
    #destinatarios_to_p = ['talavanf@tda-sgft.com']
    #destinatarios_cc_x = ['carpios@tda-sgft.com']
    #destinatarios_to_x = ['talavanf@tda-sgft.com']
    #------------------
    asunto = f'Eventos Relevantes y Comunicados Bolsas_{var_Fechas2} | Tda Update '
    asunto_x = f'Eventos Relevantes y Comunicados Bolsas_{var_Fechas2} | Tda Excluidos '
    ruta = f'{sTv.var_RutaInforme}'
    nombre_archivo_m = "none" # f'BIVA_{var_Fechas3}_M.zip' : sTv se mandaría un zip con los 2 excel  
    nombre_archivo_p = "none" # f'BMV_{var_Fechas3}_M.zip'  : sTv se mandaría un zip con los 2 excel
    nombre_archivo_x = "none"
    cuerpo_m1=f'Fecha Datos: <b>{var_Fechas2}</b><br>Número de Emisores: <b>{num_emisores_m1}</b><br>Número de Eventos/Comunicados: <b>{num_eventos_m1}</b><br>Lista de Emisores: <b>{lst_emisores_m1}</b>' 
    cuerpo_m2=f'Fecha Datos: <b>{var_Fechas2}</b><br>Número de Emisores: <b>{num_emisores_m2}</b><br>Número de Eventos/Comunicados: <b>{num_eventos_m2}</b><br>Lista de Emisores: <b>{lst_emisores_m2}</b>'
    cuerpo_p1=f'Fecha Datos: <b>{var_Fechas2}</b><br>Número de Emisores: <b>{num_emisores_p1}</b><br>Número de Eventos/Comunicados: <b>{num_eventos_p1}</b><br>Lista de Emisores: <b>{lst_emisores_p1}</b>' 
    cuerpo_p2=f'Fecha Datos: <b>{var_Fechas2}</b><br>Número de Emisores: <b>{num_emisores_p2}</b><br>Número de Eventos/Comunicados: <b>{num_eventos_p2}</b><br>Lista de Emisores: <b>{lst_emisores_p2}</b>'
    cuerpo_x1=f'Fecha Datos: <b>{var_Fechas2}</b><br>Número de Emisores: <b>{num_emisores_x1}</b><br>Número de Eventos/Comunicados: <b>{num_eventos_x1}</b><br>Lista de Emisores: <b>{lst_emisores_x1}</b>' 
    cuerpo_x2=f'Fecha Datos: <b>{var_Fechas2}</b><br>Número de Emisores: <b>{num_emisores_x2}</b><br>Número de Eventos/Comunicados: <b>{num_eventos_x2}</b><br>Lista de Emisores: <b>{lst_emisores_x2}</b>'

    print(f"\n- Cuerpo final del Email\n")
    print(f"  Email M: ")
    print(f"  Destinatarios TO:    {destinatarios_to_m}")
    print(f"  Destinatarios CC:    {destinatarios_cc_m}")
    print(f"  Asunto:              {asunto}")
    print(f"  Ruta:                {ruta}")
    print(f"  Nombre Archivo:      {nombre_archivo_m}")
    print(f"\n  Cuerpo BIVA Resumen: {cuerpo_m1}")
    print(f'  Cuerpo BIVA Datos: \n{df_BIVA_M}')
    print(f"\n  Cuerpo BMV Resumen:  {cuerpo_m2}")
    print(f'  Cuerpo BMV Datos:\n{df_BMV_M}')

    print(f" \n\n Email P: ")
    print(f"  Destinatarios TO:    {destinatarios_to_p}")
    print(f"  Destinatarios CC:    {destinatarios_cc_p}")
    print(f"  Asunto:              {asunto}")
    print(f"  Ruta:                {ruta}")
    print(f"  Nombre Archivo:      {nombre_archivo_p}")
    print(f"\n  Cuerpo BIVA Resumen: {cuerpo_p1}")
    print(f'  Cuerpo BIVA Datos: \n{df_BIVA_P}')
    print(f"\n  Cuerpo BMW Resumen:  {cuerpo_p2}")
    print(f'  Cuerpo BMV Datos:\n{df_BMV_P}') 

    # Envío del email
    enviar_email_con_adjunto(destinatarios_to_m, destinatarios_cc_m, asunto, cuerpo_m1, cuerpo_m2, ruta, nombre_archivo_m, df_BIVA_M, df_BMV_M)
    enviar_email_con_adjunto(destinatarios_to_p, destinatarios_cc_p, asunto, cuerpo_p1, cuerpo_p2, ruta, nombre_archivo_p, df_BIVA_P, df_BMV_P)

    conteo_BIVA_X = (df_BIVA_X['CLAVE'] == 'none').sum()
    conteo_BMV_X  = (df_BMV_X['CLAVE']  == 'none').sum()
    conteo_X = conteo_BIVA_X + conteo_BMV_X
    if conteo_X != 2:  # Mandará un email en caso de que existan registros.
        print("- Se manda email con datos excluidos")
        enviar_email_con_adjunto(destinatarios_to_x, destinatarios_cc_x, asunto_x, cuerpo_x1, cuerpo_x2, ruta, nombre_archivo_x, df_BIVA_X, df_BMV_X)
