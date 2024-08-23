FROM node
MAINTAINER Thomas FADY <thomas.fady@zenika.com>

ADD front/app /app
WORKDIR /app
RUN npm install && npm install --only=dev
ENV NODE_OPTIONS --openssl-legacy-provider
RUN npm run build


FROM python:3.11-alpine
MAINTAINER Thomas FADY <thomas.fady@zenika.com>

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver curl bash

# upgrade pip
RUN pip install --upgrade pip

RUN pip install pipenv

RUN adduser --gecos "" --disabled-password simpleuser
WORKDIR /home/simpleuser
COPY --chown=simpleuser Pipfile Pipfile.lock ./
USER simpleuser
RUN pipenv install
COPY --chown=simpleuser curlbot curlbot
WORKDIR /home/simpleuser/curlbot
RUN export SECRET_KEY=testing ; pipenv run pytest ; for file in $(find -name "test_*.py"); do echo "Delete $file";rm $file; done && for file in $(find -name "*.db"); do echo "Delete $file";rm $file; done
COPY --from=0 /app/dist /home/simpleuser/curlbot/app/front-app
EXPOSE 5000
ENTRYPOINT export SECRET_KEY=$(head /dev/urandom| md5sum | cut -d ' ' -f1) && pipenv run gunicorn -b :5000 run:app -w 4
