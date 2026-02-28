#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e


echo "Starting Renkei backend..."


# =========================
# WAIT FOR DATABASE
# =========================

if [ -n "$DATABASE_URL" ]; then
  echo "Waiting for database..."

  python << END
import time
import psycopg2
import os

db_url = os.getenv("DATABASE_URL")

max_retries = 30

for i in range(max_retries):
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print("Database is ready.")
        break
    except Exception as e:
        print(f"Database not ready, retrying ({i+1}/{max_retries})...")
        time.sleep(2)
else:
    raise Exception("Database connection failed.")
END

fi


# =========================
# RUN ALEMBIC MIGRATIONS
# =========================

echo "Running migrations..."

alembic upgrade head


# =========================
# OPTIONAL: SEED DATA (dev only)
# =========================

if [ "$SEED_DATA" = "true" ]; then
  echo "Seeding database..."
  python scripts/seed_data.py
fi


# =========================
# START FASTAPI SERVER
# =========================

echo "Starting FastAPI server..."

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 1