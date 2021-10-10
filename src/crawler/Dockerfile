FROM python:3.8.11
COPY ./app/ /app/
COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt
CMD ["scrapy", "runspider", "/app/crawler.py", "--nolog"]