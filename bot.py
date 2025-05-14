import time
import os
from dotenv import load_dotenv
from helpers.speedtest_utils import *
from helpers.id_manipulation import *
from helpers.detail_scraping import get_speed_values
from helpers.generate_captions import generate_caption
from helpers.mastodon_helper import make_post
from mastodon import Mastodon

# Read env
load_dotenv()

OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL")
OPEN_WEBUI_TOKEN = os.getenv("OPEN_WEBUI_TOKEN")
OPEN_WEBUI_MODEL = os.getenv("OPEN_WEBUI_MODEL")
MASTODON_INSTANCE = os.getenv("MASTODON_INSTANCE")
MASTODON_TOKEN = os.getenv("MASTODON_TOKEN")
NUM_RECENT_CAPTIONS_IN_PROMPT = int(os.getenv("NUM_RECENT_CAPTIONS_IN_PROMPT", 10))
MODE = os.getenv("MODE", "production")

# init Mastodon
mastodon = Mastodon(
    access_token=MASTODON_TOKEN,
    api_base_url=MASTODON_INSTANCE
)
ms = mastodon.account_verify_credentials()
ms_id = ms['id']

# Get a speedtest id
speedtest_id = get_speedtest_id()

test_id = randomize_test_id(speedtest_id)
test_image = generate_image_url(test_id)
test_url = generate_test_url(test_id)

time.sleep(4) # Wait for URL to actually exsist

test_values = get_speed_values(test_url) # Scrape tests values

# Generate a caption
caption_raw = generate_caption(
            OPEN_WEBUI_URL, 
            OPEN_WEBUI_TOKEN, 
            OPEN_WEBUI_MODEL, 
            NUM_RECENT_CAPTIONS_IN_PROMPT, 
            mastodon,
            ms_id,
            test_values
        )

caption = caption_raw['choices'][0]['message']['content']

# Actually post it (or not)
if(MODE == "debug"):
    print(f"Test-url: {test_url}")
    print(f"Test-values: {test_values['download']} mbps download, {test_values['upload']} mbps upload, {test_values['ping']} ms ping")
    print(f"Caption: {caption}")

if(MODE == "production"):
    make_post(mastodon, caption, test_image)