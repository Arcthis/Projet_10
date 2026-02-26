import pandas as pd

df = pd.read_excel("./data_files/Fichier_web.xlsx")

df = df.dropna(subset=["sku"])

df = df[df["post_type"] == "product"]

df.to_excel("./data_files/Fichier_web_treated.xlsx", index=False)
