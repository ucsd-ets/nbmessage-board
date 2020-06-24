# Dockerfile used for DEVELOPMENT environment only

FROM jupyter/datascience-notebook:latest

USER root

# make directories to maintain/configure program state
RUN mkdir -p /etc/nbmessage-board/admin /var/lib/nbmessage-board/test
COPY ./nbmessage_board/static /var/lib/nbmessage-board/static
COPY . /opt/nbmessage-board
COPY ./tests/mocks/nbmessage-board-config.yaml /etc/nbmessage-board

WORKDIR /opt/nbmessage-board

RUN python3 setup.py bdist_wheel
RUN pip install dist/*.whl

RUN jupyter serverextension enable --sys-prefix --py nbmessage_board
RUN jupyter nbextension install --sys-prefix --py nbmessage_board
RUN jupyter nbextension enable --user message/main --section=tree
RUN jupyter nbextension enable --user admin/main --section=tree

