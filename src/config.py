import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    # python-dotenv not installed; we'll rely on environment only
    def load_dotenv(*_, **__):
        return False


def _try_load_env_files():
    """Attempt to load .env from a few likely locations without overwriting existing env vars."""
    # load default .env from cwd (no override)
    try:
        load_dotenv(override=False)
    except TypeError:
        # older dotenv versions may not accept override kwarg
        load_dotenv()

    # Try repo-root .env and deployment/.env (paths relative to project root)
    repo_root = Path(__file__).resolve().parents[1]
    candidates = [repo_root / ".env", repo_root / "deployment" / ".env"]
    for p in candidates:
        try:
            if p.exists():
                try:
                    load_dotenv(dotenv_path=str(p), override=False)
                except TypeError:
                    load_dotenv(dotenv_path=str(p))
        except Exception:
            # ignore any errors reading these files
            pass


def _strip_quotes(value: str | None) -> str | None:
    if value is None:
        return None
    v = value.strip()
    if (v.startswith("'") and v.endswith("'")) or (v.startswith('"') and v.endswith('"')):
        return v[1:-1]
    return v


# Try to load .env files from likely locations (won't override existing env vars)
_try_load_env_files()

# Expose environment variables for services to consume (normalize quoting)
_env = os.environ

# Support common alternate names for compatibility with earlier .env
MONGODB_URI = _strip_quotes(_env.get("MONGODB_URI") or _env.get("MONGO_URI"))
# prefer MONGODB_DB but fall back to MONGO_DB_NAME or MONGO_DB
MONGODB_DB = _strip_quotes(
    _env.get("MONGODB_DB") or _env.get("MONGO_DB_NAME") or _env.get("MONGO_DB")
)
# collection name compatibility
MONGO_COLLECTION_NAME = _strip_quotes(
    _env.get("MONGO_COLLECTION_NAME") or _env.get("COLLECTION_NAME") or _env.get("COLLECTION")
) or "towns"

__all__ = ["MONGODB_URI", "MONGODB_DB", "MONGO_COLLECTION_NAME"]
