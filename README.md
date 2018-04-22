# DM-bot
A slack companion for Dungeon and Dragon groups that use Slack to manage their campaigns. 
It's backed by Google Sheets, so that the DM doesn't need a huge amount of techinical work to keep things up to date.
Currently in alpha, so it must be hosted and set up as a custom Slack app

## Getting a Slack API key
1. Create a new Slack app for your team (https://api.slack.com/apps/new)
2. In the left-hand sidebar click "Bot Users", then "Add a bot user", giving the bot user a slack username (eg DMBot)
3. Under "Settings" in the left-hand sidebar, click "Install App", and install it to your workspace
4. Copy the Bot User OAuth Access Token that is provided, and paste it into the config.ini in place of `[YOUR SLACK KEY HERE]`

## Alpha Usage
1. Create a copy of [this google sheets workbook](https://docs.google.com/spreadsheets/d/1jGwyqOEg6RnzruYpHKetSH_d6Ckp5WOTxGJpIpITf8Q/edit?usp=sharing), and upadte it as needed
2. Click "File" > "Publish to the web". Change the format dropdown from "Web page" to "Comma-separated values (CSV)"
3. Click "Publish" and confirm
4. Select "Log" from the dropdown instead of "Entire Document". Copy the URL in the box and add it to the config.ini
5. Repeat step 4 for the "tldr" and "whois" pages

