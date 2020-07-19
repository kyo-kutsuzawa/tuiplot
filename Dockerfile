FROM ubuntu:20.04
LABEL maintainer "Kyo Kutsuzawa <kutsuzawa@tohoku.ac.jp>"

# Specify a time-zone (without them, build is interrupted to configure tzdata)
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo

# Setup python3
RUN apt-get update \
    && apt-get install -y \
        python3-dev \
        python3-pip \
        python3-tk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Setup python packages
RUN pip3 install \
        numpy==1.19.0 \
        scipy==1.5.1 \
        matplotlib==3.2.2

# Change python command to run python 3.6
RUN update-alternatives --remove python /usr/bin/python2 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

RUN apt-get update \
    && apt-get install -y \
        vim \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

