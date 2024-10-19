from fastapi import FastAPI

from src.items.router import router as items_router

app = FastAPI(
    title='Vkusno'
)

app.include_router(items_router)