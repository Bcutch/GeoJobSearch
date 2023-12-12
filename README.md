# CIS*3760 Project Template

This project will serve as a guide on how to setup a three part application that includes a Spring server, a SQL database and a React frontend both locally and on a Kubernetes host.

## Local Setup

To setup the project locally, you must have [docker](https://www.docker.com/products/docker-desktop/) installed and running on your machine. Once it is setup, run the following command:

```
docker compose up
```

This will setup the app and you can access the following addresses on your browser:
- React frontend = http://localhost:3000
- Spring backend = http://localhost:8080/api (add **/docs.html** to access Swagger UI)
- Blogs = http://localhost/blogs/


## Local Minikube Setup or remote host setup

To setup the project in a K8s cluster, use the yaml files found in the k8s file and apply them using the following command:

```
kubectl apply -f <file-name.yaml>
```

> Note: This is assuming the container registry has all the images pulled the deployment.yaml files AND the secret token in the manifest file is valid.

You can access the following endpoints on the host that currently runs the application:

- React Frontend = amerch04.socs.uoguelph.ca
- Spring backend = amerch04.socs.uoguelph.ca/api (add **/docs.html** to access Swagger UI)
- Blogs = amerch04.socs.uoguelph.ca/api/blogs
