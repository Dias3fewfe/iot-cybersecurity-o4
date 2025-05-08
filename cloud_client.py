import pandas as pd
import requests

# Загружаем CSV 
df = pd.read_csv("data/IoT_DDoS_normal_fridge.csv")

# Берем первые 100 строк
records = df.head(100).to_dict(orient='records')
print(f"📤 Отправка {len(records)} записей на fog-сервер...")

# Отправляем на fog для предсказаний
fog_response = requests.post("http://127.0.0.1:6000/fog", json=records)

print("📨 Ответ от fog-сервера (raw):", fog_response.text[:300], "...")  # обрезаем длинный вывод

# Проверка ответа
if fog_response.status_code == 200:
    predicted_data = fog_response.json()
    print("✅ Получены предсказания от fog-сервера. Пример:")
    print(predicted_data[:1])  # только одну строку для примера

    # 🔁 Отправляем каждый предсказанный результат в Cloud Layer
    for record in predicted_data:
        try:
            cloud_response = requests.post("http://127.0.0.1:7000/cloud", json=record)
            if cloud_response.status_code == 200:
                print("🌥 Ответ от Cloud Layer:", cloud_response.json())
            else:
                print(f"⚠️ Ошибка от Cloud Layer [{cloud_response.status_code}]:", cloud_response.text)
        except Exception as e:
            print("🚫 Ошибка при подключении к Cloud Layer:", str(e))

else:
    print("❌ Ошибка от fog-сервера:", fog_response.status_code)
    print("Тело ответа:", fog_response.text)
