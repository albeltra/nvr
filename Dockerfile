FROM python:3.10-alpine

RUN apk update \
    && apk upgrade \
    && apk add tzdata ffmpeg python3 bash \
    && mkdir -p /recordings \
    && mkdir -p /scripts

COPY ./scripts/ /scripts/

RUN chmod -R +x /scripts

COPY ./docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

WORKDIR /scripts

ENTRYPOINT ["/docker-entrypoint.sh"]
