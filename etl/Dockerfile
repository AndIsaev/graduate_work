FROM python:3.9.7-slim
WORKDIR /code
COPY requirements.ini /code
RUN pip install -r /code/requirements.ini --no-cache-dir
COPY . /code
EXPOSE 8000
CMD python /code/load_data.py