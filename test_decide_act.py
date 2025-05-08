import requests

# ⚠️ Создаём запись с угрозой и высокой температурой
test_data = {
    "Fridge_Temperature": 99.9,
    "Temp_Condition": 1,
    "Threat_Prediction": 1
}

# 🔁 Отправляем на Cloud Layer
response = requests.post("http://127.0.0.1:7000/cloud", json=test_data)

# 📩 Смотрим ответ
if response.status_code == 200:
    print("✅ Cloud response:")
    print(response.json())
else:
    print("❌ Error:", response.status_code)
    print(response.text)
