from fastapi import FastAPI

from app.api import documents, search

app = FastAPI(title="Knowledge Base Assistant")
app.include_router(documents.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {"message": "Hi, this is a project meant to be a Knowledge Base Assistant API. If you'd like to see the docs, please see /docs."}

@app.get("/status")
def status():
    return {"status": "ok"}