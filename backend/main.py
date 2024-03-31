from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.main import api_router

app = FastAPI(
    description="CNSP Backend",
    title="CNSP Backend"
)

origins = [
    'http://localhost:3000',
    'https://cnsp-fyp.web.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)