# GSOC_Mention_Bot
Slack Bot that sends every @GSOC mention in a slack channel
Of course. Here is the README for the Python bot, formatted for a plain text file.

```text
GSOC MENTION FORWARDER BOT 🤖
=============================

This is a simple, self-hosted Python Slack bot that listens for mentions of a specific user group (e.g., @gsoc) in any channel it's a member of. When a mention is detected, it forwards a formatted summary of the message to a single, designated "feed" channel for easy collation and tracking.

--------------------------------------------------

FEATURES
--------
* Listens in real-time for @app_mention events using Slack's Socket Mode.
* Collates mentions from multiple channels into one centralized feed.
* Includes a convenient link back to the original message for full context.
* Securely loads credentials from an .env file.

--------------------------------------------------

SETUP AND CONFIGURATION
-----------------------

Follow these steps to get your bot running.

1. Project Files
~~~~~~~~~~~~~~~~
Create a dedicated folder for this project and place the following three files inside it.

File: requirements.txt
    slack_bolt
    python-dotenv

File: .env
    # Get this from the "OAuth & Permissions" page, starts with "xoxb-"
    SLACK_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"

    # Get this from the "Basic Information" page under "App-Level Tokens", starts with "xapp-"
    SLACK_APP_TOKEN="YOUR_APP_LEVEL_TOKEN_HERE"

File: bot.py
    import os
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Initializes your app with your bot token and app-level token
    app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

    # --- IMPORTANT ---
    # You must edit this line with the channel ID for your feed channel.
    # To get the ID: right-click the channel name in Slack -> Copy -> Copy link.
    # The ID is the string that starts with 'C', e.g., "C04B123XYZ".
    TARGET_CHANNEL_ID = "YOUR_TARGET_CHANNEL_ID_HERE"

    # This function listens for any time the bot is mentioned
    @app.event("app_mention")
    def handle_mention(event, say):
        # Get details to create a link to the original message
        channel_id = event["channel"]
        message_ts = event["ts"]
        team_id = event["team"]
        user_id = event["user"]
        message_link = f"https://app.slack.com/client/{team_id}/{channel_id}/thread/{message_ts}"
        
        original_text = event["text"]

        # Re-post a formatted message to the target channel
        say(
            channel=TARGET_CHANNEL_ID,
            text=f"New @gsoc mention from <@{user_id}> in <#{channel_id}>:\n>>> {original_text}\n\n<{message_link}|Jump to message>"
        )

    # Start your app using Socket Mode
    if __name__ == "__main__":
        handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
        handler.start()


2. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~
Open a terminal in your project folder and run:

    pip install -r requirements.txt


3. Add Your Credentials
~~~~~~~~~~~~~~~~~~~~~~~
Fill in the SLACK_BOT_TOKEN and SLACK_APP_TOKEN values in your .env file. You get these from your app's pages on api.slack.com.


4. Set Your Target Channel
~~~~~~~~~~~~~~~~~~~~~~~~~~
Open bot.py and replace "YOUR_TARGET_CHANNEL_ID_HERE" with the actual ID of your feed channel.

--------------------------------------------------

USAGE
-----
1. Invite the Bot: 
   In Slack, you must invite the bot into every channel you want it to monitor, as well as the final "feed" channel where it will post the collated messages.

2. Run the Script: 
   From your terminal, run the bot with:

    python bot.py

The bot will connect and start listening. For it to run 24/7, this script needs to be running continuously on a server or VM.
```
