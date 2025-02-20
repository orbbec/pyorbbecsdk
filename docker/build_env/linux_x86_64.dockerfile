# Use the official Ubuntu 18.04 image as base
FROM ubuntu:18.04

# Set non-interactive mode to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i 's|http://archive.ubuntu.com/ubuntu|http://mirrors.aliyun.com/ubuntu|g' /etc/apt/sources.list

# Install basic dependencies
RUN apt update
RUN apt upgrade -y
RUN apt install -y software-properties-common
RUN apt install -y \
    build-essential zlib1g-dev libssl-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libreadline-dev libffi-dev libsqlite3-dev \
    git \
    wget \
    curl

# Build cmake 3.15.x from source
RUN wget https://cmake.org/files/v3.15/cmake-3.15.0.tar.gz
RUN tar -zxvf cmake-3.15.0.tar.gz
RUN cd cmake-3.15.0 && mkdir build && cd build && ../configure --prefix=/usr && make -j$(nproc) && make install
RUN cmake --version

# Build python3.10 from source
RUN rm /usr/bin/python3*

RUN curl -O https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz
RUN tar xzf Python-3.10.13.tgz
RUN cd Python-3.10.13 && ./configure --enable-optimizations --with-ssl --enable-shared --enable-static --prefix=/usr && make -j$(nproc) && make altinstall
RUN python3.10 --version

# Link python3.10 to system dir
RUN ln -s $(which python3.10) /usr/bin/python3
RUN ln -s $(which pip3.10) /usr/bin/pip3
RUN ln -s /usr/lib/lipython3* /usr/lib/x86_64-linux-gnu/libpython3*
RUN python3 --version
RUN pip3 --version

# Set python site-packages path for cmake to find
ENV PYTHON3_EXECUTABLE=/usr/bin/python3
ENV PYTHON3_INCLUDE_DIR=/usr/include/python3.10
ENV PYTHON3_LIBRARY=/usr/lib/libpython3.10.so
ENV CMAKE_PREFIX_PATH=/usr/lib/python3.10/site-packages

# Install pybind11 and other Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install pybind11
RUN pip3 install wheel

# Ensure that Python 3.10 is the default Python version
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
# RUN update-alternatives --install /usr/bin/pip3 pip3 /usr/bin/pip3 1

# Set working directory in the container
WORKDIR /workspace

# Copy your project files into the container
COPY . /workspace

# Expose any ports if necessary (optional, for example if you have a web service)
# EXPOSE 8080

# Command to run the build script
CMD ["bash", "./scripts/build_whl/build_linux_whl.sh"]

