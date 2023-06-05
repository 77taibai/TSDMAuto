FROM alpine:latest

WORKDIR /app

RUN apk update \

    && apk add --no-cache tzdata \

    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \

    && echo "Asia/Shanghai" > /etc/timezone \

    && apk add wget \

    && wget https://github.com/77taibai/tsdm/releases/download/v0.1/app.tar \

    && tar -zxvf ./app.tar \

    && chmod +x ./app

EXPOSE 5000

ENTRYPOINT ["./app"]