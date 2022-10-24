FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system

COPY index.py .

CMD [ "index.lambda_handler" ]
