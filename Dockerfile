FROM python:3.11.1

WORKDIR /app

COPY . /app

RUN python3 -m pip install --upgrade pip && pip install -r requirements.txt

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:80"]
