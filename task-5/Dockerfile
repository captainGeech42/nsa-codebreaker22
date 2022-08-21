FROM library/ubuntu:20.04

RUN apt-get update
RUN apt-get -qq -y install \
    openssh-server \
    gdb \
    curl \
    wget \
    elfutils \
    binutils \
    file \
    libc-bin \
    libc-dev \
    vim \
    build-essential \
    libssl-dev \
    autoconf \
    zlib1g-dev

RUN bash -c "$(curl -fsSL https://gef.blah.cat/sh)"

ENV LC_CTYPE C.UTF-8

WORKDIR /root
COPY .gdbinit gdbinit
RUN cat .gdbinit gdbinit > a
RUN mv a .gdbinit
RUN rm gdbinit

RUN mkdir /vol
WORKDIR /vol