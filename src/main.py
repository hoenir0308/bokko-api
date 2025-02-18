import uvicorn
import asyncio
from demon.schreduler import run_schreduler

async def start_scheduler():
    await run_schreduler()

async def main():
    scheduler_task = asyncio.create_task(start_scheduler())
    
    config = uvicorn.Config("app:app", host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())