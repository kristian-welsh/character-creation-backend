FROM python:3.9.10-alpine3.15

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .
RUN export FLASK_APP=server
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]