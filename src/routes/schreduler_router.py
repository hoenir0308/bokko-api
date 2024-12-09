from fastapi import APIRouter, Depends, HTTPException
from data.depends import get_repository
from middleware.auth import get_current_user
from data.repository import Repository
from middleware.auth import TelegramUser
from utils.serialize import get_serialize_document
from models.schreduler_models import Schreduler

router = APIRouter()

@router.get("/")
async def fetch_schreduler(repo: Repository = Depends(get_repository),
                           user: TelegramUser = Depends(get_current_user)):
    document = await repo.find_one("schreduler", {"tg_id": user.id})
    if not document:
        raise HTTPException(404, "Schreduler not found")
    return await get_serialize_document(document)

@router.put("/")
async def change_schreduler(request: Schreduler,
                            repo: Repository = Depends(get_repository),
                            user: TelegramUser = Depends(get_current_user)):
    document = request.model_dump()
    await repo.update_one("schreduler", {"tg_id": user.id}, document)
    doc = await repo.find_one("schreduler", {"tg_id": user.id})
    return await get_serialize_document(doc)
    