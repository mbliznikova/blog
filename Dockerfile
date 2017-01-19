FROM alpine:3.1
MAINTAINER Margarita Bliznikova <captainderteufel@gmail.com>

RUN apk add --update python py-pip

ENV INSTALL_PATH /blog
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH

COPY requirements.txt $INSTALL_PATH/
RUN pip install -r requirements.txt

COPY . $INSTALL_PATH/
RUN python manage.py migrate
EXPOSE 8000
ENTRYPOINT ["/usr/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]