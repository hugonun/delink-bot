# delink-bot

A Discord bot to combat phishing links for Steam trades and Discord gifts.

## Features

- Removes domains listed on the blacklist.
- Automatically deletes domains that have a certain pattern and are not yet on the blacklist.
- Allows you to make your own URL blacklist and whitelist for your server. We will periodically check and add it to the global list.
- Supports other phishing and scam databases, giving us a total of +5000 URLs. 

## Invite link

https://discord.com/oauth2/authorize?client_id=903114852631969802&scope=bot&permissions=2147871808

## Supported databases

Fish Project - https://blog.hyperphish.com/

(TBD) Azeael Phish API - https://phish.azrael.gg/

## Requirement

`python3 -m pip install -U discord.py`

`python3 -m pip install tldextract`

or

`python3 -m pip install -r requirements.txt`

## Setup

Create the file `token.txt` and add your Discord token inside it.

Then run the bot using `python3 init.py`.

## For fast setup and run bot after

`python run_setup.py`
