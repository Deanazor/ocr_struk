FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get install libopencv-dev git build-essential -y

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod +x InitApp.sh
RUN ./InitApp.sh

EXPOSE 8080

CMD [ "python3", "app.py" ]