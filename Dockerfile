FROM python:3.11


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY project /app/project
WORKDIR /app/project