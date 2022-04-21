FROM python:3.9.11

# Dockerをインストール

RUN apt-get update
RUN apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list >/dev/null

RUN apt-get update
RUN apt-get install -y docker-ce docker-ce-cli containerd.io

# serverlessをインストール

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - 
RUN apt-get install -y nodejs

RUN npm install -g serverless@3.12.0

# その他ツールをインストール

RUN pip install pipenv

RUN npm install -g prettier@2.6.2

RUN apt-get install -y openjdk-11-jre
