from fastapi import APIRouter, Depends, HTTPException
from data.repository import Repository
from data.depends import get_repository
from middleware.auth import TelegramUser
from middleware.auth import get_current_user
from models.user_models import UserModel
from utils.serialize import get_serialize_document
import datetime

router = APIRouter()

@router.post("/register/")
async def register_user(request: UserModel, 
                        repo: Repository = Depends(get_repository),
                        user: TelegramUser = Depends(get_current_user)):
    document = request.model_dump()
    document["tg_id"] = user.id
    ins_id = await repo.insert_one("users", document)
    doc = await repo.find_one("users", {"_id": ins_id})
    schreduler = {
        "tg_id": user.id,
        "send_at": datetime.datetime.now(),
        "interval": "12h",
        "enable": False,
        "motivate": False
    }
    await repo.insert_one("schreduler", schreduler)
    return await get_serialize_document(doc)

@router.put("/")
async def change_user(request: UserModel,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    document = request.model_dump()
    await repo.update_one("users", {"tg_id": user.id}, document)
    return {"detail":"document successfull update"}

@router.get("/me/")
async def fetch_me(repo: Repository = Depends(get_repository),
                   user: TelegramUser = Depends(get_current_user)):
    document = await repo.find_one("users", {"tg_id": user.id})
    if not document:
        raise HTTPException(404, "document not found")
    return await get_serialize_document(document)

