FROM python:3.12-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk add --no-cache git
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api /code/api
COPY ./db /code/db

CMD ["fastapi", "run", "api/main.py", "--port", "80"]
