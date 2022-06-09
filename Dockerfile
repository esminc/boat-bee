FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

COPY app.py ./
COPY ./bee_slack_app/ ./bee_slack_app/

CMD [ "app.lambda_handler" ]
