import os

import httpx
from dotenv import load_dotenv

from src.dataObjects.message import Message, Role, ToolCall
from src.providers.baseprovider import BaseLLMProvider

load_dotenv()

# El error 400 es el que pasa cuando no se hace una request buena
# Si el status es incomplete, entonces significa que se ha quedado sin tokens para
# la request, mirar si es el mismo error que un rate limit o que se acaban los tokens del dia

GEMINI_ROLE_MAP = {
    Role.USER: "user",
    Role.ASSISTANT: "model",
}


class GeminiHydrogenProvider(BaseLLMProvider):
    """
    Clase para encapsular las llamadas a Gemini, su método generate acepta una lista
    de mensajes si necesitamos el historial (que hay que usarlo por si se usa un modelo)
    antes. La idea de ejecución es:

        g = GeminiHydrogenProvider()
        newMessage = g.generate(messages, tools)

    ...
    """

    URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
    API_KEY = os.getenv("GEMINI_KEY")

    def __init__(self) -> None:
        self.payload = {
            "model": "gemini-4-hydrogen",
            "input": None,
            "system_instruction": "Habla como un gitano",  # Modificar mas tarde
            "generation_config": {  # Modificar más tarde
                "temperature": 0.4,
                "max_output_tokens": 8024,
            },
        }
        self.headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.API_KEY,
        }

    def _message_to_steps(self, message: Message) -> list[dict]:
        steps: list[dict] = []

        # Caso 1: Resultado de una herramienta ejecutada previamente
        if message.tool_id is not None:
            steps.append(
                {
                    "type": "function_result",
                    "call_id": message.tool_id,
                    "result": message.content,
                }
            )
            return steps

        # Caso 2: Mensaje de usuario o texto del asistente
        content = []
        for a in message.attachments:
            content.append(
                {
                    "type": a.type,
                    "data": a.data,
                    "mime_type": a.mime_type,
                }
            )

        if message.content:
            content.append(
                {
                    "type": "text",
                    "text": message.content,
                }
            )

        if content:
            step_type = "user_input" if message.role == Role.USER else "model_output"
            steps.append(
                {
                    "type": step_type,
                    "content": content,
                }
            )

        # Caso 3: Llamadas a herramientas emitidas por el modelo en ese turno
        for tc in message.tool_calls:
            steps.append(
                {
                    "type": "function_call",
                    "id": tc.id,
                    "name": tc.name,
                    "arguments": tc.args,
                }
            )

        return steps

    def _json_to_message(self, data: dict) -> Message:
        status = data.get("status")
        if status not in ("completed", "requires_action"):
            raise RuntimeError(
                f"Respuesta inesperada de Gemini (status={status}): {data}"
            )

        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        for step in data.get("steps", []):
            step_type = step.get("type")

            if step_type == "model_output":
                for block in step.get("content", []):
                    if block.get("type") == "text":
                        text_parts.append(block.get("text", ""))

            elif step_type == "function_call":
                tool_calls.append(
                    ToolCall(
                        id=step["id"],
                        name=step["name"],
                        args=step.get("arguments", {}),
                    )
                )

        return Message(
            role=Role.ASSISTANT,
            content="".join(text_parts),
            tool_calls=tool_calls,
        )

    async def generate(self, messages: list[Message], tools) -> Message:
        steps: list[dict] = []
        for m in messages:
            steps.extend(self._message_to_steps(m))

        payload = {**self.payload, "input": steps}

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.URL, headers=self.headers, json=payload)
            if response.is_error:
                print("Detalle del error de Google:", response.text)
            response.raise_for_status()
            data = response.json()

        return self._json_to_message(data)
