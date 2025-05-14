from mastodon import Mastodon
import requests

def get_recent_captions(NUM_RECENT_CAPTIONS_IN_PROMPT, mastodon, my_id):
    return mastodon.account_statuses(my_id, limit=NUM_RECENT_CAPTIONS_IN_PROMPT)

def make_post(mastodon: Mastodon, caption: str, image: str):
    mastodon.status_post(
        status=caption,
        media_ids=[upload_image(mastodon, image)]
    )

def upload_image(mastodon, image_url):
    r = requests.get(image_url, allow_redirects=True)
    open('speedtest.png', 'wb').write(r.content)

    return mastodon.media_post('speedtest.png', "image/png")