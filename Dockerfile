FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app/ /app/

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

RUN apt-get update && apt-get install -y curl
