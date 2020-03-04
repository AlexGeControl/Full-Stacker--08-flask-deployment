#!/bin/bash

aws ssm put-parameter --name JWT_SECRET --value "UdacityFullStackDevelopmentJWTSecret" --type SecureString