import time
import os
import schedule
import logging
from dotenv import load_dotenv
from helpers.speedtest_utils import *
from helpers.id_manipulation import *
from helpers.detail_scraping import get_speed_values
from helpers.generate_captions import generate_caption
from helpers.mastodon_helper import make_post
from mastodon import Mastodon

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("scheduler.log")
    ]
)
logger = logging.getLogger(__name__)

def run_speedtest():
    logger.info("Starting scheduled speedtest run...")
    
    try:
        # Read env
        OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL")
        OPEN_WEBUI_TOKEN = os.getenv("OPEN_WEBUI_TOKEN")
        OPEN_WEBUI_MODEL = os.getenv("OPEN_WEBUI_MODEL")
        MASTODON_INSTANCE = os.getenv("MASTODON_INSTANCE")
        MASTODON_TOKEN = os.getenv("MASTODON_TOKEN")
        NUM_RECENT_CAPTIONS_IN_PROMPT = int(os.getenv("NUM_RECENT_CAPTIONS_IN_PROMPT", 10))
        MODE = os.getenv("MODE", "debug")
        
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
        
        logger.info(f"Got speedtest ID: {test_id}")
        
        # Wait for URL to actually exist
        time.sleep(4)
        
        # Scrape test values
        test_values = get_speed_values(test_url)
        logger.info(f"Test values: {test_values}")
        
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
        caption += f"\n{test_url}"
        
        # Actually post it (or not)
        if MODE == "debug":
            logger.info(f"Test-url: {test_url}")
            logger.info(f"Test-values: {test_values['download']} mbps download, {test_values['upload']} mbps upload, {test_values['ping']} ms ping")
            logger.info(f"Caption: {caption}")
        elif MODE == "production":
            logger.info("Posting to Mastodon...")
            make_post(mastodon, caption, test_image)
            logger.info("Post successful!")
        
        logger.info("Scheduled run completed successfully")
    except Exception as e:
        logger.error(f"Error during scheduled run: {str(e)}", exc_info=True)

if __name__ == "__main__":
    logger.info("Starting scheduler...")
    
    # Load environment variables
    load_dotenv()
    DAILY_RUN_TIME = os.getenv("DAILY_RUN_TIME", "12:45")
    MODE = os.getenv("MODE", "production")
    
    if MODE == "debug":
        # In debug mode, just run once and exit
        logger.info("Debug mode: Running single test and exiting...")
        run_speedtest()
        logger.info("Debug run completed, exiting.")
    else:
        # In production mode, set up scheduling
        logger.info(f"Production mode: Scheduling daily runs at {DAILY_RUN_TIME}")
        schedule.every().day.at(DAILY_RUN_TIME).do(run_speedtest)
                
        # Keep the script running with the scheduler
        logger.info("Scheduler running, waiting for scheduled time...")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute