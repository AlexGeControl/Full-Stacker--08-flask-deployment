# Udacity Full Stack Development Nanodegree

This is the lecture notes for Containerized Service Deployment on AWS EKS of Udacity's Full Stack Development Nanodegree

---

## Containers

One approach to bundle application with its environment and dependencies.

### Container V.S. Virtual Machine

Containers running on the same machine share the same low-level operating system kernel. 

However the VM is like a complete computer, with its own copy of an operating system and virtual hardware. Thus VM could be resource intensive and suffer from the overhead caused.

### Docker Engine

Docker Engine consists of client, API and daemon.

* **Daemon** A server that manages the images, containers, networks, and volumes.
* **Client** The user interface for Docker as a CLI.

### Core Concepts

* **Docker Image** The set of instructions for creating a container.
* **Docker Container** A running instance of an Docker image.
* **Docker Registry** A registry for Docker image storage and distribution.

### DockerHub

DockerHub is the largest and most popular open Docker image registry. DockerHub is the default registry for Docker.

---

## Container Orchestration

One of the major strengths of using containers is **the ease of scaling container instances up and down to meet demands**, known as **horizontal scaling**.

Kubernetes is the most popular container orchestration platform. Its key components include:

* **Cluster** A group of machines running Kubernetes. 
* **Master** The system which controls a Kubernetes cluster. You will typically interact with the master when you communicate with a cluster. The master includes:
    * an api 
    * scheduler
    * management daemon.
* **Nodes** The machines inside a cluster controlled by the master. These machines can be virtual, physical, or a combination of both.
* **Pods** A deployment of an application. This consists of a container, it’s storage resources, and a unique IP address. Pods are not persistent, and may be brought up and down by the master during scaling.

### AWS EKS

Amazon Elastic Kubernetes Service is:

* A managed Kubernetes service
* Control layer runs the master system
* Secure networks are set up automatically
* You only setup Nodes, Pods, and Services

---

## CI/CD -- Build, Test and Deploy Automatically

Automatically building and testing your code when changes are made is called **continuous integration**. 
Continuous integration combined with automated deployment is referred to as **continous delivery**.

--- 

## AWS

### Hands on AWS

First, install awscli

```bash
pip3 install awscli --upgrade
```

AWSCLI: This tool allows you to interact with a wide variety of AWS services, not just EKS. Although there are aws commands to create or modify EKS services, this is a much more manual approach than using the other options.
eksctl: This command line tool allows you to run commands against a kubernetes cluster. This is the best tool for creating or deleting clusters from the command line, since it will take care of all associated resources for you.
kubectl: This tool is used to interact with an existing cluster, but can’t be used to create or delete a cluster.