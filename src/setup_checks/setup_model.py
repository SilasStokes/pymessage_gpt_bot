from abc import ABC, abstractmethod


class SetupCheckBase(ABC):
    check_name: str
    success: bool
    error_reason: str
    instructions: list[str]

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def _check_setup():
        ...

    def __repr__(self):
        return f'Check: {self.check_name}, Success: {self.success}'
