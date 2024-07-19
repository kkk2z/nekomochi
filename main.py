import revolt
import asyncio
import sqlite3
from transformers import AutoModelForCausalLM, AutoTokenizer
import schedule
import time
import requests
import subprocess

# モデルとトークナイザの読み込み
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# データベース接続とテーブル作成
conn = sqlite3.connect('chat_logs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chat_logs (id INTEGER PRIMARY KEY, user_input TEXT, bot_response TEXT)''')

def save_chat_log(user_input, bot_response):
    c.execute("INSERT INTO chat_logs (user_input, bot_response) VALUES (?, ?)", (user_input, bot_response))
    conn.commit()

async def generate_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

class MyBot(revolt.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message: revolt.Message):
        if message.author.bot:
            return

        if message.content.startswith('/ねこもち'):
            user_input = message.content[len('/ねこもち'):].strip()
            response = await generate_response(user_input)
            await message.channel.send(response)
            save_chat_log(user_input, response)

def train_model():
    subprocess.run(["python", "train_model.py"])

def schedule_training():
    schedule.every().day.at("00:00").do(train_model)

async def main():
    token = "YOUR_BOT_TOKEN"  # Revolt Botのトークンをここに入力
    bot = MyBot()
    await bot.start(token)

    schedule_training()
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

asyncio.run(main())
import revolt
import asyncio
import sqlite3
from transformers import AutoModelForCausalLM, AutoTokenizer
import schedule
import time
import requests
import subprocess

# モデルとトークナイザの読み込み
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# データベース接続とテーブル作成
conn = sqlite3.connect('chat_logs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chat_logs (id INTEGER PRIMARY KEY, user_input TEXT, bot_response TEXT)''')

def save_chat_log(user_input, bot_response):
    c.execute("INSERT INTO chat_logs (user_input, bot_response) VALUES (?, ?)", (user_input, bot_response))
    conn.commit()

async def generate_response(user_input):
    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

class MyBot(revolt.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_message(self, message: revolt.Message):
        if message.author.bot:
            return

        if message.content.startswith('/ねこもち'):
            user_input = message.content[len('/ねこもち'):].strip()
            response = await generate_response(user_input)
            await message.channel.send(response)
            save_chat_log(user_input, response)

def train_model():
    subprocess.run(["python", "train_model.py"])

def schedule_training():
    schedule.every().day.at("00:00").do(train_model)

async def main():
    token = "YOUR_BOT_TOKEN"  # Revolt Botのトークンをここに入力
    bot = MyBot()
    await bot.start(token)

    schedule_training()
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

asyncio.run(main())
