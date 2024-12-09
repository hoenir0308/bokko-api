from data.repository import Repository
from config import DATABASE_URL, DATABASE_NAME

async def get_repository() -> Repository: 
    return Repository(
        DATABASE_URL,
        DATABASE_NAME
    )  