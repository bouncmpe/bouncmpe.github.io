FROM ghcr.io/peaceiris/hugo:v0.146.4-full

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

# Hinode v2 transpiles SCSS with Dart Sass. Hugo bundles LibSass in its extended
# edition but never Dart Sass, so the binary has to be installed separately.
ARG DART_SASS_VERSION=1.102.0
RUN curl -sSL "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz" \
      | tar -xz -C /opt && \
    ln -s /opt/dart-sass/sass /usr/local/bin/sass && \
    sass --version

RUN groupadd bouncmpe -g 1000 && \
    useradd -ms /bin/bash bouncmpe -g 1000 -u 1000 && \
    printf "bouncmpe:bouncmpe" | chpasswd && \
    printf "bouncmpe ALL= NOPASSWD: ALL\\n" >> /etc/sudoers

USER bouncmpe
WORKDIR /home/bouncmpe

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pre-commit

ENV PATH=/home/bouncmpe/.local/bin:$PATH
