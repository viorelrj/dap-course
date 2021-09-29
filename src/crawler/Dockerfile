FROM python:alpine
COPY ./crawler.py /crawler.py
COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt
# CMD [ "python", "/crawler.py" ]
CMD ["scrapy", "crawl", "/crawler"]

# RUN pip install -r requirements.txt