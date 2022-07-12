FROM python:3.10.0-alpine

RUN apk update \
    && apk add bash tzdata ffmpeg \
    && rm -rf /var/cache/apk/* \

USER nobody
RUN mkdir -p /recordings \
    && mkdir -p /scripts

COPY ./scripts/* /scripts/

RUN chmod -R +x /scripts

COPY ./docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

WORKDIR /scripts

ENTRYPOINT ["/docker-entrypoint.sh"]

