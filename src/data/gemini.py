import httpx

class Gemini:
    _instance = None

    def __new__(cls, key: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.key = key
            cls._instance.client = httpx.AsyncClient()
        return cls._instance

    async def ask(self, prompt: str):
        return await self.ask_with_history([prompt])

    async def ask_with_history(self, messages: list):
        parts = [{'text': m} for m in messages]
        try:
            response = await self.client.post(
                'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent',
                params={'key': self.key},
                headers={'Content-Type': 'application/json'},
                json={
                    'contents': [{'parts': parts}],
                    "safetySettings": [
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                }
            )
            response_json = response.json()
            print(response_json)
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"Error: {e} | Messages: {e.__str__}")
            return None

    async def close(self):
        await self.client.aclose()
