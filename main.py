import os
from background import keep_alive #импорт функции для поддержки работоспособности
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, executor
import time
import schedule
import datetime
#ДЛЯ VERCEL
from http.server import BaseHTTPRequestHandler, HTTPServer
class TelegramWebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Ваш код обработки входящего веб-хука от Telegram
        pass
#ДЛЯ VERCEL
bot = Bot(token='5948169074:AAGwiVPPIqbFhzwxYj9HnjukeFHyo4zWvW8')
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)




#ПРИВЕТСТВИЕ 
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.reply(f"Отбъебись уже от меня, {user_full_name}!")





#ЗАПРОС О ПРАЗДНИКАХ ОТ ЧЛЕНА БЕСЕДЫ
@dp.message_handler(commands=['holiday'])
async def process_start_command(message: types.Message):
  dayNow = 'q' + str(datetime.datetime.now().day) +       str(datetime.datetime.now().month)
  with open('holyday.txt', encoding='utf-8') as f:
    text = f.read()
  start_index = text.find(str(dayNow))  # Находим индекс начала подстроки
  end_index = text.find('/'+dayNow)  # Находим индекс конца подстроки
  result = text[start_index+5:end_index]# Извлекаем подстроку
  #СЛЕДУЮЩИЙ ПРАЗДНИК
  nextHolyday = -1
  nextDay = int(dayNow[1:len(dayNow)])%10 + 1
  nextMonth = int(datetime.datetime.now().month)
  while text.find(str(nextHolyday)) == -1:#пока не найдена дата
    while text.find(str(nextHolyday)) == -1:
      nextHolyday = 'q' + str(nextDay) + str(nextMonth)
      if nextDay + 1 > 31:
        nextDay = 1
        nextMonth = int(datetime.datetime.now().month)+1
        nextHolyday = 'q' + str(nextDay) + str(nextMonth)
        break
      nextDay = int(nextDay) + 1
    if datetime.datetime.now().month > 12:
      break

  if start_index == -1 or end_index == -1:
    await message.reply(f"Сегодня нет никаких праздников:)")
    start_index = text.find(str(nextHolyday))  # Находим индекс начала подстроки
    end_index = text.find('/'+nextHolyday)  # Находим индекс конца подстроки
    await message.reply(f"Следующий праздник: {text[start_index+5:end_index]}")
  else:
    await message.reply(f"{result}")






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
keep_alive()#запускаем flask-сервер в отдельном потоке
bot.polling(non_stop=True, interval=0) #запуск бота
#ДЛЯ VERCEL
server = HTTPServer(('', 8000), TelegramWebhookHandler)
server.serve_forever()
#ДЛЯ VERCEL