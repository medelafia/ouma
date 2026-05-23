from utils.env_factory import get_config 
from slack_sdk import WebClient


TOKEN = get_config("SLACK_TOKEN") 
SLACK_CHANNEL = get_config("SLACK_CHANNEL") 
SLACK_USER = get_config("SLACK_USER")
client = WebClient(token=TOKEN)



def send_slack_message(message) : 
    client.chat_postMessage(
        channel=SLACK_CHANNEL, 
        text=message,
        username=SLACK_USER
    )