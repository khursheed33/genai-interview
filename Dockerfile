FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml .python-version ./
RUN uv sync --group dev --no-dev 2>/dev/null || uv sync --no-cache || pip install -e .
COPY . .
CMD ["python", "--version"]
