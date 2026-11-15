from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    TOOL = "tool"
    ASSISTANT = "assistant"


@dataclass
class ToolCall:
    id: str
    name: str
    args: dict[str, Any]


@dataclass
class Attachment:
    file_path: str
    mime_type: str  # jpg, pdf, mp3...


@dataclass
class Message:
    """
    Esta clase responde a la pregunta de, ¿que tiene que tener?
    un mensaje, entonces un mensaje del historial tiene que tener
    un rol concreto (si es una tool, algo del usuario, historial o
    del sistema)

    Luego tenemos el mensaje en sí y las tool calls que han sido
    necesarias para llegar al resultado, así como todos los archivos
    adjuntos que llegan al mensaje
    """

    role: Role
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_id: str | None = None
    attachments: list[Attachment] = field(default_factory=list)

    @property
    def char_count(self) -> int:
        tools_len = sum(len(tc.name) + len(str(tc.args)) for tc in self.tool_calls)
        return len(self.content) + tools_len
