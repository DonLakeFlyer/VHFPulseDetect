FROM auterion/skynode:customer-base-v2.0.0.0

ENV PYTHONUNBUFFERED=0
ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:/usr/local/lib/python3/dist-packages/VHFPulseSender2

# Install gnu radio dependencies
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
RUN pip3 install six

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
COPY PulseDetectBase.py .
COPY PulseDetectBase.py.xml .
COPY PulseDetectCmdLineUDP.py .
COPY simple.py .
COPY udpTest.py .

ENTRYPOINT [ "python3", "/app/PulseDetectCmdLineUDP.py" ]
#ENTRYPOINT [ "python3", "/app/simple.py" ]
