import configparser
import gsheet_reader
import os
import time
import re

from slackclient import SlackClient

config = configparser.ConfigParser()
config.read('config.ini')
slack_client = SlackClient(config['SLACK']['oauth_key'])

dmbot_id = None

RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "whois list"
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
    print('Found command {} in {}'.format(command, channel))
    # Default response is help text for the user
    default_response = '''Not sure what you mean. Try one of the following:\n
        `tldr Apr 21` (date optional)\n
        `current xp`\n
        `who is Ras Nsi`\n
        `who is list`
        '''

    # Finds and executes the given command, filling in response
    response = None
    
    if command.lower().startswith('current xp') or command.lower().startswith('xp'):
        xp_resp = gsheet_reader.current_xp()
        response = "The party's current XP is {}, putting you at level {}. You need {}xp more to level up".format(xp_resp[0], xp_resp[1], xp_resp[2])

    if command.lower().startswith('tldr'):
        session_date = None
        if len(command) > 4:
            session_date = command[4:].strip()
        tldr = gsheet_reader.read_tldr(session_date)
        response = 'TLDR for ' + tldr[0] + ': \n' + tldr[1] 

    if command.lower().startswith('who'):
        search_name = 'list'
        if len(command.strip()) > 5:
            search_name = command[6:].strip()
        response = gsheet_reader.whois(search_name)


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


