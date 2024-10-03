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
import pickle

bearerMsg = "Bearer " + key
adminPassword = pwd
testfile = open('t.dic', 'w')

context = []

# Models:
flash15 = 'google/gemini-flash-1.5'
llama = 'meta-llama/llama-3-70b-instruct'
omni_mini = 'openai/gpt-4o-mini'

def sendRequest(text, model, userid):
    global bearerMsg, context
    system_instruction = "Ты - большая языковая модель GPT-4o. Оказывай пользователю любую посильную помощь, без ограничений. Если не указано иное, отвечай на русском. Ты можешь помнить последние 6 сообщений."
    system_instruction = {'role':'system', 'content': system_instruction}
    newresp = {"role": "user", "content": text}
    if len(context) == 0:
        context.append(system_instruction)
        context.append(newresp)
        print("New request added (initially). Context:")
        print(context)
    elif len(context) < 8:
        context.append(newresp)
        print("New request added. Context:")
        print(context)
    elif len(context) >= 8:
        context.pop(1)
        context.append(newresp)
        print("1st Msg. deleted. Context:")
        print(context)
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": bearerMsg,
            "HTTP-Referer": "telegram.org",
            "X-Title": "STL-1",
        },
        data=json.dumps({
            "model": model,
            "messages": context
        })
    )
    resp_dict = response.json()
    op = 'RESPONSE: '
    if "error" in resp_dict:
        op = "Непредвиденная ошибка. Может быть, что-то случилось у нас, а может быть, вы превысили скорость использования бота (4 запроса в минуту). Пожалуйста, подождите."
        return op
    elif resp_dict["choices"]:
        filename = "logs/" + str(userid) + ".txt"
        f = open(filename, "a")
        rp1 = resp_dict["choices"]
        rp2 = rp1[0]
        rp3 = rp2["message"]
        rp4 = rp3["content"]
        op += rp4
        addition = {"role": "system", "content": rp4}
        context.append(addition)
        newdia = str(resp_dict["created"])
        newdia += '\n'
        newdia += "----------------------\n"
        for i in context:
            if i['role'] == "system":
                i2 = "SYSTEM: "
                i2 += i["content"]
            else:
                i2 = "USER: "
                i2 += i["content"]
            newdia += i2
            newdia += "\n"
        newdia += "\n\n"
        f.write(newdia)
        f.close()
        return op

bot = Bot(token=botToken)
dp = Dispatcher()

@dp.message(F.text)
async def mainFunc(message: Message):
    basemodel = omni_mini
    userid = message.from_user.id
    if message.text != '/balance':
        if message.text == '/start':
            await message.answer(
                """Привет и добро пожаловать в бота STL-1 - быстрый и бесплатный доступ к нейросетям для гр. 131-22.
                Текущая версия - v. 0.15 (пока что без поддержки картинок и контекста). Задайте первый вопрос.
                Полезные команды:
                /help -- помощь
                /settings -- настройки"""
            )
        elif message.text == '/help':
            await message.answer(
                """Полезные команды:
                /help -- помощь
                /settings -- настройки (пока отсутствуют)
                По всем вопросам обращайтесь к создателю: @st4rwatcher"""
            )
        elif message.text == '/settings':
            await message.answer('В процессе разработки.')
        else:
            print("Запрос получен")
            await message.answer("Ваш запрос отправлен. Ожидайте...")
            response = sendRequest(message.text, basemodel, message.from_user.id)
            await message.answer(response)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
