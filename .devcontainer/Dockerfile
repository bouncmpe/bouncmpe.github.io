FROM ghcr.io/peaceiris/hugo:latest-full

ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install \
      sudo \
      git \
      make \
      tar curl wget zip unzip gnupg2 \
      python3 \
      python3-pip \
      && \
    apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN groupadd bouncmpe -g 1000 && \
    useradd -ms /bin/bash bouncmpe -g 1000 -u 1000 && \
    printf "bouncmpe:bouncmpe" | chpasswd && \
    printf "bouncmpe ALL= NOPASSWD: ALL\\n" >> /etc/sudoers

USER bouncmpe
WORKDIR /home/bouncmpe

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pre-commit

ENV PATH=/home/bouncmpe/.local/bin:$PATH
