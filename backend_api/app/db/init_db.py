# backend_api/app/db/init_db.py

from backend_api.app.db.connection import engine
from backend_api.app.db import models

models.Base.metadata.create_all(bind=engine)


