# Deploying a Flask API

This is the project starter repo for the fourth course in the [Udacity Full Stack Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004): Server Deployment, Containerization, and Testing.

In this project you will containerize and deploy a Flask API to a Kubernetes cluster using Docker, AWS EKS, CodePipeline, and CodeBuild.

The Flask app that will be used for this project consists of a simple API with three endpoints:

- `GET '/'`: This is a simple health check, which returns the response 'Healthy'. 
- `POST '/auth'`: This takes a email and password as json arguments and returns a JWT based on a custom secret.
- `GET '/contents'`: This requires a valid JWT, and returns the un-encrpyted contents of that token. 

The app relies on a secret set as the environment variable `JWT_SECRET` to produce a JWT. The built-in Flask server is adequate for local development, but not production, so you will be using the production-ready [Gunicorn](https://gunicorn.org/) server when deploying the app.

## Initial setup
1. Fork this project to your Github account.
2. Locally clone your forked version to begin working on the project.

## Dependencies

- Docker Engine
    - Installation instructions for all OSes can be found [here](https://docs.docker.com/install/).
    - For Mac users, if you have no previous Docker Toolbox installation, you can install Docker Desktop for Mac. If you already have a Docker Toolbox installation, please read [this](https://docs.docker.com/docker-for-mac/docker-toolbox/) before installing.
 - AWS Account
     - You can create an AWS account by signing up [here](https://aws.amazon.com/#).
     
## Project Steps

Completing the project involves several steps:

1. Write a Dockerfile for a simple Flask API
2. Build and test the container locally
3. Create an EKS cluster
4. Store a secret using AWS Parameter Store
5. Create a CodePipeline pipeline triggered by GitHub checkins
6. Create a CodeBuild stage which will build, test, and deploy your code

---

## EKS Cluster and IAM Roles

### Create a Kubernetes (EKS) Cluster

First, create an EKS cluster using eksctl:
```bash
nohup eksctl create cluster --name uda-full-stack-development --region us-west-2 & > eks-create-cluster.log
```

### Set Up an IAM Role for the Cluster

The next steps are provided to quickly set up an IAM role for your cluster.

#### Create an IAM role that CodeBuild can use to interact with EKS

* Set an environment variable ACCOUNT_ID to the value of your AWS account id. You can do this with awscli:

    ```bash
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    ```

* Create a role policy document that allows the actions "eks:Describe*" and "ssm:GetParameters". You can do this by setting an environment variable with the role policy:

    ```bash
    TRUST="{ \"Version\": \"2012-10-17\", \"Statement\": [ { \"Effect\": \"Allow\", \"Principal\": { \"AWS\": \"arn:aws:iam::${ACCOUNT_ID}:root\" }, \"Action\": \"sts:AssumeRole\" } ] }"
    ```

* Create a role named 'UdacityFlaskDeployCBKubectlRole' using the role policy document:

    ```bash
    aws iam create-role --role-name UdacityFlaskDeployCBKubectlRole --assume-role-policy-document "$TRUST" --output text --query 'Role.Arn'
    ```

* Create a role policy document that also allows the actions "eks:Describe*" and "ssm:GetParameters". You can create the document in your tmp directory:

    ```bash
    echo '{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "eks:Describe*", "ssm:GetParameters" ], "Resource": "*" } ] }' > /tmp/iam-role-policy 
    ```

* Attach the policy to the 'UdacityFlaskDeployCBKubectlRole'. You can do this using awscli:

    ```bash
    aws iam put-role-policy --role-name UdacityFlaskDeployCBKubectlRole --policy-name eks-describe --policy-document file:///tmp/iam-role-policy
    ```

#### Grant the Role Access to the Cluster.

* Get the current configmap and save it to a file:

    ```bash
    kubectl get -n kube-system configmap/aws-auth -o yaml > /tmp/aws-auth-patch.yml
    ```

* In the data/mapRoles section of this document add, replacing <ACCOUNT_ID> with your account id:

    ```yaml
    - rolearn: arn:aws:iam::<ACCOUNT_ID>:role/UdacityFlaskDeployCBKubectlRole
        username: build
        groups:
        - system:masters
    ```

* Now update your cluster's configmap:

    ```bash
    kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /tmp/aws-auth-patch.yml)"
    ```

#### Create GitHub Personal Access Tokens

Generate a GitHub access token. A Github acces token will allow CodePipeline to monitor when a repo is changed. You should generate the token with full control of private repositories, as shown in the image below. Be sure to save the token somewhere that is secure.