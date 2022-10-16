FROM node:13
ADD ./app /app
WORKDIR /app
EXPOSE 3000
RUN npm install --silent
ENTRYPOINT ["npm", "start"]
