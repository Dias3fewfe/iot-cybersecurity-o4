import pandas as pd
import requests

# Загрузка и обработка первых 10 строк
df = pd.read_csv("data/IoT_DDoS_normal_fridge.csv")
df_filtered = df[["Fridge_Temperature", "Temp_Condition"]].head(10)

# Отправка в fog
try:
    response = requests.post("http://127.0.0.1:6000/from_edge", json=df_filtered.to_dict(orient="records"))
    print("Edge → Fog result:", response.json())
except Exception as e:
    print("Error sending to Fog:", e)
