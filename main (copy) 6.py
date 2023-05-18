import openai
import discord
import os
from server import stay_alive

# Laden des OpenAI API-Schlüssels aus der Umgebungsvariable
openai.organization = "org-qzUScDWpsWoEv03Im9FZBKHQ"
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key
stay_alive()
# Erstellen einer Discord-Bot-Instanz
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Event-Handler, der auf eine eingehende Nachricht reagiert
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
        max_tokens=3000
        ,)

  

    # Senden der generierten Antwort als Nachricht zurück an den Benutzer
    response_text = completion.choices[0].message['content']
    await message.channel.send(response_text)

    
   


# Starten des Discord-Bots
client.run(os.environ['DISCORD_TOKEN1'])









