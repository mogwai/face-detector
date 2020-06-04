#!/bin/bash
docker build -t 382533253677.dkr.ecr.eu-west-1.amazonaws.com/lab/face-detector --build-arg ssh_key="$(cat ~/.ssh/id_rsa)" .
