FROM --platform=linux/amd64 public.ecr.aws/lambda/nodejs:16 as builder
WORKDIR /usr/app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM --platform=linux/amd64 public.ecr.aws/lambda/nodejs:16
WORKDIR ${LAMBDA_TASK_ROOT}
COPY package*.json ./
RUN npm ci
COPY --from=builder lib/* ./
CMD ["app.handler"]
