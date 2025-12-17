import requests
import sys

# Вставьте сюда ваш BOT_TOKEN и URL от Railway
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
RAILWAY_URL = "YOUR_RAILWAY_URL_HERE"  # Например: https://your-app.up.railway.app

def setup_webhook():
    """Устанавливает webhook для бота"""
    webhook_url = f"{RAILWAY_URL}/{BOT_TOKEN}"
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    
    response = requests.post(api_url, json={"url": webhook_url})
    result = response.json()
    
    if result.get('ok'):
        print(f"✅ Webhook успешно установлен!")
        print(f"URL: {webhook_url}")
    else:
        print(f"❌ Ошибка: {result}")

def check_webhook():
    """Проверяет текущий webhook"""
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(api_url)
    result = response.json()
    
    print("\n📋 Информация о webhook:")
    print(f"URL: {result['result'].get('url', 'Не установлен')}")
    print(f"Pending updates: {result['result'].get('pending_update_count', 0)}")
    
if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or RAILWAY_URL == "YOUR_RAILWAY_URL_HERE":
        print("⚠️ Сначала замените YOUR_BOT_TOKEN_HERE и YOUR_RAILWAY_URL_HERE на реальные значения!")
        sys.exit(1)
    
    setup_webhook()
    check_webhook()
