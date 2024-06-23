FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
