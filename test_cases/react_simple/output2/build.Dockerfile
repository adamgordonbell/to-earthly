FROM node:19

WORKDIR /app

COPY package*.json ./

RUN npm install -g typescript
RUN npm ci

COPY . .

CMD ["./build.sh"]
