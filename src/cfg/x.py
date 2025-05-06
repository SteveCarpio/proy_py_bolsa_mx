import pandas as pd

df_paso8_P_ = pd.read_excel(r"C:\MisCompilados\PROY_BOLSA_MX\BIVA\INFORMES\BIVA_20250424_M.xlsx")
df_paso8_P_ = df_paso8_P_.loc[:, ~df_paso8_P_.columns.str.contains('^Unnamed')]
df_paso8_M_ = pd.read_excel(r"C:\MisCompilados\PROY_BOLSA_MX\BIVA\INFORMES\BIVA_20250424_M.xlsx")
df_paso8_M_ = df_paso8_M_.loc[:, ~df_paso8_M_.columns.str.contains('^Unnamed')]



# Crea el filtro True - False de los registros que cumplen la condición
filtro_df_P = df_paso8_P_['ASUNTO'].str.contains('asamblea', case=False, na=False) & \
             ~df_paso8_P_['ASUNTO'].str.contains('tenedores', case=False, na=False)   #   'tenedores|otros1|otros2|etc..'
filtro_df_M = df_paso8_M_['ASUNTO'].str.contains('asamblea', case=False, na=False) & \
             ~df_paso8_M_['ASUNTO'].str.contains('tenedores', case=False, na=False)   #   'tenedores|otros1|otros2|etc..'
# Crear los DF con los datos a enviar y los excluidos
df_paso8_P_F = df_paso8_P_[~filtro_df_P]
df_exclu_P_F = df_paso8_P_[filtro_df_P]
df_paso8_M_F = df_paso8_M_[~filtro_df_M]
df_exclu_M_F = df_paso8_M_[filtro_df_M]
# Crea un nuevo campo para diferenciar
df_exclu_P_F = df_exclu_P_F.copy()  # copy = para que salga mensaje de warning
df_exclu_P_F["EMAIL"] = "P"
df_exclu_M_F = df_exclu_M_F.copy()  # copy = para que salga mensaje de warning
df_exclu_M_F["EMAIL"] = "M"
# Concatenamos las dos tabla de datos excluidos
df_excluidos = pd.concat([df_exclu_P_F, df_exclu_M_F], ignore_index=True)
df_excluidos.index = df_excluidos.index + 1

print(df_excluidos)
