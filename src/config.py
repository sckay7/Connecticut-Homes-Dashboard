import os
from dotenv import load_dotenv

try:
    load_dotenv()
except Exception:
    # ignore if dotenv not available
    pass

# Expose environment variables for services to consume
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")

__all__ = ["MONGODB_URI", "MONGODB_DB"]
