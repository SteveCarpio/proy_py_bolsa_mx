# ----------------------------------------------------------------------------------------
#  PASO8: ENVIO DE EMAIL
#  Autor: SteveCarpio-2025
# ----------------------------------------------------------------------------------------

import cfg.BMV_variables as sTv
from   cfg.BMV_librerias import *

# Función envió de Email
def enviar_email_con_adjunto(destinatarios_to, destinatarios_cc, asunto, cuerpo, ruta, nombre_archivo, df):
    # Configuración del servidor SMTP (Zimbra)
    smtp_server = 'zimbra.tda-sgft.com'
    smtp_port = 25  
    correo_remitente = 'publicacionesbolsasmx@tda-sgft.com'  
    contrasena = 'tu_contraseña'  # no procede

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje['From'] = correo_remitente
    mensaje['To'] = ", ".join(destinatarios_to)
    mensaje['Cc'] = ", ".join(destinatarios_cc)
    mensaje['Subject'] = asunto
    
    # Combinar destinatarios principales y en copia
    todos_destinatarios = destinatarios_to + destinatarios_cc 

    # Convertir el DataFrame a HTML
    tabla_html = df.to_html(index=True)  # con el índice

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
                background-color: #96C60F;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            
            <h2>EVENTOS RELEVANTES Y COMUNICADOS - BMV</h2>
            <p>{cuerpo}</p>
            
            {tabla_html}  <!-- Aquí se inserta el DF convertido a HTML  -->
            <p></p><br><p></p>
            
            <p>  </p><br><p></p>
            <i> ** Este email fue enviado desde un proceso automático desde TdA. Por favor, no responder a este email. ** </i>
            <p>
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
 http://www.tda-sgft.com            </pre>
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
    archivo_completo = os.path.join(ruta, nombre_archivo)

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


# ----------------------------------------------------------------------------------------
#                               INICIO DEL PROGRAMA
# ----------------------------------------------------------------------------------------

