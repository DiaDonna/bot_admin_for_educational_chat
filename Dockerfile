FROM python:3.10-slim-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME}"

COPY requirements.txt /usr/src/app/"${BOT_NAME}"
RUN pip install --no-cache-dir --upgrade pip  \
    && pip install -r /usr/src/app/"${BOT_NAME}"/requirements.txt
COPY . /usr/src/app/"${BOT_NAME}"
