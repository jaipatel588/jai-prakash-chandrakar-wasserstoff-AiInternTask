
import os

class Settings:
    DATA_DIR = os.getenv("DATA_DIR", "backend/data/")
    VECTOR_PATH = os.getenv("VECTOR_PATH", os.path.join(DATA_DIR, "vector_store"))

settings = Settings()
