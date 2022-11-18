FROM python:3.10-slim-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR app/"${BOT_NAME}"

COPY requirements.txt /app/"${BOT_NAME}"
RUN pip install --no-cache-dir --upgrade pip  \
    && pip install -r app/"${BOT_NAME}"/requirements.txt
COPY . .
