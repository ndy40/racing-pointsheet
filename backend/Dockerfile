FROM python:3.12-bullseye
LABEL authors="ndy40"
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="/opt/venv"

RUN apt update -y && python -m venv $VIRTUAL_ENV

ENV PATH=$VIRTUAL_ENV/bin:$PATH

COPY ./pointsheet/pyproject.toml ./pointsheet/poetry.lock /app/
RUN pip install poetry && poetry install
COPY ./pointsheet/ /app

CMD ["python", "main.py"]
