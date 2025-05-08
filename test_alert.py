import requests

def send_telegram_alert(message):
    token = "7286132933:AAGTxMXlBVFF62KeED_pnKodc6K3lrc1Hqs"
    chat_id = 699941829  # <-- ВСТАВЬ СЮДА СВОЙ CHAT ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, data=data)
    print("Status:", response.status_code)
    print("Response:", response.text)

send_telegram_alert("🚨 Тестовое сообщение от твоей системы безопасности!")
