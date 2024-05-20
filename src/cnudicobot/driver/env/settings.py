from dotenv import load_dotenv
import os


load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")
discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")
cnu_base_url = os.getenv("BASE_URL")
cnu_front_url = os.getenv("FRONT_URL")
