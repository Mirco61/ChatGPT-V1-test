import os
from flask import Flask, redirect, request
from threading import Thread

app = Flask(__name__)

# Discord-Anwendungsdetails
CLIENT_ID = '1097631848466751518'
CLIENT_SECRET = os.environ['CLIENT_SECRET']
REDIRECT_URI = 'https://discord.com/ChatGPT-V1'

# Scope für die Berechtigungen
scope = 'identify guilds rpc.voice.read gdm.join rpc.video.write messages.read voice applications.commands.permissions.update activities.read applications.commands rpc.activities.write email guilds.join rpc rpc.voice.write bot rpc.screenshare.read applications.store.update dm_channels.read activities.write applications.builds.upload role_connections.write relationships.read applications.entitlements applications.builds.read webhook.incoming rpc.video.read rpc.screenshare.write rpc.notifications.read guilds.members.read connections'

# OAuth2-Endpunkte
AUTHORIZATION_URL = f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={scope}'
TOKEN_URL = 'https://discord.com/api/oauth2/token'
USER_URL = 'https://discord.com/api/users/@me'

@app.route('/')
def index():
    return redirect(AUTHORIZATION_URL)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"Code: {code}")  # Hinzugefügt
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': scope
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Token-Endpunkt aufrufen, um Access Token zu erhalten
    response = request.post(TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    token = response.json()['access_token']
    print(f"Token: {token}")  # Hinzugefügt

    # Access Token verwenden, um Benutzerinformationen abzurufen
    headers = {'Authorization': f'Bearer {token}'}
    response = request.get(USER_URL, headers=headers)
    response.raise_for_status()
    user = response.json()
    print(f"User: {user}")  # Hinzugefügt

    # Benutzerinformationen anzeigen
    return f'Willkommen, {user["username"]}#{user["discriminator"]}!'

def run_app():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    t = Thread(target=run_app)
    t.start()

