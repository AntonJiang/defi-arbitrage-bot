FROM python:3

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY contracts ./contracts
COPY src ./src
COPY .env ./

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD [ "python", "src/main.py" ]

