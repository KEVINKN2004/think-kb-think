from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api import ask, documents, search

limiter = Limiter(key_func = get_remote_address)

app = FastAPI(title = "Knowledge Base Assistant")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(documents.router)
app.include_router(search.router)
app.include_router(ask.router)

@app.get("/")
def root():
    return {"message": "Hi, this is a project meant to be a Knowledge Base Assistant API. If you'd like to see the docs, please input /docs at the top of the interactive UI's URL."}

@app.get("/status")
def status():
    return {"status": "ok"}