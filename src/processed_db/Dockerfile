FROM docker.io/bitnami/postgresql:latest

COPY ./init.sh /etc/init.d/my-startup.sh
USER root
RUN apt-get update