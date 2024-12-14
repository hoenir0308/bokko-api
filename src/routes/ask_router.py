from fastapi import APIRouter, Depends, HTTPException
from data.depends import get_repository
from middleware.auth import get_current_user
from data.repository import Repository
from middleware.auth import TelegramUser
from utils.promt import ask_decomposing
import bson

router = APIRouter()

@router.post("/decomposing/")
async def fetch_motivate(goal_id: str,
                         repo: Repository = Depends(get_repository),
                         user: TelegramUser = Depends(get_current_user)):
    docoment = await repo.find_one("goals", {"_id": bson.ObjectId(goal_id), "tg_id": user.id})
    db_user = await repo.find_one("users", {"tg_id": user.id})
    if not docoment:
        raise HTTPException(404, "document not found")

    resp = [
        {
            "title": "Task 1",
            "description": "description",
        },
        {
            "title": "Task 2",
            "description": "description",
        },
        {
            "title": "Task 3",
            "description": "description",
        },
        {
            "title": "Task 4",
            "description": "description",
        },
    ]

    return {"detail": resp}


