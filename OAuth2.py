import os
import requests
import redirect 


from flask import Flask

app = Flask(__name__)

# Discord-Anwendungsdetails
CLIENT_ID = '1097631848466751518'
CLIENT_SECRET = os.environ['YOUR_CLIENT_SECRET']
REDIRECT_URI = 'https://chatgpt-v1.mircohoskowetz.repl.co/callback'

# OAuth2-Endpunkte
AUTHORIZATION_URL = f'https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20email'
TOKEN_URL = 'https://discord.com/api/oauth2/token'
USER_URL = 'https://discord.com/api/users/@me'


@app.route('/')
def index():
    return redirect(AUTHORIZATION_URL)


@app.route('/callback')
def callback():
    code = requests.args.get('code')
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identify email'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Token-Endpunkt aufrufen, um Access Token zu erhalten
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    token = response.json()['access_token']

    # Access Token verwenden, um Benutzerinformationen abzurufen
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(USER_URL, headers=headers)
    response.raise_for_status()
    user = response.json()

    # Benutzerinformationen anzeigen
    return f'Willkommen, {user["username"]}#{user["discriminator"]}!'


if __name__ == '__main__':
  def run(): 
    app.run(host='0.0.0.0', port=8080)



