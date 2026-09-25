from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies import history
from app.routers import calculator, history as history_router

app = FastAPI(title="Mini Calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator.router)
app.include_router(history_router.router)
