FROM python:3.9.6-slim-buster
RUN mkdir /bitrix
WORKDIR /bitrix
COPY requirements.txt /bitrix/
RUN pip install -r requirements.txt
COPY . /bitrix/