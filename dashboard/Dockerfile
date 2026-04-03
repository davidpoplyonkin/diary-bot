FROM node:25.1 AS dashboard
WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build

FROM nginx:latest

COPY --from=dashboard /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
