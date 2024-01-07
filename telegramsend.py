from telegram import Bot
import credentials
async def send(message):
    bot = Bot(token=credentials.updater)
    await bot.send_message(chat_id=credentials.chatid, text=message)
