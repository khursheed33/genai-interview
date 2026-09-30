"""06_config.py — one recipe, many canteens (env decides).

Run: uv run python topics/03-backend-frameworks/examples/06_config.py
"""

import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    env: str = "dev"
    database_url: str = "sqlite:///./dev.db"
    openai_api_key: str = ""

    def validate_prod(self):
        if self.env == "prod" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY required in prod — fail fast at boot!")

    def safe_view(self):  # never log the secret raw
        key = self.openai_api_key
        return {"env": self.env, "key": (key[:3] + "***" if key else "(empty)")}


os.environ.pop("APP_ENV", None)
dev = Settings()
dev.validate_prod()  # dev may run keyless
assert dev.safe_view()["key"] == "(empty)"

os.environ["APP_ENV"] = "prod"  # not our prefix — proves env_nested? no, proves isolation
prod = Settings(env="prod", openai_api_key="sk-live-123")
prod.validate_prod()
assert prod.safe_view() == {"env": "prod", "key": "sk-***"}
try:
    Settings(env="prod", openai_api_key="").validate_prod()
    raise AssertionError("should have failed fast!")
except ValueError as e:
    assert "required in prod" in str(e)
print("dev:", dev.safe_view(), "| prod:", prod.safe_view())
print("OK — env decides, secrets from vaults, fail fast, mask in logs")