def sTv_paso8(var_NombreSalida, var_FechasSalida, var_Fechas3, var_SendEmail):
    
    # Leer el excel de entrada 
    df_paso8 = pd.read_excel(f'{sTv.var_RutaInforme}{var_NombreSalida}_paso7_{var_FechasSalida}.xlsx')

    # Obtener la fecha actual
    #fecha_actual = dt.now()

    # <--OJO--> usar esta variable "var_FechasSalida" si la tenemos activa
    # fecha_formateada = var_FechasSalida
    fecha_formateada = var_Fechas3

    ruta = f'{sTv.var_RutaInforme}'
    
    # Creamos DF con los datos por grupos
    df_paso8_P_ = df_paso8[df_paso8['GRUPO'] == 'P'][['CLAVE', 'SECCION', 'FECHA','ASUNTO','URL','ARCHIVO']]
    df_paso8_M_ = df_paso8[df_paso8['GRUPO'] == 'M'][['CLAVE', 'SECCION', 'FECHA','ASUNTO','URL','ARCHIVO']]

    # Ordenar el DataFrame
    df_paso8_P = df_paso8_P_.sort_values(by='CLAVE')
    df_paso8_M = df_paso8_M_.sort_values(by='CLAVE')

    if len(df_paso8_P) > 0:

        # Numero de emisores distintos
        num_emisores_p = len(df_paso8_P['CLAVE'].unique())

        # Fecha de los datos
        fec_emisores_p = df_paso8_P['FECHA'].unique()

        # Lista de emisores distintos
        lst_emisores_p = ', '.join(df_paso8_P['CLAVE'].unique())
        
        # Reiniciamos el indice
        df_paso8_P = df_paso8_P.reset_index(drop=True)

        # Empezamos por el indice 1 y no por el 0
        df_paso8_P.index = df_paso8_P.index + 1

        # Excel de salida
        nombre_archivo_p = f'{var_NombreSalida}_{fecha_formateada}_P.xlsx' #  

        # Creo un excel con el resultado del DataFrame
        df_paso8_P.to_excel(f'{sTv.var_RutaInforme}{nombre_archivo_p}',sheet_name='EMISORES', index=True)
        print(f"- Datos temporales guardados en el excel {sTv.var_RutaInforme}{nombre_archivo_p}")
        
        # Cuenta de Email para el GRUPO (P) - TO y CC
        # to
        valor_to_p1 = df_paso8.loc[df_paso8['GRUPO'] == 'P', 'TO'].iloc[0]
        valor_to_p2 = str(valor_to_p1)
        destinatarios_to_p = [elemento.strip("'") for elemento in valor_to_p2.split(",")]
        # cc
        valor_cc_p1 = df_paso8.loc[df_paso8['GRUPO'] == 'P', 'CC'].iloc[0]
        valor_cc_p2 = str(valor_cc_p1)
        destinatarios_cc_p = [elemento.strip("'") for elemento in valor_cc_p2.split(",")]

        # Asuntos 
        asunto_p = f'EVENTOS RELEVANTES Y COMUNICADOS BOLSAS_{fec_emisores_p[0]}_tda update '

        # Datos compartidos
        cuerpo_p = f'Fecha Datos: <b>{fec_emisores_p[0]}</b><br>Número de Emisores: <b>{num_emisores_p}</b><br>Número de Eventos/Comunicados: <b>{len(df_paso8_P)}</b><br>Lista de Emisores: <b>{lst_emisores_p}</b>'
        
        #destinatarios_to_p=['carpios@tda-sgft.com']
        #destinatarios_cc_p=['carpios@tda-sgft.com']  # repcomun

        # Envio a la función enviar_email los datos necesarios
        if var_SendEmail == "S":
            enviar_email_con_adjunto(destinatarios_to_p, destinatarios_cc_p, asunto_p, cuerpo_p, ruta, nombre_archivo_p, df_paso8_P)
    else:
        if var_SendEmail == "S":
            print(f"- NO HAY DATOS PARA MANDAR UN EMAIL GRUPO (P)")
     
    if len(df_paso8_M) > 0:

        # Numero de emisores distintos
        num_emisores_m = len(df_paso8_M['CLAVE'].unique())

        # Fecha de los datos
        fec_emisores_m = df_paso8_M['FECHA'].unique()

        # Lista de emisores distintos
        lst_emisores_m = ', '.join(df_paso8_M['CLAVE'].unique())
        
        # Reiniciamos el indice
        df_paso8_M = df_paso8_M.reset_index(drop=True)

        # Empezamos por el indice 1 y no por el 0
        df_paso8_M.index = df_paso8_M.index + 1

        # Excel de salida
        nombre_archivo_m = f'{var_NombreSalida}_{fecha_formateada}_M.xlsx' #  

        # Creo un excel con el resultado del DataFrame
        df_paso8_M.to_excel(f'{sTv.var_RutaInforme}{nombre_archivo_m}',sheet_name='EMISORES', index=True)
        print(f"- Datos temporales guardados en el excel {sTv.var_RutaInforme}{nombre_archivo_m}")

        # Cuenta de Email para el GRUPO (M) - TO y CC
        # to
        valor_to_m1 = df_paso8.loc[df_paso8['GRUPO'] == 'M', 'TO'].iloc[0]
        valor_to_m2 = str(valor_to_m1)
        destinatarios_to_m = [elemento.strip("'") for elemento in valor_to_m2.split(",")]
        # cc
        valor_cc_m1 = df_paso8.loc[df_paso8['GRUPO'] == 'M', 'CC'].iloc[0]
        valor_cc_m2 = str(valor_cc_m1)
        destinatarios_cc_m = [elemento.strip("'") for elemento in valor_cc_m2.split(",")]

        # Asuntos 
        asunto_m = f'EVENTOS RELEVANTES Y COMUNICADOS BOLSAS_{fec_emisores_m[0]}_tda update '

        # Datos compartidos
        cuerpo_m = f'Fecha Datos: <b>{fec_emisores_m[0]}</b><br>Número de Emisores: <b>{num_emisores_m}</b><br>Número de Eventos/Comunicados: <b>{len(df_paso8_M)}</b><br>Lista de Emisores: <b>{lst_emisores_m}</b>'
        
        #destinatarios_to_m=['carpios@tda-sgft.com']
        #destinatarios_cc_m=['carpios@tda-sgft.com']  # repcomun

        # Envio a la función enviar_email los datos necesarios
        if var_SendEmail == "S":
            enviar_email_con_adjunto(destinatarios_to_m, destinatarios_cc_m, asunto_m, cuerpo_m, ruta, nombre_archivo_m, df_paso8_M)
    else:
        if var_SendEmail == "S":
            print(f"- NO HAY DATOS PARA MANDAR UN EMAIL GRUPO (M)")
