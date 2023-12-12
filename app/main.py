
# Import FastAPI from FastAPI Library
from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
import urlShortner

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Tortoise.init_models(["models"], "models")

app.include_router(urlShortner.route)

register_tortoise(
    app, 
    db_url="sqlite://db.sqlite3",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)


