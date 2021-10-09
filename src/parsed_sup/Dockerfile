FROM python:3.8.11
COPY ./parsed_sup/app/ /app/
COPY ./parsed_sup/requirements.txt /requirements.txt
COPY ./common/ /app/

RUN pip3 install -r /requirements.txt
CMD ["python3", "/app/parsed_sup.py"]