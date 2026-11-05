FROM ubuntu:24.04@sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 git libgmp10 libatomic1 libuv1t64 libcap2 libstdc++6 && rm -rf /var/lib/apt/lists/*
RUN install -d -m 0755 -o 1000 -g 1000 /home/bench
ENV PATH="/opt/lean/bin:/usr/bin:/bin" HOME="/home/bench" LD_LIBRARY_PATH="/opt/lean/lib/lean:/opt/lean/lib"
USER 1000:1000
WORKDIR /work
