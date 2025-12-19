from fastapi import FastAPI
from CaseService import router

app=FastAPI()

app.include_router(router)


