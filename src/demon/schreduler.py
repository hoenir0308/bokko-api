from config import DATABASE_NAME, DATABASE_URL
from data.repository import Repository
import asyncio
from utils.promt import ask_motivation
from time import sleep
from datetime import datetime, timedelta
from utils.telegram import send_message
import bson

async def get_schredule(repo: Repository):
    current_date = datetime.now()
    tasks = await repo.find_many("schreduler", {"send_at": {"$lte": current_date}, "enable": True})
    return tasks

async def get_schredule_task(repo: Repository, user_id: int):
    current_date = datetime.now()
    start_of_day = datetime(current_date.year, current_date.month, current_date.day)
    end_of_day = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)
    tasks = await repo.find_many("tasks", {"deadline": {"$gte": start_of_day, "$lte": end_of_day}, "complite": True, "tg_id": user_id})
    return tasks

async def update_schreduled_task(repo: Repository, task):
    interval = task.get("interval")
    next_time = datetime.now()
    if interval == "6h":
        next_time += timedelta(days=0.25)
    elif interval == "12h":
        next_time += timedelta(days=0.5)
    elif interval == "24h":
        next_time += timedelta(days=1)

    await repo.update_one("schreduler", {"_id": task['_id']}, {
        "send_at": next_time
    })

async def run_schreduler():
    repo = Repository(DATABASE_URL, DATABASE_NAME)
    while True:
        schredulers = await get_schredule(repo)
        for schreduler in schredulers:
            user_id = schreduler["tg_id"]

            tasks = get_schredule_task(repo, user_id)

            for task in tasks:
                if schreduler["motivate"]:
                    goal = await repo.find_one("goals", {"_id": bson.ObjectId(task["goal_id"])})
                    text = await ask_motivation(goal["title"], [task])  
                    await send_message(task["tg_id"],
                                       f"{text}")  
                    sleep(1)
                else:
                    await send_message(task["tg_id"],
                                f"Привет дружище, дедлайн задачи {task['title']} сгорает сегодня. Может пора взяться?")
                    sleep(1)
            await update_schreduled_task(repo, schreduler)
        await asyncio.sleep(60)
