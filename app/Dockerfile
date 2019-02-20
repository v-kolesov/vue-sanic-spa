# окончательный вид app/Dockerfile
FROM node:10.15.0-alpine
RUN apk add --no-cache bash
RUN npm install -g @vue/cli
WORKDIR /app
VOLUME ["/app"]
RUN npm install 
EXPOSE 8080
CMD ["npm", "run", "serve"]