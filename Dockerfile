# Docker file for pull_scp ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build --build-arg UID=$UID -t local/pl-pull_scp .
#
# In the case of a proxy (located at 10.41.13.4:3128), do:
#
#    PROXY=http://10.41.13.4:2138
#    docker build --build-arg http_proxy=$PROXY --build-arg UID=$UID -t local/pl-pull_scp .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-pull_scp
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-pull_scp
#

FROM python:3.9.1-slim-buster
LABEL maintainer="Rudolph Pienaar -- FNNDSC <rudolph.pienaar@childrens.harvard.edu>"

WORKDIR /usr/local/src

COPY requirements.txt .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN pip install .
# COPY pull_scp/.env /usr/local/lib/python3.9/site-packages/pull_scp
COPY key.pub        /tmp
COPY pull_scp/.env  /tmp

CMD ["pull_scp", "--help"]
