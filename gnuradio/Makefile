appName ?= vhf-pulse-detect
toolsPath = //home/parallels/auterion_developer_tools-master/tools

ifneq ($(artifactPath),)
	artifactPath=$(artifactPath)
else
	artifactPath=$(shell pwd)/output/$(appName).auterionos
endif

build-vhf-pulse-detect:
	docker build . -t vhf-pulse-detect

build: build-vhf-pulse-detect
	mkdir -p output
	docker save vhf-pulse-detect | gzip > output/$(appName).image
	$(toolsPath)/package_app.sh --app=$(appName)

install:
	$(toolsPath)/update.py --artifact $(artifactPath)
