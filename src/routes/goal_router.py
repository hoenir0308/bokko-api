from annotated_types import doc
from fastapi import APIRouter, Depends, HTTPException
from data.depends import get_repository
from middleware.auth import get_current_user
from data.repository import Repository
from middleware.auth import TelegramUser
from models.goal_models import GoalModel
from utils.serialize import get_serialize_document
import bson

router = APIRouter()

@router.post("/")
async def create_goal(request: GoalModel,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    document = request.model_dump()
    document["tg_id"] = user.id
    ins_id = await repo.insert_one("goals", document)
    doc = await repo.find_one("goals", {"_id": ins_id})
    return await get_serialize_document(doc)

@router.put("/")
async def update_goal(goal_id: str, 
                      request: GoalModel, 
                      repo: Repository = Depends(get_repository), 
                      user: TelegramUser = Depends(get_current_user)):
    filter_query = {"_id": goal_id, "tg_id": user.id}
    update_data = {"$set": request.model_dump()}
    update_result = await repo.update_one("goals", filter_query, update_data)
    
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Goal not found or not modified")
    
    updated_doc = await repo.find_one("goals", filter_query)
    return await get_serialize_document(updated_doc)

@router.get("/")
async def fetch_goals(repo: Repository = Depends(get_repository),
                    user: TelegramUser = Depends(get_current_user)):
    documents = await repo.find_many("goals", {"tg_id": user.id})

    for i in range(len(documents)):
        cd = documents[i]
        tasks = await repo.find_many("tasks", {"goal_id": cd["_id"]})
        ct = 0
        cp = 0

        for t in tasks:
            if t["complite"]: ct += 1
        
        if len(tasks) != 0:
            cp = int(100.0 / len(tasks) * ct)

        documents[i]["complete"] = cp

    return await get_serialize_document(documents)

@router.get("/tasks/")
async def fetch_tasks(goal_id: str,
                    repo: Repository = Depends(get_repository)):
    documents = await repo.find_many("tasks", {"goal_id": goal_id})
    return await get_serialize_document(documents)

@router.delete("/")
async def delete_goal(id: str,
                      repo: Repository = Depends(get_repository),
                      user: TelegramUser = Depends(get_current_user)):
    document = await repo.find_one("goals", {"tg_id": user.id, "_id": bson.ObjectId(id)})
    if not document:
        raise HTTPException(404, "document not found")
    await repo.delete_one("goals", {"tg_id": user.id, "_id": bson.ObjectId(id)})
    return {"detail":"document succesfully delete"}
