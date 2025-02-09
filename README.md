# Geo Job Search

CIS*3760 Project

This project will serve as a guide on how to setup a three part application that includes a Spring server, a SQL database and a React frontend both locally and on a Kubernetes host.

## Local Setup

To setup the project locally, you must have [docker](https://www.docker.com/products/docker-desktop/) installed and running on your machine. Once it is setup, run the following command:

``` bash
docker compose up
```

This will setup the app and you can access the following addresses on your browser:

- React frontend = <http://localhost:3000>
- Spring backend = <http://localhost:8080/api> (add **/docs.html** to access Swagger UI)
