FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    coreutils \
    findutils \
    grep \
    gawk \
    sed \
    procps \
    iproute2 \
    iputils-ping \
    net-tools \
    curl \
    dnsutils \
    traceroute \
    openssh-client \
    rsync \
    cron \
    nano \
    less \
    python3 \
    sudo \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Create a non-root training user (Slide 40-41: Least Privilege & UID/GID)
RUN useradd -m -s /bin/bash devuser \
  && echo "devuser:devpass" | chpasswd \
  && mkdir -p /workspace/training_lab

COPY init-lab.sh /usr/local/bin/init-lab.sh
RUN sed -i 's/\r$//' /usr/local/bin/init-lab.sh && chmod +x /usr/local/bin/init-lab.sh

WORKDIR /workspace/training_lab

CMD ["/bin/bash", "-c", "/usr/local/bin/init-lab.sh && exec python3 -m http.server 8080 --directory /workspace/training_lab/docs >/dev/null 2>&1"]
