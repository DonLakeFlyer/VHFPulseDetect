# VHF Pulse Detect

This repository contains source for detection of a VHF pulse at a specific frequency as output by wildlife research collars. It can be run standalone from GNU Radio Companion or on a companion computer running on a drone.

## GNU Radio

### [PulseDetectGui.grc](https://github.com/DonLakeFlyer/VHFPulseDetect/blob/master/src/PulseDetectGui.grc)

This GNU Radio Companion program can be used as a gui for testing the gnu radio scripts which do the pulse detection. They are meant to be used with an AirSpy Mini as the SDR. It's also handy to do things like range testing of the vhf processing. 

### [PulseDetectBase.grc](https://github.com/DonLakeFlyer/VHFPulseDetect/blob/master/src/PulseDetectBase.grc)

This is the main part of VHF signal processing. The construction of this block is based on the dicussion here: https://lists.gnu.org/archive/html/discuss-gnuradio/2017-03/msg00083.html.

Overview of block steps:
* Apply low pass decimating filter multiple times to increase sensitivity/range
* Send the output through a PLL to lock to the specified frequency
* Multiply the PLL and signal output together to filter out freqs we aren't looking for
* Run that through a moving average filter to reduce noise

### [gr-VHFPulseDetect2](https://github.com/DonLakeFlyer/VHFPulseDetect/tree/master/src/gr-VHFPulseDetect2)

This custom block is used for pulse detection from the processed VHF signal. It is loosely based on the discussion here: https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/22640362#22640362. It uses a moving window standard deviation to determine whether there is a true pulse or just noise.

### [gr-VHFPulseSender2](https://github.com/DonLakeFlyer/VHFPulseDetect/tree/master/src/gr-VHFPulseSender2)

This custom block is used to send pulse values out over a UDP port.

### [PulseDetectCommandLineUDP](https://github.com/DonLakeFlyer/VHFPulseDetect/tree/master/src/PulseDetectCommandLineUDP.py)

This is a python script which can be run on a companion computer which will output pulses found over UDP. It is created from the corresponding grc block.

## Auterion Skynode

There is also support for deploying all of this to a Skynode docker as the `vhf-pulse-detect` skynode application. This is still a WIP and is not yet fully complete.

## Commands

You can build the application by running the following command:

```
make build
```

It will create an app artifact in `output/vhf-pulse-detect.auterionos`.

After a successful build, you can connect your Skynode with USB-C and run the following command to install the application on your device:

```
make install
```

You can monitor the application execution by ssh into the device (`ssh root@10.41.1.1`) and run the following command:

```
docker logs vhf-pulse-detect
```

You can stop and remove the application with the following commands:

```
cd /data/app/vhf-pulse-detect/src
docker-compose stop
docker-compose rm -f
docker rmi vhf-pulse-detect
```

Shell into docker
```
docker exec -it vhf-pulse-detect /bin/bash
```
