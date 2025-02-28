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

# Build openssl 1.1.1 greater
RUN wget https://www.openssl.org/source/openssl-1.1.1k.tar.gz
RUN tar -xvzf openssl-1.1.1k.tar.gz
RUN cd openssl-1.1.1k && ./config --prefix=/usr --openssldir=/usr/local/ssl && make -j$(nproc) && make install && ldconfig
RUN openssl version

# Build python3.8 to python3.13 from source
RUN rm -f /usr/bin/python3*
RUN rm -rf /opt/python/* 

# Install multiple Python versions and their dependencies
# 3.12.9 3.13.2 has issue
RUN for py_version in 3.8.20 3.9.21 3.10.16 3.11.11; do \
    # Build required python version from sources
    curl -O https://www.python.org/ftp/python/$py_version/Python-$py_version.tgz && \
    tar xzf Python-$py_version.tgz; \
done

# RUN for py_version in 3.8.20 3.9.21 3.10.16 3.11.11 3.12.9 3.13.2; do \
RUN cd Python-3.8.20 && \
    ./configure --enable-optimizations --with-ssl --enable-shared --enable-static --prefix=/opt/python/3.8.20 && \
    make -j$(nproc) && \
    make altinstall
RUN cd Python-3.9.21 && \
    ./configure --enable-optimizations --with-ssl --enable-shared --enable-static --prefix=/opt/python/3.9.21 && \
    make -j$(nproc) && \
    make altinstall
RUN cd Python-3.10.16 && \
    ./configure --enable-optimizations --with-ssl --enable-shared --enable-static --prefix=/opt/python/3.10.16 && \
    make -j$(nproc) && \
    make altinstall
RUN cd Python-3.11.11 && \
    ./configure --enable-optimizations --with-ssl --enable-shared --enable-static --prefix=/opt/python/3.11.11 && \
    make -j$(nproc) && \
    make altinstall

# Remove python source code for disk save
RUN for py_version in 3.8.20 3.9.21 3.10.16 3.11.11; do \
    rm -rf Python-$py_version && \
    rm -rf Python-$py_version.tgz; \
done

RUN for py_version in 3.8.20 3.9.21 3.10.16 3.11.11; do \
    cd /opt/python/$py_version/bin && \
    ln -s ./python${py_version%.*} ./python3 && \
    ln -s ./pip${py_version%.*} ./pip3 && \
    export PATH=/opt/python/$py_version/bin:$PATH && \
    export LD_LIBRARY_PATH=/opt/python/$py_version/lib:$LD_LIBRARY_PATH && \
    python3 --version && \
    pip3 --version && \
    pip3 install --upgrade pip && \
    pip3 install pybind11 wheel cibuildwheel auditwheel; \
done

# Set working directory in the container
WORKDIR /workspace

# Copy your project files into the container
COPY . /workspace

# Command to run the build script
CMD ["bash", "./scripts/build_whl/build_linux_whl_docker.sh"]

