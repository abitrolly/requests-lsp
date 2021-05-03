#!/bin/bash

while true; do podman run --rm -it -p 127.0.0.1:9084:7658 -e LOG_LEVEL=DEBUG docker.io/yakshaveinc/solargraph || bash; done
