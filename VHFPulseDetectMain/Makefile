appName ?= vhf-pulse-mavlink
toolsPath = //home/parallels/auterion_developer_tools-master/tools

ifneq ($(artifactPath),)
	artifactPath=$(artifactPath)
else
	artifactPath=$(shell pwd)/output/$(appName).auterionos
endif

build-vhf-pulse-main:
	docker build ./src -t $(appName)

build: build-vhf-pulse-main
	mkdir -p output
	docker save $(appName) | gzip > output/$(appName).image
	$(toolsPath)/package_app.sh --app=$(appName)

install:
	$(toolsPath)/update.py --artifact $(artifactPath)
