package=cloud
UNAME=$(shell uname)
VERSION=`head -1 ../../VERSION`

define banner
	@echo
	@echo "###################################"
	@echo $(1)
	@echo "###################################"
endef

######################################################################
# DOCKER
######################################################################

all: clean image

image:
	$(call banner, "Building cloudmesh/cloudmesh-${package}")
	docker build -t cloudmesh/cloudmesh-${package}:${VERSION} .
	docker tag cloudmesh/cloudmesh-${package}:${VERSION} \
		cloudmesh/cloudmesh-${package}:latest
	$(call banner, "tag cloudmesh/cloudmesh-${package}:${VERSION} cloudmesh/cloudmesh-${package}:latest")

shell:
	docker run \
		-v `pwd`:/cloudmesh \
		-v ~/.cloudmesh:/root/.cloudmesh \
		-w /cloudmesh --rm \
		-it cloudmesh/cloudmesh-${package}:${VERSION} /bin/bash

clean:
	-docker system prune -a
	-docker images purge
	#-docker kill $$(docker ps -q)
	#-docker rm $$(docker ps -a -q) 
	#-docker rmi $(docker images -a -q) --force
	-docker ps
	-docker image ls

push:
	docker push cloudmesh/cloudmesh-${package}:${VERSION}
