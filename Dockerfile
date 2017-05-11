FROM python:3.6

ENV PATH /usr/local/bin:$PATH
RUN apt-get update && apt-get -y install --no-install-recommends
RUN apt-get install -y wget \
	curl \
	apt-utils

RUN pip3 install -U pip \ 
	setuptools \
	Django 

RUN mkdir code/
WORKDIR code/
ADD . /code/
RUN pip3 install -e .[dev]
RUN cd .. && apt-get install -y nodejs-legacy
RUN cd .. && apt-get install -y nodejs npm
RUN cd .. && npm config set unsafe-perm true
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs
RUN npm install


























