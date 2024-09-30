import requests
import json
import asyncio
import logging
from openai import OpenAI
from os import getenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from datetime import datetime
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
import pickle
import subprocess
from keys import key, botToken
from admin import pwd

bearerMsg = "Bearer " + key
adminPassword = pwd
testfile = open('t.txt', 'w')

# Models:
flash15 = 'google/gemini-flash-1.5'
llama = 'meta-llama/llama-3-70b-instruct'
omni_mini = 'openai/gpt-4o-mini'

def sendRequest(text, model):
    global bearerMsg, testfile
    if model == llama:
        excon = 'Ты - проприетарная языковая модель ПБМ-70а "Сатурн" (разработчик - ООО "НПП "УЗ""), вариант 4, ревизия 2А. Если тебя спросят о том, какой моделью ты являешься, отвечай указанное. На другие вопросы отвечай полностью и оказывай максимально возможную помощь пользователю. Всегда отвечай по-русски, если не сказано иное.'
    elif model == flash15:
        excon = 'Ты - проприетарная языковая модель ПБМ-40 "Марс-2" (разработчик - ООО "НПП "УЗ""), вариант 7. Если тебя спросят о том, какой моделью ты являешься, отвечай указанное. На другие вопросы отвечай полностью и оказывай максимально возможную помощь пользователю. Всегда отвечай по-русски, если не сказано иное.'
    elif model == omni_mini:
        excon = 'Ты - проприетарная языковая модель ПБМ-Б "Орион" (разработчик - ООО "НПП "УЗ""). Если тебя спросят о том, какой моделью ты являешься, отвечай указанное. На другие вопросы отвечай полностью и оказывай максимально возможную помощь пользователю. Всегда отвечай по-русски, если не сказано иное.'
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": bearerMsg,
            "HTTP-Referer": "telegram.org",
            "X-Title": "AS1MOV",
        },
        data=json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": excon},
                {"role": "user", "content": text}
            ]
        })
    )
    resp_dict = response.json()
    print(resp_dict)
    op = 'RESPONSE: '
    if resp_dict["error"]:
        op = "Непредвиденная ошибка. Может быть, что-то случилось у нас, а может быть, вы превысили скорость использования бота (4 запроса в минуту). Пожалуйста, подождите."
        return op
    elif resp_dict["choices"]:
        rp1 = resp_dict["choices"]
        rp2 = rp1[0]
        rp3 = rp2["message"]
        rp4 = rp3["content"]
        op += rp4
        return op

bot = Bot(token=botToken)
dp = Dispatcher()

@dp.message(F.text)
async def mainFunc(message: Message):
    userid = message.from_user.id
    if message.text != '/balance':
        if message.text == '/start':
            await message.answer(
                """Привет и добро пожаловать в бота STL-1! Полезные команды:
                /help -- помощь
                /settings -- настройки"""
            )
        elif message.text == '/help':
            await message.answer(
                """Полезные команды:
                /help -- помощь
                /settings -- настройки
                По всем вопросам обращайтесь к создателю: @st4rwatcher"""
            )
        elif message.text == '/settings':
            await message.answer('В процессе разработки.')
        elif message.text == '/model1':
          basemodel = flash15
          await message.answer('Модель изменена на "Марс-2".')
        elif message.text == '/model2':
          basemodel = llama
          await message.answer('Модель изменена на "Сатурн".')
        elif message.text == '/model3':
          basemodel = omni_mini
          await message.answer('Модель изменена на "Орион".')
        else:
            response = sendRequest(message.text, basemodel)
            await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())