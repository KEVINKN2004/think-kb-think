from fastapi import FastAPI

app = FastAPI(title="Knowledge Base Assistant")

@app.get("/")
def root():
    return {"message": "Hi, this is a project meant to be a Knowledge Base Assistant API. If you'd like to see the docs, please see /docs."}

@app.get("/status")
def status():
    return {"status": "ok"}