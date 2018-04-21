import configparser
import os
import time
import re

from slackclient import SlackClient

config = configparser.ConfigParser()
config.read('config.ini')
slack_client = SlackClient(config['SLACK']['oauth_key'])

dmbot_id = None

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "current xp"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == dmbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "The party's current XP is 2,926, putting you at level 4. You're 3,574xp away from level 5"

    if command.startswith('tldr'):
        response = "APR 17 TLDR: Pressed onward up River Shosenstar. Sid spotted a beheaded corpse in red robes, Udril shared his knowledge of the Red Wizards of Thay. Reached Camp Vengeance and found it destroyed, continued overland. Were accosted by the Flaming Fist and forced to pay a bribe. Climbed the cliff and had a sweeping view of the Aldani Basin. Reached Mbala and met the witch doctor Nanny Pu'pu, who was definitely more than she let on. She told of Rite of Stolen Life, the yuan-ti, Dendar the Night Serpent, and Ras Nsi. Asked the party to wipe out the pterafolk nest in exchange for more information."

    if 'next session' in command:
        response = 'The next session is Tuesday April 17 at 6pm.'

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )
if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("DM Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        dmbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")


