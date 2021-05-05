FROM auterion/skynode:customer-base-v2.0.0.0

ENV PYTHONUNBUFFERED=0
ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:/usr/local/lib/python3/dist-packages/VHFPulseSender2

RUN apt update && \ 
    apt install -y --no-install-recommends \
        liborc-0.4-dev \
        cmake \
        g++ make \
        airspy libairspy0 \
        usbutils \
        gr-osmosdr \
        swig \
        gnuradio-dev \
        python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /buildroot/gr-VHFPulseDetect2/
COPY gr-VHFPulseDetect2 .
WORKDIR /buildroot/gr-VHFPulseDetect2/build/
RUN cmake ../ && \
    make && \
    make install && \
    ldconfig

WORKDIR /buildroot/gr-VHFPulseSender2/
COPY gr-VHFPulseSender2 .
WORKDIR /buildroot/gr-VHFPulseSender2/build/
RUN cmake ../ && \
    make && \
    make install && \
    ldconfig

RUN rm -rf /buildroot

WORKDIR /app
COPY --from=auterion/ubuntu-python-mavsdk:latest /install /usr/lib/python3/dist-packages/
COPY get_telemetry.py /app/get_telemetry.py
COPY PulseDetectBase.py /app/PulseDetectBase.py
COPY PulseDetectBase.py.xml /app/PulseDetectBase.py.xml
COPY PulseDetectCmdLineUDP.py /app/PulseDetectCmdLineUDP.py


ENTRYPOINT [ "python3", "/app/get_telemetry.py" ]