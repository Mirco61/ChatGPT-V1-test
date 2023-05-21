import openai
import discord
import os
from dotenv import load_dotenv
from discord_oauth import run_app

# Laden des OpenAI API-Schlüssels aus der Umgebungsvariable
openai.organization = "org-qzUScDWpsWoEv03Im9FZBKHQ"
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN1')

# Erstellen einer Discord-Bot-Instanz
intents = discord.Intents.default()
intents.members = True  # Aktiviere den members-Intent
client = discord.Client(intents=intents)

@client.event
async def on_connect():
    print(f'{client.user} has connected to the Discord Gateway!')

    


@client.event
async def on_disconnect():
    print(f'{client.user} has disconnected from the Discord Gateway!')





@client.event
async def on_message(message):
    # Überprüfen, ob die Nachricht von einem Benutzer stammt und nicht von einem Bot
    if message.author.bot:
        return

    # Generieren von Text mit der OpenAI API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent."},
            {"role": "user", "content": message.content}
        ],
        temperature=0.7,
        max_tokens=3000,
    )

    # Senden der generierten Antwort als Nachricht zurück an den Benutzer
    response_text = completion.choices[0].message['content']
    await message.channel.send(response_text)

import threading

# ...

def run_bot():
    client.run(TOKEN)

def run_flask_app():
    run_app()

bot_thread = threading.Thread(target=run_bot)
flask_thread = threading.Thread(target=run_flask_app)

bot_thread.start()
flask_thread.start()

