# Build Stage
FROM node:23.7 AS build

WORKDIR /app

COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json

RUN npm install
COPY . /app
RUN rm -rf /app/dist
RUN npm run build

# Deployment Stage
FROM nginx:1.27.3

WORKDIR /usr/share/nginx/html

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html
