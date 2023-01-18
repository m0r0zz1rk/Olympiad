FROM node:19-alpine

WORKDIR /front

ARG BACKEND_URL
ENV VUE_APP_BACKEND_URL=$BACKEND_URL

ENV PATH /front/node_modules/.bin:$PATH

COPY package.json /front/package.json

RUN npm install --silent

COPY . /front

CMD npm run build
