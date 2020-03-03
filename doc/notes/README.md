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

