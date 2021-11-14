FROM python:3.8.9
COPY ./service/app/ /app/
COPY ./service/requirements.txt /requirements.txt
COPY ./common/ /app/

RUN pip3 install -r /requirements.txt
CMD ["python3", "-u", "/app/service.py"]