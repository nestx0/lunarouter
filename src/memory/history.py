from collections import deque

from dataObjects.message import Message, Role
from exceptions.contextexcedeed import ContextWindowExcedeed


# Quizas cambiar characters por tokens usados
class ConversationHistory:
    def __init__(self, max_tam: int = 3, max_chars: int = 5000) -> None:
        self.MAX_TAM = max_tam
        self.MAX_CHARS = max_chars
        self._messages: deque[Message] = deque()
        self._current_chars: int = 0

    def addMessage(self, txt: Message):
        if txt.char_count > self.MAX_CHARS:
            raise ContextWindowExcedeed

        while len(self._messages) >= self.MAX_TAM or (
            self._current_chars + txt.char_count > self.MAX_CHARS
        ):
            self._evictOldest()

        self._messages.append(txt)
        self._current_chars += txt.char_count

    def _evictOldest(self) -> None:
        removed = self._messages.popleft()
        self._current_chars -= removed.char_count

        while self._messages and self._messages[0].role == Role.TOOL:
            orphan = self._messages.popleft()
            self._current_chars -= orphan.char_count

    def getHistory(self) -> list[Message]:
        return list(self._messages)

    def clear(self) -> None:
        self._messages = deque()
