# =========================
# BASE IMAGE
# =========================

FROM python:3.11-slim


# =========================
# ENVIRONMENT VARIABLES
# =========================

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app


# =========================
# SET WORK DIRECTORY
# =========================

WORKDIR $APP_HOME


# =========================
# INSTALL SYSTEM DEPENDENCIES
# =========================

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*


# =========================
# INSTALL PYTHON DEPENDENCIES
# =========================

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt


# =========================
# COPY PROJECT FILES
# =========================

COPY . .


# =========================
# CREATE NON-ROOT USER
# =========================

RUN adduser --disabled-password --gecos '' appuser

RUN chown -R appuser:appuser $APP_HOME

USER appuser


# =========================
# EXPOSE PORT
# =========================

EXPOSE 8000


# =========================
# START SERVER
# =========================

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]