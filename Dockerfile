# Dockerfile used for DEVELOPMENT environment only

FROM jupyter/datascience-notebook:latest

USER root

# make directories to maintain/configure program state
RUN mkdir -p /etc/nbmessage-board/admin /var/lib/nbmessage-board/{test,mboard}
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

# Chromedriver
# RUN apt-get update
# RUN apt-get install software-properties-common -y 
# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
# RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

# RUN apt-get clean
# RUN apt-get update
# RUN apt-get install google-chrome-stable -y

# RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
# RUN unzip chromedriver_linux64.zip
# RUN mv chromedriver /usr/bin/chromedriver
# RUN chown root:root /usr/bin/chromedriver
# RUN chmod +x /usr/bin/chromedriver

# RUN apt-get install iputils-ping

# RUN useradd -ms /bin/bash user1
# RUN useradd -ms /bin/bash user2
# RUN useradd -ms /bin/bash user3