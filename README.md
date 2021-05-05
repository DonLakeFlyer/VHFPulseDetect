# vhf-pulse-detect

## Introduction

The `vhf-pulse-detect` is an application written in C++ and using mavsdk to get telemetry from the flight controller (over mavlink) and print the data to the standard output.

This application is composed of one Docker container based on `auterion/ubuntu-mavsdk:0.35.1`. This base image is itself based on Ubuntu Focal ARM64V8 (20.04) and contains essential build dependencies to build C++ programs. It also contains mavsdk v0.35.1.
Our container is built using the [multi-stage](https://docs.docker.com/develop/develop-images/multistage-build/) feature from Docker. In the first stage (`build-stage`) we copy our source code and build our application. In the second stage (`release-stage`), we copy the mavsdk binaries from `auterion/ubuntu-mavsdk:0.35.1` and our application binary from the first stage, we also need to install all the dependencies needed to run our application. Finally, using the command `ENTRYPOINT`, we define the startup command that Docker will use to start our container.

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