FROM python:3.12-bullseye
LABEL authors="ndy40"
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV="/opt/venv"

RUN apt update -y && apt install -y libgl1 tesseract-ocr && python -m venv $VIRTUAL_ENV

ENV PATH=$VIRTUAL_ENV/bin:$PATH

COPY ./pointsheet/pyproject.toml ./pointsheet/poetry.lock /app/
RUN pip install poetry && poetry install
COPY ./pointsheet/ /app

RUN pip install gunicorn
CMD ["gunicorn", "--workers=4", "--threads=2", "--worker-class=gthread", "--bind=0.0.0.0:5000", "pointsheet:create_app()"]
