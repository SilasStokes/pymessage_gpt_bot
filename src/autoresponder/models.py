from dataclasses import dataclass, field
from typing import List
from dataclass_wizard import JSONWizard

@dataclass
class PersonalInfo:
    name: str
    date_of_birth: str
    phone_number: str

@dataclass
class Recipient:
    name: str
    phone_number: str
    about: str

@dataclass
class GroupChat(JSONWizard):
    name: str
    prompt: str
    context: bool
    enabled: bool
    only_reply_focus_mode: bool
    number_previous_messages: int
    emoji_pasta: bool
    bot_trigger_command: str
    recipients: List['Recipient']
    
    def __contains__(self, user_id) -> bool:
        return self.name == user_id

@dataclass
class SingleChat:
    name: str
    phone_number: str
    about: str
    prompt: str
    context: bool
    enabled: bool
    only_reply_focus_mode: bool
    number_previous_messages: int
    emoji_pasta: bool
    bot_trigger_command: str
    
    def __contains__(self, user_id) -> bool:
        return self.name == user_id

@dataclass
class DefaultSingleChat:
    about: str
    prompt: str
    context: bool
    enabled: bool
    only_reply_focus_mode: bool
    number_previous_messages: int
    emoji_pasta: bool
    bot_trigger_command: str

@dataclass
class Configuration(JSONWizard):
    openai_api_key: str
    max_tokens: int
    delay_between_loops: int
    personal_info: 'PersonalInfo'
    single_chats: List['SingleChat']
    default_single_chat: 'DefaultSingleChat'
    group_chats: List['GroupChat']
