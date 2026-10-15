from flask import request, jsonify, after_this_request
import threading
import requests


botID = '8568183583:AAGUdyl8zFki1Wj5jX9JXS7LGtENgYmpVPk'
adminID = '5235744796'


def send_telegram_message(text: str):
    """Отправка в фоновом потоке (не блокирует ответ)"""
    def _send():
        try:
            url = f"https://api.telegram.org/bot{botID}/sendMessage"
            payload = {
                'chat_id': adminID,
                'text': text,
                'parse_mode': 'HTML'
            }
            # Уменьшаем таймаут — если не ответит за 3 сек, забиваем
            requests.post(url, json=payload, timeout=3)
        except Exception as e:
            pass

    # Запускаем в отдельном потоке
    thread = threading.Thread(target=_send, daemon=True)
    thread.start()