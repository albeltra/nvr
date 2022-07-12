FROM python:3.10.0-alpine

RUN apk update \
    && apk add bash tzdata ffmpeg \
    && rm -rf /var/cache/apk/* \
    && mkdir -p /usr/data/recordings \
    && mkdir -p /usr/data/scripts

COPY ./scripts/* /usr/data/scripts

RUN chmod -R +x /usr/data/scripts

COPY ./docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

WORKDIR /usr/data/scripts

ENTRYPOINT ["/docker-entrypoint.sh"]

