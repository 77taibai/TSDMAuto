FROM alpine:latest

WORKDIR /ap

RUN apk update \

    && apk add --no-cache tzdata \

    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \

    && echo "Asia/Shanghai" > /etc/timezone \
    
    && mkdir /lib64 \
    
    && ln -s /lib/libc.musl-x86_64.so.1 /lib64/ld-linux-x86-64.so.2 \
    
    && apk add libc6-compat \

    && apk add wget \

    && wget https://github.com/77taibai/tsdm/releases/download/v0.1/app.tar \

    && tar -xf ./app.tar \

    && chmod +x ./app

EXPOSE 5000

ENTRYPOINT ["./app"]
