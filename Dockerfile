FROM --platform=linux/amd64 node:14 AS builder

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM --platform=linux/amd64 public.ecr.aws/lambda/nodejs:14

COPY package*.json ./

RUN npm ci

COPY --from=builder /lib ./

CMD [ "app.handler" ]
