import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import get_settings
from database.db import connect_db, close_db
from routers.api import api_router

import logging

logging.basicConfig(filename='server.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

app = FastAPI()
app.include_router(api_router)

origins = [
    get_settings().client_url,
    "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await connect_db()


@app.on_event("shutdown")
async def startup_event():
    await close_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=get_settings().port, reload=True)