from dataclasses import dataclass

@dataclass
class GroupchatConfig:
    gptprompt: str
    openai_api_key: str
    emoji_pasta: bool
    delay_between_loops: int
    groupchat_name: str
    groupchat_recipients: list[str]

@dataclass
class AutoRespondConfig:
    gptprompt: str
    openai_api_key: str
    emoji_pasta: bool
    delay_between_loops: int