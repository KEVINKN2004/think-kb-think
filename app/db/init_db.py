from app.db import models  # noqa: F401 (Ensures the models are registered)
from app.db.session import Base, engine


def init():
    Base.metadata.create_all(bind = engine)
    print("Tables created: {sorted(Base.metadate.tables)}.")

if __name__ == "__main__":
    init()