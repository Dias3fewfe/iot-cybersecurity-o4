from flask import Flask, request, jsonify
import pandas as pd
import joblib
import requests

app = Flask(__name__)

# Загружаем обученную модель
model = joblib.load("model.pkl")

# Cloud endpoint
CLOUD_ENDPOINT = "http://127.0.0.1:7000/cloud"  # Убедись, что cloud_server.py работает

@app.route('/fog', methods=['POST'])

def fog_process():
    try:
        # Получаем JSON-данные и превращаем в DataFrame
        data = request.json
        df = pd.DataFrame(data)

        # Удаляем лишние колонки, если они есть
        df = df.drop(columns=["Unnamed: 0", "Unnamed: 1", "Unnamed: 3"], errors='ignore')

        # Обрабатываем Temp_Condition
        if "Temp_Condition" in df.columns:
            df["Temp_Condition"] = df["Temp_Condition"].map({"low": 0, "high": 1})

        # Выбираем нужные признаки
        expected_columns = ["Fridge_Temperature", "Temp_Condition"]
        df = df[expected_columns]

        # Предсказание угрозы
        predictions = model.predict(df)
        df['Threat_Prediction'] = predictions

        # ⬆️ Отправляем результат в облако
        for _, row in df.iterrows():
            payload = row.to_dict()
            try:
                cloud_response = requests.post(CLOUD_ENDPOINT, json=payload)
                print("☁️ Sent to cloud:", cloud_response.status_code)
            except Exception as e:
                print("❌ Error sending to cloud:", str(e))

        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=6000, debug=True)
