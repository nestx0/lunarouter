import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()


async def realizarLlamadaGemini(texto: str):
    API_KEY = os.getenv("GEMINI_KEY")
    URL = "https://generativelanguage.googleapis.com/v1beta/interactions"
    payload = {
        "model": "gemini-4-hydrogen",
        "input": texto,
        "system_instruction": "Habla como un gitano",
        "generation_config": {
            "temperature": 0.4,
            "max_output_tokens": 1024,
        },
    }
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data


async def main():
    r1 = await realizarLlamadaGemini("buenos dias !")
    await asyncio.sleep(5)
    r2 = await realizarLlamadaGemini("que dices primo")

    print(r1)
    print(r2)


if __name__ == "__main__":
    asyncio.run(main())
