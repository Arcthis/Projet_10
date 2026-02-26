import pandas as pd
df_erp = pd.read_excel("Fichier_erp.xlsx")
print(f"ERP : {df_erp.columns}")

df_web = pd.read_excel("Fichier_web.xlsx")
print(f"WEB : {df_web.columns}")

df_liaison = pd.read_excel("fichier_liaison.xlsx")
print(f"LIAISON : {df_liaison.columns}")
