"""Solution: fail fast at boot, mask in logs, stream rows lazily."""

import json
import types

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"
    database_url: str = "sqlite:///./dev.db"
    llm_key: str = ""

    def must_have_llm(self):
        if self.env == "prod" and not self.llm_key:
            raise ValueError("LLM_KEY required in prod")
        return True

    def masked(self):
        return self.llm_key[:3] + "***" if self.llm_key else "(empty)"


def ndjson(rows):
    for r in rows:
        yield json.dumps(r) + "\n"


assert isinstance(ndjson([]), types.GeneratorType)  # lazy by construction
