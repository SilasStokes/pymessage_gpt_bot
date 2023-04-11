from dataclasses import dataclass

@dataclass
class Config:
    gptprompt: str
    imessage_phone_number: str
    destination_phone_numbers: list[str]
    openai_api_key: str

@dataclass
class AutoRespondConfig:
    gptprompt: str
    openai_api_key: str
    emoji_pasta: bool
    delay_between_loops: int