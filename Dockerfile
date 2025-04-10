FROM python:3.12.6-slim-bullseye AS refextract

ARG APP_HOME=/inspire_dojson
WORKDIR ${APP_HOME}

#COPY inspire_dojson inspire_dojson/
#COPY poetry.lock pyproject.toml ${APP_HOME}
COPY . .

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry

#RUN echo "poetry version: $(poetry --version)"
#RUN poetry install
CMD "/bin/bash"
