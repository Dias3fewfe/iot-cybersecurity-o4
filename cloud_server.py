from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 🔐 Настройки Telegram
BOT_TOKEN = "7286132933:AAGTxMXlBVFF62KeED_pnKodc6K3lrc1Hqs"
CHAT_ID = 699941829  # 🔁 ← Поменяй на СВОЙ chat_id

# 🔔 Функция отправки сообщения
def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{"7286132933:AAGTxMXlBVFF62KeED_pnKodc6K3lrc1Hqs"}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        print("📤 Alert sent:", response.status_code)
    except Exception as e:
        print("⚠️ Telegram error:", str(e))


# ⚙️ Интеллектуальный анализ контекста (O3 reasoning: Orient phase)
def analyze_context(threat, temp, condition):
    risk_score = 0
    reasons = []

    if threat == 1:
        risk_score += 2
        reasons.append("🧠 ML predicted a threat.")

    if temp > 10:
        risk_score += 1
        reasons.append("🌡 High temperature detected.")

    if condition == 1:
        risk_score += 1
        reasons.append("🔥 Condition indicates 'high'.")

    if risk_score >= 3:
        level = "HIGH"
    elif risk_score == 2:
        level = "MEDIUM"
    elif risk_score == 1:
        level = "LOW"
    else:
        level = "NORMAL"

    return level, reasons

@app.route('/cloud', methods=['POST'])
@app.route('/cloud', methods=['POST'])
def cloud_layer():
    try:
        data = request.json

        context = {
            "source": "Fog Layer",
            "threat_type": data.get("Threat_Prediction"),
            "device_temp": data.get("Fridge_Temperature"),
            "condition": data.get("Temp_Condition")
        }

        level, reasons = analyze_context(
            data.get("Threat_Prediction"),
            data.get("Fridge_Temperature"),
            data.get("Temp_Condition")
        )

        # 🔎 Decide phase
        decision = "No action needed"
        if level == "LOW":
            decision = "📝 Log only"
        elif level == "MEDIUM":
            decision = "🔔 Notify security officer"
        elif level == "HIGH":
            decision = "❌ Block device + notify admin"

        # ✅ Act phase
        actions_taken = []
        if "notify" in decision:
            actions_taken.append("Sent Telegram alert")
            alert_msg = f"🚨 Alert Level: {level}\nReasons:\n" + "\n".join(reasons) + f"\n\nDecision: {decision}\nContext: {context}"
            send_telegram_alert(alert_msg)
        if "block" in decision:
            actions_taken.append("Device blocked (simulated)")
        if "Log" in decision or level == "NORMAL":
            actions_taken.append("Logged to system")

        return jsonify({
            "status": "processed",
            "alert_level": level,
            "reasons": reasons,
            "decision": decision,
            "actions": actions_taken,
            "context": context
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📥 Простой upload-эндпоинт 
@app.route('/upload', methods=['POST'])
def upload_endpoint():
    try:
        data = request.json
        print("📦 Получены данные от fog_layer:", data[:1])  # лог только первой записи
        return jsonify({"status": "received", "count": len(data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=7000, debug=True)
