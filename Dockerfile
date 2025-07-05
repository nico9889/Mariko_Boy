FROM docker.io/python:3.13-alpine AS build-deps

RUN pip3 install --no-cache-dir uv

COPY ./requirements.txt /opt/requirements.txt

RUN mkdir /opt/marikoboy/ && uv venv /opt/marikoboy/.venv

ENV PATH="/opt/marikoboy/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/marikoboy/.venv"

RUN uv pip install --no-cache-dir --upgrade -r /opt/requirements.txt

FROM docker.io/python:3.13-alpine
ARG USERNAME=marikoboy
ARG USER_UID=10000
ARG USER_GID=$USER_UID

RUN addgroup --gid $USER_GID $USERNAME \
    && adduser -u $USER_UID -G $USERNAME -H --disabled-password $USERNAME

RUN apk add --no-cache sdl2

WORKDIR /opt/marikoboy

COPY ./marikoboy /opt/marikoboy/marikoboy

COPY --from=build-deps /opt/marikoboy/.venv /opt/marikoboy/.venv

RUN chown $USERNAME -R /opt/marikoboy

USER $USERNAME

ENV PATH="/opt/marikoboy/.venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/marikoboy/.venv"

CMD ["gunicorn", "-k","gevent", "-b", "0.0.0.0", "-w", "1", "marikoboy:app"]

EXPOSE 8000

