import os
import requests
from datetime import datetime

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')  # Ваш Telegram ID

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

def get_updates(offset=None):
    """Получение обновлений от Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"offset": offset, "timeout": 30}
    response = requests.get(url, params=params)
    return response.json()

def process_updates():
    """Обработка всех новых сообщений"""
    updates = get_updates()
    
    if not updates.get('result'):
        return
    
    for update in updates['result']:
        if 'message' not in update:
            continue
            
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
Мы обязательно их рассмотрим. 💡

Просто напишите ваше сообщение, и мы его получим!
            """
            send_message(chat_id, welcome_text)
        
        # Пересылка всех сообщений админу (кроме /start)
        elif text:
            notify_admin(user, text)
            
            # Подтверждение пользователю
            confirmation = "✅ Спасибо! Ваше сообщение получено и передано администратору."
            send_message(chat_id, confirmation)

if __name__ == "__main__":
    process_updates()
