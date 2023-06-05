FROM ubuntu:latest

WORKDIR /ap

RUN apt update \

    && apt install wget \

    && wget https://github.com/77taibai/tsdm/releases/download/v0.1/app.tar \

    && tar -xf ./app.tar \

    && chmod +x ./app

EXPOSE 5000

ENTRYPOINT ["./app"]
