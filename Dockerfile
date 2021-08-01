FROM python:3-alpine

ADD . /app

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]