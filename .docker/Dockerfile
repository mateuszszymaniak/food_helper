FROM python:3.11
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false
WORKDIR /app

RUN pip install poetry

COPY ../poetry.lock /app
COPY ../pyproject.toml /app

RUN poetry install --no-root

COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]