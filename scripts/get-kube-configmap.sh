#!/bin/bash

kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml