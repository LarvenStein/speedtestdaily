from helpers.mastodon_helper import get_recent_captions
from bs4 import BeautifulSoup
import requests

def generate_caption(
        OPEN_WEBUI_URL, 
        OPEN_WEBUI_TOKEN, 
        OPEN_WEBUI_MODEL, 
        NUM_RECENT_CAPTIONS_IN_PROMPT, 
        MS,
        MS_ID,
        test_values
    ):

    prompt = build_prompt(NUM_RECENT_CAPTIONS_IN_PROMPT, MS, MS_ID, test_values)

    url = f"{OPEN_WEBUI_URL}/api/chat/completions"
    headers = {
        'Authorization': f'Bearer {OPEN_WEBUI_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
      "model": OPEN_WEBUI_MODEL,
      "messages": [
        {
          "role": "user",
          "content": prompt
        }
      ]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def build_prompt(NUM_RECENT_CAPTIONS_IN_PROMPT: int, MS, MS_ID, test_values):
    caption = "You are a twitter bot that posts a picture of a random speedtest.net result every day.\n" 
    caption += f"Todays result is {test_values['download']} mbps download, {test_values['upload']} mbps upload and {test_values['ping']} ms ping. You do not need to include these values, but you can. Remember: this is a result of a random speedtest from a stranger, they dont know you, you dont know them.\n"
    caption += "Please write an entertaining caption for that result. You can also be mean to bad results or be sarcastic. Please keep it straight to the point, do not include hashtags, do not include links!\n"
    caption += "You can take slight inspiration from these ones, you wrote in the past, if you want, but change it up!\n"

    past_captions = get_recent_captions(NUM_RECENT_CAPTIONS_IN_PROMPT, MS, MS_ID)

    for past_caption in past_captions:
        soup = BeautifulSoup(past_caption['content'], 'html.parser')
        caption += f"- {soup.get_text()}\n"

    caption += "Just respond with the caption, nothing else."

    return caption
