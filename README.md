# GPT-3 powered iMessage groupchat bot:

This is a few different implementations of an iMessage chatbot that uses openAI's chatgpt to power its response.

## Caveats:
This has to be ran on mac with iCloud account and iMessage setup. Also I believe that groupchat has to be already created. I initially tried to use twilio to power the texts but it looks like as of right now (April 2023) they have deprecated groupmessaging. 

## auto_respond_to_all_texts.py
I wrote this script to intercept any text I receive and then auto-respond to it. Currently I use it to let people know I am at work and wont be on my phone. Uses Emojipastabot to make gpt's response less ✨boring✨.

### TODO:
- [ ] set up config so that emoji pasta can be turned off and on. 
- [ ] I have to manually run it when I start work and stop it when I'm off work - a better implementation would be to run it constantly and programmatically check if do not disturb is on and only respond if dnr is on. 
- [ ] currently responding to groupchats is broken, could be fixed by manually adding your groupchats to the program but that's not ideal. Need to find a way to provide a mapping of user_id to groupchat phone numbers. 


## groupchat.py
This is a more conventional "chatbot", mirror'd after the ones I see in discord. Anyone in the chat can prepend their text with the "!bot" tag and then the body will be sent to openai. 

- [ ] adapt the script to allow for the config files


## General Todo:
- [ ] EmojipastaBot is installed incorrectly - I want to install it in the virtual environment instead of as a top level folder. 
- [ ] Write a script that will set up py-imessage-shortcuts and Emojipastabots since they aren't hosted on pip. 
- [ ] push changes to imessage_reader to the repo. 
