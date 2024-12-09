from data.gemini import Gemini
from config import GEMINI_API_KEY

gemini = Gemini(
    key=GEMINI_API_KEY
)

async def ask_decomposing(title: str, text: str, name: str, age: int) -> str:
    promt_text = f"Привет, ты самый лучший персональный тьютор, можешь декомпозировать цель: {title} и расписать возможные ее задачи вот ее описание {text}. Меня зовут {name}, мне {age} лет. Отвечай эмоционально и можешь использовать эмодзи."
    result = await gemini.ask(promt_text)
    return result

async def ask_motivation(title: str, tasks: list):
    promt_text = f"Привет, ты самый лучший персональный тьютор, можешь задать мотивацию для выполнение цели: {title}. Вот задачи, которе сгорают скоро:"
    for task in tasks:
        promt_text += f"\n {str(task)}"
    result = await gemini.ask(promt_text)
    return result