# SpeedTest Daily - Mastodon Bot

SpeedTest Daily is a Mastodon bot that posts a random speedtest.net result every day. 

<a rel="me" href="https://mastodon.online/@SpeedtestDaily" target="_blank">![Mastodon Follow](https://img.shields.io/mastodon/follow/109502147114279183?domain=mastodon.online)</a>

## Features
- Automatically performs a random speedtest.net test daily.
- Posts the result to a Mastodon instance with an entertaining caption.
- Fully configurable via environment variables.
- Can be run locally or inside a Docker container.

---

## Setup Instructions

### Prerequisites
To run this bot, you'll need:
1. A Mastodon account and API key.
2. Access to an Open WebUI instance and its API key.

### Environment Variables
The following environment variables are required for the bot to function. You can configure these in a `.env` file or pass them directly as Docker environment variables using the `-e` flag.

| Variable                   | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `OPEN_WEBUI_URL`           | The URL of your Open WebUI instance.                                       |
| `OPEN_WEBUI_TOKEN`         | API token for authenticating with Open WebUI.                              |
| `OPEN_WEBUI_MODEL`         | The model to use when generating captions.                                 |
| `MASTODON_INSTANCE`        | The Mastodon instance URL (e.g., `https://mastodon.social`).               |
| `MASTODON_TOKEN`           | API token for authenticating with Mastodon.                                |
| `NUM_RECENT_CAPTIONS_IN_PROMPT` | Number of recent captions to use for inspiration when generating new ones. |
| `DAILY_RUN_TIME`           | The time for the daily run in `HH:MM` format (e.g., `12:45`).              |
| `MODE`                     | Set to `debug` or `production` to control output behavior.                 |

Refer to the [`.env.example`](./.env.example) file for an example configuration.

---

## Running the Bot

### Using Docker
The Docker image for this bot is available at `ghcr.io/larvenstein/speedtestdaily:latest`. 

1. Pull the Docker image:
   ```bash
   docker pull ghcr.io/larvenstein/speedtestdaily:latest
   ```
2. Run the container:
   ```bash
   docker run -e OPEN_WEBUI_URL=<your_open_webui_url> \
              -e OPEN_WEBUI_TOKEN=<your_open_webui_token> \
              -e OPEN_WEBUI_MODEL=<your_model> \
              -e MASTODON_INSTANCE=<your_mastodon_instance> \
              -e MASTODON_TOKEN=<your_mastodon_token> \
              -e NUM_RECENT_CAPTIONS_IN_PROMPT=10 \
              -e DAILY_RUN_TIME="12:45" \
              -e MODE=production \
              ghcr.io/larvenstein/speedtestdaily:latest
   ```
   Replace `<...>` with your actual values.

### Running Locally
1. Create and modify `.env`
    ```bash
    cp .env.example .env
    ```
    Fill in the fields in .env
    
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
