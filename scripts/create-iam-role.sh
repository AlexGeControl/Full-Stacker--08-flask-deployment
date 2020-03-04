#!/bin/bash

# identify account id:
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# create role policy document for IAM:
TRUST="{ \"Version\": \"2012-10-17\", \"Statement\": [ { \"Effect\": \"Allow\", \"Principal\": { \"AWS\": \"arn:aws:iam::${ACCOUNT_ID}:root\" }, \"Action\": \"sts:AssumeRole\" } ] }"

# create role in IAM
aws iam create-role \
    --role-name UdacityFlaskDeployCBKubectlRole \
    --assume-role-policy-document "$TRUST" \
    --output text \
    --query 'Role.Arn'

# create role poly document for EKS:
echo '{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "eks:Describe*", "ssm:GetParameters" ], "Resource": "*" } ] }' > /tmp/iam-role-policy 

# create role in EKS:
aws iam put-role-policy \
    --role-name UdacityFlaskDeployCBKubectlRole \
    --policy-name eks-describe \
    --policy-document file:///tmp/iam-role-policy

aws iam attach-role-policy \
    --role-name UdacityFlaskDeployCBKubectlRole \
    --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess

aws iam attach-role-policy \
    --role-name UdacityFlaskDeployCBKubectlRole \
    --policy-arn arn:aws:iam::aws:policy/AWSCodeBuildAdminAccess
