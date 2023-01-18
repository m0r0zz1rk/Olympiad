FROM python:3.10 as builder

WORKDIR /usr/src/drf

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install postgresql gcc python3-dev musl-dev -y

RUN pip install --upgrade pip

COPY . .

COPY ./req.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/drf/wheels -r req.txt

FROM python:3.10

RUN mkdir -p /home/drf

RUN groupadd drf
RUN useradd -m -g drf drf -p !#@olympic2023
RUN usermod -aG drf drf

ENV HOME=/home/drf
ENV APP_HOME=/home/drf/backend
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apt-get update \
    && apt-get install netcat -y

COPY --from=builder /usr/src/drf/wheels /wheels
COPY --from=builder /usr/src/drf/req.txt .

RUN pip install --no-cache /wheels/*

COPY ./entry.sh $APP_HOME
COPY . $APP_HOME

RUN chown -R drf:drf $APP_HOME

USER drf

ENTRYPOINT ["/home/drf/backend/entry.sh"]
