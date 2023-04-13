# GPT-3 powered iMessage groupchat bot:

This is a few different implementations of an iMessage chatbot that uses openAI's chatgpt to power its responses.

## Caveats:
This has to be ran on mac with iCloud account and iMessage setup and thus will appear to be sent from *you* rather than an external number. Also I believe that groupchat has to be already created. I initially tried to use twilio to power the texts but it looks like as of right now (April 2023) they have deprecated groupmessaging. 

## Instructions:
1. create virtual environment with `python -m venv .venv`
2. install python packages with `pip install -r requirements.txt`
3. Install the emojiapasta generator, not a pip package but there is a setup.py so:
    1. Go to the pip package installation location in the virtual environment: `cd .venv/lib/python3.10/site-packages`
    2. Clone the emojipastabot there: `git clone https://github.com/Kevinpgalligan/EmojipastaBot.git`
    3. Open the emojipastabot repo and run the setup.py file: `cd emojipasta && pip install .`
4. Install the py-imessage-shortcuts package. You'll need to set up the shortcut by double clicking the `send-imessage.shortcut` and then selecting "Add shortcut" (the shortcut is from that repo - I did not create it).

## auto_respond_to_all_texts.py
I wrote this script to intercept any text I receive and then auto-respond to it. Currently I use it to let people know I am at work and wont be on my phone. Uses Emojipastabot to make gpt's response less ✨boring✨.

### TODO:
- [ ] clean up the gpt prompt generation, rn it's inline and gross
- [ ] add support for contacts.vcf that way gpt can know the contact name for the person texting and address them by name. 
- [x] set up config so that emoji pasta can be turned off and on. 
- [x] I have to manually run it when I start work and stop it when I'm off work - a better implementation would be to run it constantly and programmatically check if do not disturb is on and only respond if dnr is on. Reading here: https://talk.automators.fm/t/get-current-focus-mode-via-script/12423/10
- [x] Change the gpt prompt to allow for the focus mode to be programmatically added - e.g gpt can say something like "Silas is in Do not disturb mode" vs. "Silas is in sleep mode"
- [x] currenty chatgpt only sees the most recent incoming message... it would be interesting to max out the tokens and add as much of the message history as possible so gpt can have a contexted response. e.g when someone texts me "hey", gpt usually will send the same response. 


## groupchat.py
This is a more conventional "chatbot", mirror'd after the ones I see in discord. Anyone in the chat can prepend their text with the "!bot" tag and then the body will be sent to openai. You'll need to set up a config for each groupchat you want the bot to run in because I haven't figured out out how to parse the groupchat numbers on the fly from the imessage database - instead I am checking for the groupchat name in the `msg.user_id`, and then messaging the numbers that I know are in that database.

### Todo:
- [x] adapt the script to allow for the config files


## General Todo:
- [ ] push changes to imessage_reader to the repo. 
- [ ] Allow the parsing of a contact file so the names associated with the phone number can be known.
- [ ] both scripts work exactly the same way, see if i can generalize more
- [x] EmojipastaBot is installed incorrectly - I want to install it in the virtual environment instead of as a top level folder. 
