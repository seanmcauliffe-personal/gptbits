import requests
import time
import random
from datetime import datetime
from textblob import Word

# Azure app details
CONFIG = {
    'TENANT_ID': 'your_tenant_id',
    'CLIENT_ID': 'your_client_id',
    'CLIENT_SECRET': 'your_client_secret',
    'TEAM_ID': 'your_team_id',
    'CHANNEL_ID': 'your_channel_id'
}

REMINDERS = [
    ["Good morning! Remember to start your day with a healthy breakfast and hydration. It's the fuel your body needs to have a productive day."],
    ["Set your goals for the day. What are the top 3 things you want to accomplish today? Write them down."],
    ["Remember to maintain good posture. Adjust your chair and desk height to ensure you're comfortable and your back is supported."],
    ["Time for a quick exercise break! Try doing a few stretches or a quick yoga routine to get your blood flowing."],
    ["Lunchtime! Step away from your work station and have a balanced meal. Don't forget to hydrate."],
    ["Have you been working on the same task for a while? Try switching tasks to keep your mind fresh."],
    ["Take a moment to practice mindfulness. A quick meditation or deep breathing exercise can help reduce stress."],
    ["Great job today! Start wrapping up your tasks for the day. Remember to take some time to relax and do something you enjoy after work."]
]

def get_access_token(config):
    url = f'https://login.microsoftonline.com/{config["TENANT_ID"]}/oauth2/v2.0/token'
    data = {
        'grant_type': 'client_credentials',
        'client_id': config["CLIENT_ID"],
        'client_secret': config["CLIENT_SECRET"],
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, data=data)
    response.raise_for_status()  # ensure we got a valid response
    return response.json()['access_token']

def send_message(config, access_token, content):
    url = f'https://graph.microsoft.com/v1.0/teams/{config["TEAM_ID"]}/channels/{config["CHANNEL_ID"]}/messages'
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    json = {
        'body': {
            'contentType': 'text',
            'content': content
        }
    }
    response = requests.post(url, headers=headers, json=json)
    response.raise_for_status()  # ensure the message was sent successfully

def randomize_phrase(phrase):
    words = phrase.split()
    new_words = [Word(random.choice([word, word.pluralize()])).lemmatize() for word in words]
    return " ".join(new_words)

def maintain_active_status(config):
    while True:
        try:
            current_hour = datetime.now().hour
            if 8 <= current_hour <= 15:
                access_token = get_access_token(config)
                reminder = random.choice(REMINDERS[current_hour - 8])
                randomized_reminder = randomize_phrase(reminder)
                send_message(config, access_token, randomized_reminder)

            # Wait for the nextI apologize for the cutoff. Here is the rest of the code:

```python
            # Wait for the next hour
            minutes_to_next_hour = 60 - datetime.now().minute
            time.sleep(minutes_to_next_hour * 60)

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(10)
            continue

maintain_active_status(CONFIG)
