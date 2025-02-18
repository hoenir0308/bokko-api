from config import TELEGRAM_API_URL
import httpx

async def send_message(user_id, text: str):
    client = httpx.AsyncClient()
    try:
        await client.post(
            f'{TELEGRAM_API_URL}sendMessage',
            json={
                'chat_id': user_id,
                'text': text
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        return None
    