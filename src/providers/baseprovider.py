from abc import ABC, abstractmethod

from src.dataObjects.message import Message


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list[Message], tools) -> Message:
        pass
