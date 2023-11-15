import os
api_id = os.getenv("telegram_api_id_my_number")  # введите API ID вашего приложения
api_hash = os.getenv("telegram_api_hash_my_number")  # введите API Hash вашего приложения
print(api_id)
print(api_hash)

phone = os.getenv("my_phone")

# user_id = 517074614 # id моего основного номера
# CHANNEL_ID = -1001988058850 # id моего канала Мониторинг сети/Мониторинг телефонии
CHANNEL_ID = 517074614 # id моей второй симки
