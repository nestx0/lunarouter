import asyncio

from dotenv import load_dotenv

from src.dataObjects.message import Message, Role
from src.exceptions.ownexceptions import TokenLimitReached
from src.providers.geminiprovider import GeminiHydrogenProvider

load_dotenv()


async def main():
    print("Creando el proveedor")
    g = GeminiHydrogenProvider()
    print("Creando un mensaje nuevo")
    inputMsg = Message(
        role=Role.USER,
        content="Explicame de forma sencilla la teoría de Hackman y Oldham",
    )
    listMsg = [inputMsg]
    print("Preguntando a Gemini")
    msg = Message(role=Role.SYSTEM, content="a")
    try:
        msg = await g.generate(listMsg, [])
    except TokenLimitReached as e:
        print(e)
    print("Respuesta obtenida")
    print(msg.content)


if __name__ == "__main__":
    asyncio.run(main())
