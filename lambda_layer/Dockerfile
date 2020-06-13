FROM amazonlinux:2

ARG PYTHON_VERSION=3.8.2

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN yum update -y && yum install -y tar gzip make gcc openssl-devel bzip2-devel libffi-devel \
  && curl https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz | tar xz
WORKDIR /Python-${PYTHON_VERSION}
RUN ./configure && make && make install
WORKDIR /
RUN rm -rf Python-${PYTHON_VERSION}

COPY entrypoint.sh /

RUN yum install -y zip \
  && mkdir /python \
  && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
