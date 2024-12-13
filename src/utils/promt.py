import openai
from config import GROQ_API_KEY

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

async def ask_decomposing(title: str, text: str, name: str, age: int) -> str:
    promt_text = f"Ты самый лучший персональный тьютор для {name}, возраста {age}. Твоя цель - декомопозировать задачи. Отвечай эмоционально. Так же, ты можешь использовать эмодзи."
    
    result = openai.ChatCompletion.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": promt_text},
            {"role": "user", "content": f"{title} \n {text}"},
        ],
    )

    return result["choices"][0]["message"]["content"]

async def ask_motivation(title: str, tasks: list, name: str, age: int):
    promt_text = f"Ты самый лучший персональный тьютор. Твоя задача - мотивировть {name}, возрастом {age}, для выполнения цели {title}, состоящей из множества подцелей"
    tasks_prompt = ""
    for task in tasks:
        promt_text += f"\n {str(task)}"
    
    result = openai.ChatCompletion.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": promt_text},
            {"role": "user", "content": tasks_prompt},
        ],
    )

    return result["choices"][0]["message"]["content"]
