# GPT-3 powered iMessage groupchat bot:

This is a few different implementations of an iMessage chatbot that uses openAI's chatgpt to power its responses.

## Caveats:
This has to be ran on mac with iCloud account and iMessage setup and thus will appear to be sent from *you* rather than an external number. Also I believe that groupchat has to be already created. I initially tried to use twilio to power the texts but it looks like as of right now (April 2023) they have deprecated groupmessaging. 

## auto_respond_to_all_texts.py
I wrote this script to intercept any text I receive and then auto-respond to it. Currently I use it to let people know I am at work and wont be on my phone. Uses Emojipastabot to make gpt's response less ✨boring✨.

### TODO:
- [ ] set up config so that emoji pasta can be turned off and on. 
- [ ] I have to manually run it when I start work and stop it when I'm off work - a better implementation would be to run it constantly and programmatically check if do not disturb is on and only respond if dnr is on. 
- [ ] currently responding to groupchats is broken, could be fixed by manually adding your groupchats to the program but that's not ideal. Need to find a way to provide a mapping of user_id to groupchat phone numbers. 
- [ ] currenty chatgpt only sees the most recent incoming message... it would be interesting to max out the tokens and add as much of the message history as possible so gpt can have a contexted response. e.g when someone texts me "hey", gpt usually will send the same response. 
- [ ] add support for contacts.vcf that way gpt can auto know someones name. 


## groupchat.py
This is a more conventional "chatbot", mirror'd after the ones I see in discord. Anyone in the chat can prepend their text with the "!bot" tag and then the body will be sent to openai. You'll need to set up a config for each groupchat you want the bot to run in because I haven't figured out out how to parse the groupchat numbers on the fly from the imessage database - instead I am checking for the groupchat name in the `msg.user_id`, and then messaging the numbers that I know are in that database.

### Todo:
- [x] adapt the script to allow for the config files


## General Todo:
- [ ] EmojipastaBot is installed incorrectly - I want to install it in the virtual environment instead of as a top level folder. 
- [ ] Write a script that will set up py-imessage-shortcuts and Emojipastabots since they aren't hosted on pip. 
- [ ] push changes to imessage_reader to the repo. 
- [ ] Allow the parsing of a contacact file so the names associated with the phone number can be known.
- [ ] both scripts work exactly the same way, see if i can generalize more
