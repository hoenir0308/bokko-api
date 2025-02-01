from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_router import router as user_router
from routes.goal_router import router as goal_router
from routes.task_router import router as task_router
from routes.ask_router import router as ask_router
from routes.schreduler_router import router as schreduler_router

app = FastAPI()

app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(goal_router, prefix="/goal", tags=["Goal"])
app.include_router(task_router, prefix="/task", tags=["Task"])
app.include_router(ask_router, prefix="/ask", tags=["Ask"])
app.include_router(schreduler_router, prefix="/schreduler", tags=["Schreduler"])

origins = ["https://benchmarkvc.ru"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health_check():
    return {"health_check": True}
