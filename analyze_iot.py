import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка CSV
df = pd.read_csv("data/IoT_DDoS_normal_fridge.csv")

# Объединение даты и времени в один timestamp
df['timestamp'] = pd.to_datetime(df['Unnamed: 0'] + ' ' + df['Unnamed: 1'])

# Построение графика
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df, x="timestamp", y="Fridge_Temperature", hue="Temp_Condition", alpha=0.7)
plt.title("Fridge Temperature Over Time")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
