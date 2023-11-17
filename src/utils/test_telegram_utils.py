from telethon import TelegramClient, sync
import os

#api_id и api_hash моего основного номера
api_id = os.getenv("telegram_api_id_my_number")
api_hash = os.getenv("telegram_api_hash_my_number")

client = TelegramClient('session_name', api_id, api_hash)

client.start()

user_id = 6287756332 # id моей второй симки
message = 'Test message'
image_path = r'C:\Users\User\Documents\py.detect_movement\src\utils\empty.jpg'

client.send_message(user_id, message)
client.send_file(user_id, image_path)
