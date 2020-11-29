FROM python:3.9-slim

ENV TZ Europe/Budapest
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

ARG RELEASE_ID
ENV RELEASE_ID ${RELEASE_ID:-""}

COPY requirements.txt ./

RUN apt update && apt install -y libmagic1 && apt clean && pip install --no-cache-dir -r requirements.txt && rm -rf requirements.txt && useradd -r -s /bin/false -M -u 999 shopper

COPY ./src .

EXPOSE 8080
USER 999
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "4", "--threads", "1", "app:app"]