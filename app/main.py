from fastapi import FastAPI
from app.routes import router


def init() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    return application


app = init()
