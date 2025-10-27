# ----------------------------------------------------------------------------------------
#                                  Validar Las lista de Emisores 
# 
# Programa que comprueba si hay nuevos emisores en BIVA o BMV que se deben agregar
# Autor: SteveCarpio
# Versión: V1 2025
# ----------------------------------------------------------------------------------------

import pandas as pd
import smtplib
import sys
from email.mime.multipart import MIMEMultipart                    
from email.mime.text import MIMEText                                

# ----------------------------------------------------------------------------------------
#                               FUNCIONES DE APOYO
# ----------------------------------------------------------------------------------------
# Función envió de Email
def enviar_email_con_adjunto(destinatarios_to, destinatarios_cc, asunto, cuerpo, df):
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
    tabla_html = df.to_html(index=True, escape=False)  # con el índice
 

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
                background-color: red;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
        </style>
    </head>
    <body>
        <div class="content">
            
            Lista de los nuevos emisores que deben ser revisados.
            <br><br>
            
            {tabla_html}  <!-- Aquí se inserta el DF convertido a HTML  -->

            <br>
            <p>"Es necesario agregar el/los {len(df)} emisores en los archivos de configuración en el servidor Python para que se tengan en cuenta en la próxima ejecución.". 
            </p><br>
            Bolsa BIVA: C:\\MisCompilados\\PROY_BOLSA_MX\\BIVA\\CONFIG\\BIVA_Filtro_Emisores_PRO.xlsx <br>
            Bolsa BMV:  C:\\MisCompilados\\PROY_BOLSA_MX\\BMV\\CONFIG\\BMV_Filtro_Emisores_PRO.xlsx <br><br>
            <p></p>

            <p>  </p><br><p></p>
            <i> ** Para más ayuda consultar con SteveCarpio. <br><br> ** Este email fue enviado desde un proceso automático desde TdA. Por favor, no responder a este email. ** </i>
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

# ----------------------------------------------------------------------------------------
#                               INICIO DEL PROGRAMA
# ----------------------------------------------------------------------------------------

# Parámetro: Producción o Desarrollo
Entorno = "DEV"
if len(sys.argv) > 1 :
    var_param = sys.argv[1]
    if var_param == "PRO":
        Entorno = var_param


RutaRaiz = "C:\\MisCompilados\\PROY_BOLSA_MX\\"
RutaBIVA = f"{RutaRaiz}BIVA\\"
RutaBMV  = f"{RutaRaiz}BMV\\"

# Leo los excel de entrada
df_biva_1 = pd.read_excel(f"{RutaBIVA}CONFIG\\BIVA_Filtro_Emisores_PRO.xlsx")
df_biva_2 = pd.read_excel(f"{RutaBIVA}INFORMES\\BIVA_paso3_id_emisores.xlsx")
df_bmv_1  = pd.read_excel(f"{RutaBMV}CONFIG\\BMV_Filtro_Emisores_PRO.xlsx", sheet_name="FILTRO")      
df_bmv_2  = pd.read_excel(f"{RutaBMV}INFORMES\\BMV_paso4_.xlsx")                       

# Quedarnos con los campos CLAVE - CODIGO
df_biva_1 = df_biva_1[['CLAVE','CODIGO']]
df_biva_2 = df_biva_2[['CLAVE','CODIGO']]
df_bmv_1 = df_bmv_1[['CLAVE','CODIGO']]
df_bmv_2 = df_bmv_2[['CLAVE','CODIGO']]

# Verificamos si existen diferencias entre las dos tablas
df_biva_3 = df_biva_2[~df_biva_2['CODIGO'].isin(df_biva_1['CODIGO'])]
df_biva_4 = df_biva_3.copy()
df_biva_4['NOTA'] = "Bolsa Biva"

# Verificamos si existen diferencias entre las dos tablas
df_bmv_3 = df_bmv_2[~df_bmv_2['CODIGO'].isin(df_bmv_1['CODIGO'])]
df_bmv_4 = df_bmv_3.copy()
df_bmv_4['NOTA'] = "Bolsa Bmv"

# Creo la tabla final    
df_final = pd.concat([df_biva_4, df_bmv_4], ignore_index=True)
df_final = df_final.reset_index(drop=True)
df_final.index = df_final.index + 1

# Si existe un nuevo emisor mando email
if len(df_final) > 0:
    print(f"- Ok se manda correo, existen {len(df_final)} registro/s a tener en cuenta")
    print(df_final)
    if Entorno == "PRO":
        print("- Ejecución en modo: PRO")
        destinatarios_to = ['repcomun@tda-sgft.com']
        destinatarios_cc = ['carpios@tda-sgft.com']
    else:
        print("- Ejecución en modo: DEV")
        destinatarios_to = ['carpios@tda-sgft.com']
        destinatarios_cc = ['carpios@tda-sgft.com']

    asunto = f"[ATENCIÓN] Nuevos emisores pendientes de revisión ({len(df_final)}) | TDA Update"
    cuerpo = ""
    enviar_email_con_adjunto(destinatarios_to, destinatarios_cc, asunto, cuerpo, df_final)

else:
    print(f"- No existen nuevos emisores a tener en cuenta")





