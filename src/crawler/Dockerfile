FROM python
COPY ./crawler.py /crawler.py
COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt
# CMD [ "python", "/crawler.py" ]
CMD ["scrapy", "runspider", "/crawler.py"]

# RUN pip install -r requirements.txt