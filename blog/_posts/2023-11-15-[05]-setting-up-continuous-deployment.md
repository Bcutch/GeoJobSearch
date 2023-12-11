---
layout: post
category: Deployment
---

So far in our journey, we've successfully containerized our application, deployed it locally using docker and minikube, and hosted it on a Kubernetes cluster. This next blog post delves into continuous deployment – the process that ensures any changes made to our repository or code are automatically reflected and deployed to the hosted template application. The key to achieving this lies in using a Gitlab Agent. While other tools like Github Actions, Jenkins, Circle CI, etc., offer similar functionalities, we'll focus on the Gitlab Agent in this guide. Let's explore how we can seamlessly integrate continuous deployment into our application workflow.

---
<h1 align="center">Definitions</h1>
---

**manifest file**: A manifest file in Kubernetes describes the desired state of an application or infrastructure to be applied within our Kubernetes (K8s) cluster. These files serve as a blueprint, outlining the configuration, specifications, and parameters necessary for Kubernetes to manage the deployment.

**CI/CD pipeline**: A CI/CD (Continuous Integration/Continuous Deployment) pipeline is an automated set of processes that facilitates the integration, testing, and deployment of code changes.

---
<h1 align="center">Setting up a Gitlab Agent</h1>
---

The first step in setting up your continuous deployment strategy is by establishing a connection between your remote repository and K8s cluster.  GitLab offers a straightforward solution through GitLab Agents ([full guide](https://docs.gitlab.com/ee/user/clusters/agent/install/)). This section provides a step-by-step guide on GitLab Agent setup:

1. Create a subdirectory in the root of your project named ```.gitlab/agents/agent_name```
2. Create a file inside that directory and name it ```config.yaml```. Paste the following in it:
```yaml
gitops:
  manifest_projects:
  - id: "amerch04/springtemplate"	# Name of your project
    ref:
      branch: deploy
    paths:
    - glob: '/**/*manifest.{yaml, yml, json}'
```

In summary, this config file sets up a GitLab Agent to monitor the project for manifest.yaml files. It specifies that the agent should track the ```deploy``` branch and identifies where the manifest files are stored in the project.

3. Navigate to **infrastructure**>**Kubernetes clusters***
4. Click on **Connect a cluster** in the top right corner of your screen
5. In the dropdown in the middle of your screen, select your GitLab agent, and click **register**

![gitlab-ss]({{site.baseurl}}/assets/img/gitlab-ss.png)

You should now see an access token and a Helm command generated for quick agent setup. We will use the Helm command for the agent setup.

6. ```ssh``` into your server where the K8s cluster is hosted
7. Install [Helm](https://helm.sh/docs/intro/install/) if it's not already installed
8. Paste the ```helm``` command from **Step 5**

Check your GitLab Dashboard to confirm the successful connection of the agent.

![gitlab-ss-2]({{site.baseurl}}/assets/img/gitlab-ss-2.png)

---
<h1 align="center">CI-CD setup</h1>
---

For deploying our application, We use a **combination** of manifest files and GitLab ci-cd pipelines.

> Use **manifests** to deploy general infrastructure that does not require pulling from container registry.

> Use **the pipeline** to deploy pods, ensures that the latest images are pulled after being built and pushed to the container registry.

![ci-cd-setup]({{site.baseurl}}/assets/img/CI-CD-setup.png)

---
<h1 align="center">Manifest file</h1>
---

Creating a manifest file is straightforward. Combine the **services**, **ingress**, and **secret** YAML files from the previous post into one file named **manifest.yaml**. Alternatively, you can have separate files, each ending with manifest.yaml. The content of this manifest file, located in the ```/k8s``` folder, should resemble the following: 

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress
...
---
apiVersion: v1
kind: Service
metadata:
  name: spring-service
...
apiVersion: v1
data:
  .dockerconfigjson: <token>
kind: Secret
metadata:
  name: regcred
```

---
<h1 align="center">Pipeline</h1>
---

Let's configure our GitLab CI/CD pipeline to build and deploy images to the Kubernetes cluster. Follow these steps:

1. Create a new file in the root of the repo and name it ```.gitlab-ci.yml``` (full guide [here](https://docs.gitlab.com/ee/ci/yaml/))
2. Let's define the two stages we will be using by adding the following lines:

```yml
stages:
  - build
  - deploy
```

3. In the same file, Let's add the [Kaniko](https://docs.gitlab.com/ee/ci/docker/using_kaniko.html) image for building and pushing images to the Docker container registry.

```yml
image: 
  name: gcr.io/kaniko-project/executor:v1.14.0-debug
  entrypoint: [""]
```

4. Add individual stages to build images using Kaniko. The rules determine when to trigger the workload based on the branch and folder changes.

```yml
build-spring:
  stage: build
  script:
    - /kaniko/executor --context "./spring" --destination "${CI_REGISTRY_IMAGE}/spring:v0.0.0"
  rules:
    - if: $CI_COMMIT_BRANCH == "deploy"
      changes:
        - spring/**/*

build-mysql:
  stage: build
  script:
    - /kaniko/executor --context "./mysql" --destination "${CI_REGISTRY_IMAGE}/mysql:v0.0.0"
  rules:
    - if: $CI_COMMIT_BRANCH == "deploy"
      changes:
        - mysql/**/*

build-react:
  stage: build
  script:
    - /kaniko/executor --context "./react" --destination "${CI_REGISTRY_IMAGE}/react:v0.0.0"
  rules:
    - if: $CI_COMMIT_BRANCH == "deploy"
      changes:
        - react/**/*
```

5. Let's deploy our application using the ```bitnami/kubectl``` image by adding the following lines:

```yml
deploy-spring-socs:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
    entrypoint: ['']
  script:
    - kubectl config use-context amerch04/springtemplate:socs
    - kubectl apply -f k8s/spring/spring-deployment.yaml
  rules:
    - if: '$CI_COMMIT_BRANCH == "deploy"'

deploy-mysql-socs:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
    entrypoint: ['']
  script:
    - kubectl config use-context amerch04/springtemplate:socs
    - kubectl apply -f k8s/mysql/mysql-deployment.yaml
  rules:
    - if: '$CI_COMMIT_BRANCH == "deploy"'

deploy-react-socs:
  stage: deploy
  image:
    name: bitnami/kubectl:latest
    entrypoint: ['']
  script:
    - kubectl config use-context amerch04/springtemplate:socs
    - kubectl apply -f k8s/react/react-deployment.yaml
  rules:
    - if: '$CI_COMMIT_BRANCH == "deploy"'
```

These lines connect to the Kubernetes cluster and apply the ```deployment.yaml``` files for each app during the deploy stage. 

> Note: We did NOT name them ```manifests.yaml``` so that we can mannually apply them without the gitlab agent's involvment.


---
<h1 align="center">General Deployment Guideline</h1>
---

In our CI/CD setup, we are using a combination of manifest files and pipelines to deploy our application. This approach provides flexibility, allowing you to choose between automatically applying manifest files or automating the deployment process with a pipeline. This template serves as a guide on how to set up your project to support both deployment methods.

If you want to make any new changes to either the **ingress**, **services**, or **secrets**, you would have to:

1. Modify the ```manifest.yaml``` file
2. Push your code to the repo
3. Merge the updates with the ```deploy``` branch

Your changes will be reflected on the host.

For changes to the applications (spring, react, or mysql) to be reflected on the host, you would have to:

1. Modify the ```.gitlab-ci.yml``` file by changing the Kaniko script to create a new image with an updated **Version Tag**
2. Modify the ```<app>-deployment.yaml``` file with the new image tag to pull in the pods
3. Push your code to the repo
4. Merge the updates with the ```deploy``` branch

This approach ensures that your changes are automatically deployed to the Kubernetes cluster through the CI/CD pipeline.