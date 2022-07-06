FROM python:3.9.11

# serverlessをインストール

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - 
RUN apt-get install -y nodejs

RUN npm install -g serverless@3.12.0

# その他ツールをインストール

RUN pip install pipenv

RUN npm install -g prettier@2.6.2

RUN apt-get install -y openjdk-11-jre
