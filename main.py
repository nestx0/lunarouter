import asyncio

from dotenv import load_dotenv

from src.dataObjects.message import Message, Role
from src.providers.geminiprovider import GeminiHydrogenProvider

load_dotenv()


async def main():
    print("Creando el proveedor")
    g = GeminiHydrogenProvider()
    print("Creando un mensaje nuevo")
    inputMsg = Message(role=Role.USER, content="Buenos dias desde fuente vaqueros")
    listMsg = [inputMsg]
    print("Preguntando a Gemini")
    msg = await g.generate(listMsg, [])
    print("Respuesta obtenida, esperando...")
    await asyncio.sleep(5)
    print(msg.content)


if __name__ == "__main__":
    asyncio.run(main())
