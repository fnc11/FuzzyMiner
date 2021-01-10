FROM node

MAINTAINER Eric eric.pireirik@gmail.com

WORKDIR /root/min-web/dist

COPY . /root/min-web

RUN cd /root/min-web \
    && npm install \
    && npm run build \
    && cd /root/min-web \
    && npm install -g http-server

CMD [ "http-server" ]

