import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Config:
    @staticmethod
    def _parse_cors_origins(origins: str) -> list[str]:
        parsed: list[str] = []
        for origin in origins.split(","):
            candidate = origin.strip().rstrip("/")
            if not candidate or candidate == "*":
                continue
            parsed.append(candidate)
        return parsed

    DATABASE_PATH = os.getenv("DATABASE_PATH", str(PROJECT_ROOT / "database" / "cyberlearn.db"))
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    DEFAULT_USER_ID = int(os.getenv("DEFAULT_USER_ID", "1"))
    CORS_ORIGINS = _parse_cors_origins.__func__(os.getenv("CORS_ORIGINS", ""))
    JSON_SORT_KEYS = False
