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

# Switch python3 version
RUN for py_version in cp38-cp38 cp39-cp39 cp310-cp310 cp311-cp311 cp312-cp312 cp313-cp313; do \
	export PATH=/opt/python/$py_version/bin:$PATH  && \
	python3 --version && \
	pip3 --version && \
	pip3 install --upgrade pip && \
	pip3 install pybind11 && \
	pip3 install wheel; \
#	pip3 install setuptools; \
done

# Set working directory in the container
WORKDIR /workspace

# Copy your project files into the container
COPY . /workspace

# Command to run the build script
CMD ["bash", "./scripts/build_whl/build_linux_whl_docker.sh"]

