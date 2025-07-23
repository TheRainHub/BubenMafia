FROM python:3.11-slim

WORKDIR /app

# 1) Устанавливаем системные зависимости + postgresql-client
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc libpq-dev python3-dev \
        postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# 2) Копируем и ставим Python‑зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 3) Копируем остальной код
COPY . /app

# 4) По‑умолчанию ждем БД, мигрируем и стартуем приложение
CMD ["sh", "-c", "\
  echo 'Waiting for database…' && \
  until pg_isready -h db -U root; do sleep 1; echo -n '.'; done; \
  echo '\nDatabase is up — running migrations' && \
  alembic upgrade head && \
  echo 'Starting FastAPI' && \
  uvicorn app.main:app --host 0.0.0.0 --port 8000\
"]
