# iMessage Chat Bot - Powered by ChatGPT

iMessage Chat Bot is a library / CLI to automate conversations via text. Use it as a funny tool to annoy friends,
or something useful such as a personalized messaging system to inform your loved ones you are not available to chat.
The chat bot uses *your* number to send the automated responses, simplifying the experience of automating and interacting with
texts.

## Usage
The chat bot utilizes a `json` file to help configure the settings and behavior when running the program. An example format for the
`config.json` can be found [here](./configs/example-config.json). Below is also a rundown of each of the sections and explanation
of their purpose.

### General Information

| Name | Description |
| --- | --- |
| max_tokens | The number of tokens that an LLM can process in a single interaction.
| delay_between_loops | The amount of time to wait until pinging the local chat database for updates.
| personal_info | An object that contains information about you. This is provided to Chat GPT if `context` is set to `true`.
| default_single_chat | a single chat object that is the default response settings for the auto-messenger. This is an optional section. If not provided, no default messages will be sent.
| single_chats | A list of single chat objects that override the `default_single_chat` settings. Unique identifier is the `phone_number`
| group_chats | A list of group chat objects that describe the settings for the auto-messenger. This is an optional section. If not provided, no responses will be made to group chats. Keys are the recipients name.

### Single/Default/Group Chats

| Name | Description |
| --- | --- |
| name | The name of the recipient.
| phone_number | The phone number of the recipient.
| about | A brief description of the purpose of the chat bot. This is not used as `context` for Chat GPT.
| prompt | The prompt to send as a request to Chat GPT.
| context | `true` to provide additional chat details to Chat GPT request.
| only_reply_focus_mode | `true` to only reply in focus mode. |
| number_of_previous_messages | if `context` is true, sends the `n` previous messages as context to create a reply. This is constrained by the maximum number of tokens allowed.
| emoji_pasta | Creates emoji-fied responses from the auto-messenger.
| bot_trigger_command | The trigger command to enable the bot in a chat. If an empty string, replies will happen with all incoming texts.

### Group Chat

| Name | Description |
| --- | --- |
| recipients | A list of recipients that are apart of the group chat. Recipients' name and phone number *must* match for every individual in the chat.

## Requirements

- MacOS computer
- iPhone with message forwarding enabled
- An iCloud account and iMessage setup
- Python3 (developed on 3.11)
- ChatGPT account with API Key

This has to be ran on mac with iCloud account and iMessage setup and thus will appear to be sent from *you* rather than an external number. Also I believe that groupchat has to be already created. I initially tried to use twilio to power the texts but it looks like as of right now (April 2023) they have deprecated group messaging.

## How to Setup
1. create virtual environment with `python -m venv .venv`
2. install python packages with `pip install -r requirements.txt`
3. Install the emojiapasta generator, not a pip package but there is a setup.py so:
    1. Go to the pip package installation location in the virtual environment: `cd .venv/lib/python3.10/site-packages`
    2. Clone the emojipastabot there: `git clone https://github.com/Kevinpgalligan/EmojipastaBot.git`
    3. Open the emojipastabot repo and run the setup.py file: `cd emojipasta && pip install .`
4. Install the py-imessage-shortcuts package. You'll need to set up the shortcut by double clicking the `send-imessage.shortcut` and then selecting "Add shortcut" (the shortcut is from that repo - I did not create it).
5. Create a Chat GPT API Key [here](https://platform.openai.com/api-keys) and add it to your config file. Alternatively, you can set the global variable in the command line: `export OPENAI_API_KEY=<your-api-key>`
6. In order to read iMessage data, the application or terminal will need full disk access. iMessage data exists in `~/Library/Messages` which is protected. Go to `Settings -> Privacy & Security -> Full Disk Access` and select the application that should get access.
7. Ensure iMessage text forwarding is enabled on your iPhone.