import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Загружаем CSV-файл
df = pd.read_csv("data/IoT_DDoS_normal_fridge.csv")


# ✅ Показываем, какие колонки есть
print("🧾 Названия колонок в CSV:", df.columns.tolist())

# ✅ Оставляем только нужные колонки
expected_columns = ["Fridge_Temperature", "Temp_Condition", "Threat_Label"]
df = df[expected_columns]

# ✅ Обработка категориальной переменной
df["Temp_Condition"] = df["Temp_Condition"].map({"low": 0, "high": 1})

# Разделение данных
X = df[["Fridge_Temperature", "Temp_Condition"]]
y = df["Threat_Label"]

# Обучаем модель
model = RandomForestClassifier()
model.fit(X, y)

# Сохраняем модель
joblib.dump(model, "model.pkl")
print("✅ Модель успешно обучена и сохранена как model.pkl")
