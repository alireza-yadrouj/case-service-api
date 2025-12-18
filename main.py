from fastapi import FastAPI
from CaseService import router

items=[]

app=FastAPI()

app.include_router(router)


