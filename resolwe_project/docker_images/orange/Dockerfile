FROM docker.io/resolwe/base:ubuntu-18.04

RUN apt-get update && apt-get install -y \
    git \
    python3-dev \
    build-essential \
    && pip3 install setuptools wheel cmake \
    # install orange3 from source
    && git clone https://github.com/biolab/orange3 \
    && pip3 install -r ./orange3/requirements-core.txt \
    && pip3 install ./orange3/. \
    # install multicore t-SNE
    && git clone https://github.com/DmitryUlyanov/Multicore-TSNE.git \
    && pip3 install --no-cache-dir ./Multicore-TSNE/. \
    # clean up
    && apt-get remove --purge -y python3-dev git build-essential \
    && pip3 uninstall -y setuptools wheel \
    && rm -rf orange3 \
    && rm -rf Multicore-TSNE \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip \
    && rm -rf /tmp/*

# docker build -t orange_resolwe ./resolwe_project/docker_images/orange/.
# docker run -ti orange_resolwe
# docker rmi -f orange_resolwe