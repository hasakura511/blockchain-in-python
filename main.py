import os, sys
import random

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print("appending", BASE_DIR)
# sys.path.append(BASE_DIR)

# python lib
import uvicorn
from typing import Optional
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.websockets import WebSocket
from fastapi import FastAPI, Response, status, Request
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time
from be.config import ROOT_PORT
from be.db.db_bc import initialize_peer

# routes
from be.routes import bc, wallet


# db models
# from db import models
# from db.databases import engine

# creates sqlite db file & model
# models.Base.metadata.create_all(engine)

# app = FastAPI(openapi_url="/api/openapi.json")
app = FastAPI()
app.include_router(bc.router)
app.include_router(wallet.router)

# middleware
origins = [
    # 'http://localhost:3000/' <- remove last /
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    # preprocess above
    # call next is the api that was called.
    response = await call_next(request)
    # postprocess below
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response


@app.get("/")
def index():
    return "Flask Blockchain Index"


if __name__ == "__main__":
    # this needs to be in main or uvicorn will run twice
    PORT = ROOT_PORT
    if os.environ.get("PEER"):
        print("PEER MODE")
        PORT = initialize_peer()

    if os.environ.get("SEED_DATA"):
        from be.db.db_bc import seed_data

        print("SEEDING DATA")
        seed_data()

    uvicorn.run(
        "main:app", host="0.0.0.0", port=PORT, log_level="info", reload=False
    )
