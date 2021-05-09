FROM auterion/ubuntu-mavsdk:0.35.1 as build-stage

WORKDIR /source
COPY * .
WORKDIR /source/build
RUN cmake ../ && \
    make

FROM arm64v8/ubuntu as release-stage

ARG DEBIAN_FRONTEND=noninteractive

# MAVSDK dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    libjsoncpp1 \
    libcurl4 \
    libncurses5 \
    libtinyxml2-6a \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=auterion/ubuntu-mavsdk:0.35.1 /buildroot/libmavsdk*.deb /tmp/
RUN dpkg -i /tmp/*.deb

COPY --from=build-stage /source/build/VHFPulseDetectMain /app/

ENTRYPOINT [ "/app/VHFPulseDetectMain", "udp://0.0.0.0:14561" ]
