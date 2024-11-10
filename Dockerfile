FROM 'mirror.gcr.io/library/python:3.11.7-bullseye'

ARG USER=user
ARG APPDIR=/app
ENV VIRTUAL_ENV=${APPDIR}/venv

RUN apt update && apt install -y libgraphviz-dev graphviz --no-install-recommends
WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt

RUN python3 -m venv ${VIRTUAL_ENV} \
  && . ${VIRTUAL_ENV}/bin/activate \
  && pip install --upgrade wheel setuptools pip \
  && pip install cython \
  && pip install -r /tmp/requirements.txt

RUN apt autoremove -y \
  && apt autoclean -y \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /tmp/*

RUN groupadd --gid 1000 $USER \
  && useradd --uid 1000 --gid $USER $USER \
  && chown -R $USER:$USER /app

RUN mkdir /home/${USER} && chown -R ${USER}:${USER} /home/${USER}

USER $USER
ENV PYTHONPATH=${APPDIR} PATH=${PYTHONPATH}:${VIRTUAL_ENV}/bin/:$PATH
