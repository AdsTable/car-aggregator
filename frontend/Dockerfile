FROM node:12.8.1-alpine as build-stage

WORKDIR /opt/app

COPY ./package.json .
RUN npm install

COPY . .
ARG configuration=production
RUN npm run build -- --output-path=./dist/out --configuration $configuration

FROM nginx

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build-stage /opt/app/dist/out/ /usr/share/nginx/html

COPY ./nginx/nginx-selfsigned.crt /etc/ssl/certs/nginx-selfsigned.crt
COPY ./nginx/nginx-selfsigned.key /etc/ssl/private/nginx-selfsigned.key
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
