FROM ubuntu
RUN apt-get -y update ; apt-get -y install nodejs npm
WORKDIR /app
COPY front-end/package.json front-end/package-lock.json .
RUN npm install
COPY front-end .
ENTRYPOINT ["npm", "run", "start"]
