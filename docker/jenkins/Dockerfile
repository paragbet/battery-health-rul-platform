FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y wget build-essential && \
    wget https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tgz && \
    tar -xzf Python-3.11.9.tgz && \
    cd Python-3.11.9 && \
    ./configure --enable-optimizations && \
    make -j2 && \
    make altinstall && \
    cd .. && \
    rm -rf Python-3.11.9 Python-3.11.9.tgz && \
    apt-get clean

USER jenkins