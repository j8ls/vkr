import os
from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')

def send_message(chat_id, text):
    """Отправка сообщения пользователю"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=data)

def notify_admin(user_info, message_text):
    """Уведомление админа о новом сообщении"""
    username = user_info.get('username', 'Без username')
    first_name = user_info.get('first_name', 'Без имени')
    user_id = user_info.get('id', 'Неизвестно')
    
    admin_text = f"""
📩 <b>Новое сообщение в бот!</b>

👤 Пользователь: {first_name}
🆔 ID: {user_id}
📱 Username: @{username}
⏰ Время: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

💬 Сообщение:
{message_text}
    """
    send_message(ADMIN_ID, admin_text)

@app.route('/', methods=['GET'])
def index():
    return "Telegram Bot is running! ✅"

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    """Обработка входящих сообщений через webhook"""
    update = request.get_json()
    
    if 'message' not in update:
        return 'ok'
    
    message = update['message']
    chat_id = message['chat']['id']
    user = message['from']
    text = message.get('text', '')
    
    # Ответ на команду /start
    if text == '/start':
        welcome_text = """
🔒 <b>Извините!</b>

К сожалению, данное исследование уже закрыто.

Но вы можете написать свои пожелания и предложения по темам для будущих постов! 
Я обязательно их рассмотрю ❤️

Просто напишите ваше сообщение здесь!
        """
        send_message(chat_id, welcome_text)
    
    # Пересылка всех сообщений админу (кроме /start)
    elif text:
        notify_admin(user, text)
        
        # Подтверждение пользователю
        confirmation = "✅ Спасибо! Ваше сообщение получено и передано администратору."
        send_message(chat_id, confirmation)
    
    return 'ok'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
