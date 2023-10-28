FROM node:16-alpine
WORKDIR /app
COPY /front .
RUN npm i
RUN npm run build
ENV NODE_ENV production
EXPOSE 3000
CMD [ "npx", "serve", "-s", "build" ]