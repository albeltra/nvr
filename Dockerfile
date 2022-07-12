FROM ubuntu:focal

RUN apt update \
    && apt upgrade -y;
    && apt install tzdata ffmpeg \

RUN mkdir -p /recordings \
    && mkdir -p /scripts

COPY ./scripts/* /scripts/

RUN chmod -R +x /scripts

COPY ./docker-entrypoint.sh /

RUN chmod +x /docker-entrypoint.sh

WORKDIR /scripts

ENTRYPOINT ["/docker-entrypoint.sh"]

