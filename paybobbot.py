import time
import telepot

from telepot.loop import MessageLoop
from controllers.parse_message import parse_handler

# Initial setup
paybot = telepot.Bot("609295389:AAE3hBianx4PMwhd6UkdAC2TawKb2MpSZd4")
paybot.getUpdates(offset=100)

def receiver(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        parse_handler(chat_id, msg["chat"], msg['text'])

# Run loop
MessageLoop(paybot, receiver).run_as_thread()

while 1:
    time.sleep(100)
