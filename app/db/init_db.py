from app.db.session import engine, Base
from app.db import models

def init():
    Base.metadata.create_all(bind = engine)
    print("Tables created.")

if __name__ == "__main__":
    init()