FROM python:3.8.9
COPY ./crawler_manager/app/ /app/
COPY ./crawler_manager/requirements.txt /requirements.txt
COPY ./common/ /app/

RUN pip3 install -r /requirements.txt
CMD ["python3", "/app/crawler_manager.py"]