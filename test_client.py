import requests

# Пример записей: одна с high, другая с low
test_data = [
    {
        "Fridge_Temperature": 8.65,
        "Temp_Condition": "high"
    },
    {
        "Fridge_Temperature": 2.50,
        "Temp_Condition": "low"
    }
]

# Отправляем на fog-сервер
response = requests.post("http://127.0.0.1:6000/predict", json=test_data)

if response.status_code == 200:
    print("✅ Prediction result:")
    for record in response.json():
        print(record)
else:
    print("❌ Error:", response.status_code)
    print(response.text)
