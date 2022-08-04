FROM python:3.9.7-slim

RUN mkdir /code
WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.ini /code

RUN python -m pip install --upgrade pip
RUN pip install -r /code/requirements.ini --no-cache-dir

COPY . .
CMD python /code/load_data.py
