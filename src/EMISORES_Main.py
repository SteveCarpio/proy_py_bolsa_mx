import pandas as pd

Entorno = "PRO"

RutaRaiz = "C:\\MisCompilados\\PROY_BOLSA_MX\\"
RutaBIVA = f"{RutaRaiz}BIVA\\"
RutaBMV  = f"{RutaRaiz}BMV\\"

df_biva_1 = pd.read_excel(f"{RutaBIVA}CONFIG\\BIVA_Filtro_Emisores_PRO.xlsx")
df_biva_2 = pd.read_excel(f"{RutaBIVA}INFORMES\\BIVA_paso3_id_emisores.xlsx")

df_bmv_1 = pd.read_excel(f"{RutaBMV}CONFIG\\BMV_Filtro_Emisores_PRO.xlsx", sheet_name="FILTRO")      
df_bmv_2 = pd.read_excel(f"{RutaBMV}INFORMES\\BMV_paso4_.xlsx")                       

# Quedarnos con los campos CLAVE - CODIGO
df_biva_1 = df_biva_1[['CLAVE','CODIGO']]
df_biva_2 = df_biva_2[['CLAVE','CODIGO']]
df_bmv_1 = df_bmv_1[['CLAVE','CODIGO']]
df_bmv_2 = df_bmv_2[['CLAVE','CODIGO']]

print(f"Registros BIVA1: {len(df_biva_1)}")
print(f"Registros BIVA2: {len(df_biva_2)}")
print(f"Registros BMV1:  {len(df_bmv_1)} ")
print(f"Registros BMV2:  {len(df_bmv_2)} ")

sw1=0
sw2=0

if len(df_biva_2) > len(df_biva_1):
    print(f"Atención: Hay mas emisores en BIVA que tenemos que analizar {len(df_biva_2)} > {len(df_biva_1)}")
    df_biva_3 = df_biva_2[~df_biva_2['CODIGO'].isin(df_biva_1['CODIGO'])]
    df_biva_4 = df_biva_3.copy()
    df_biva_4['NOTA'] = "Bolsa Biva"
    sw1 = 1

if len(df_bmv_2) > len(df_bmv_1):
    print(f"Atención: Hay mas emisores en BMV que tenemos que analizar {len(df_bmv_2)} > {len(df_bmv_1)}")
    df_bmv_3 = df_bmv_2[~df_bmv_2['CODIGO'].isin(df_bmv_1['CODIGO'])]
    df_bmv_4 = df_bmv_3.copy()
    df_bmv_4['NOTA'] = "Bolsa Bmv"
    sw2 = 1
        
if (sw1 == 1) and (sw2 == 1):
    df_final = pd.concat([df_biva_4, df_bmv_4], ignore_index=True)

if (sw1 == 1) and (sw2 == 0):
    df_final = df_biva_4

if (sw1 == 0) and (sw2 == 1):
    df_final = df_bmv_4

# Aquí el código de envió de email
if sw1 == 1 or sw2 == 1:
    print(f"Falta {len(df_final)} registro/s en BMV: \n{df_final}")



