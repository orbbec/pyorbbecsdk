FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
  build-essential \
  cmake \
  python3-dev \
  python3-pip \
  python3-setuptools \
  g++ \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Install Python3 and pybind11 dependencies
RUN pip3 install pybind11FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
  build-essential \
  cmake \
  python3-dev \
  python3-pip \
  python3-setuptools \
  g++ \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Install Python3 and pybind11 dependencies
RUN pip3 install pybind11

# Set up the environment for building
WORKDIR /src

