# Use the manylinux2014_x86_64 image as the base
FROM quay.io/pypa/manylinux2014_x86_64

# Set non-interactive mode to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update CentOS repo to use Aliyun mirror for faster downloads
RUN curl -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.cloud.tencent.com/repo/centos7_base.repo
RUN curl -O /etc/yum.repos.d/epel.repo http://mirrors.cloud.tencent.com/repo/epel-7.repo
RUN yum clean all && yum makecache
RUN yum update

# Install necessary dependencies
RUN yum -y groupinstall "Development Tools"
RUN yum install -y \
    zlib-devel \
    openssl-devel \
    ncurses-devel \
    gdbm-devel \
    libffi-devel \
    sqlite-devel \
    git \
    wget \
    curl \
    gcc-c++ \
    make \
    && yum clean all

# Build python3.8 to python3.13 from source
RUN rm /usr/bin/python3*
RUN rm -r /opt/python/ *

RUN for py_version in 3.8.20 3.9.21 3.10.16 3.11.11 3.12.9 3.13.2; do \
    # Build required python3 version from sources
    curl -O https://www.python.org/ftp/python/$py_version/Python-$py_version.tgz
    tar xzf Python-$py_version.tgz
    cd Python-$py_version && \
    ./configure --enable-optimizations --with-ssl --enable-shared --enable-static --prefix=/opt/python/$py_version && \
    make -j$(nproc) && \
    make altinstall
    cd /opt/python/$py_version/bin && \
    ./python3 --version
    # Install pip dependencies
    export PATH=/opt/python/$py_version/bin:$PATH  && \
	python3 --version && \
	pip3 --version && \
	pip3 install --upgrade pip && \
	pip3 install pybind11 && \
	pip3 install wheel; \
done

# Set working directory in the container
WORKDIR /workspace

# Copy your project files into the container
COPY . /workspace

# Command to run the build script
CMD ["bash", "./scripts/build_whl/build_linux_whl_docker.sh"]

