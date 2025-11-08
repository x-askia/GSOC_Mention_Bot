import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration Loaded from .env ---
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
TARGET_CHANNEL_ID = os.environ.get("TARGET_CHANNEL_ID")
USER_GROUP_NAME = os.environ.get("USER_GROUP_NAME")
# -----------------------------------------

# Initializes your app with your bot token
app = App(token=SLACK_BOT_TOKEN)

# This handler now listens to ALL messages in channels the bot is in
#@app.message(f"@{USER_GROUP_NAME}")
@app.message("gsoc-test")
def handle_user_group_mention(message, say):
    # Get details from the message to create a link
    channel_id = message["channel"]
    message_ts = message["ts"]
    team_id = message.get("team") # Use .get() for safety
    user_id = message["user"]
    original_text = message["text"]

    # Construct the permalink to the original message
    message_link = f"https://app.slack.com/client/{team_id}/{channel_id}/thread/{message_ts}"

    # Re-post a formatted message to the target channel
    say(
        channel=TARGET_CHANNEL_ID,
        text=f"New @{USER_GROUP_NAME} mention from <@{user_id}> in <#{channel_id}>:\n>>> {original_text}\n\n<{message_link}|Jump to message>"
    )

# Start your app using Socket Mode
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()