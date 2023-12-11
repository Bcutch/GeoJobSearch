---
layout: post
category: Docker
---

Docker, at its core, is a powerful tool that helps in seamlessly deploying applications across various operating systems, including Linux, Windows, and MacOS. Its key strength lies in encapsulating or isolating your program, creating a package that can run on any system that has the Docker runtime installed on it. Applications and their dependencies built using Docker are isolated from the underlying operating system and other containers running on the same machine.

Docker plays a huge role in the world of modern software development world as it allows developers to build microservices. Application that were once built as giant monoliths can now be broken down into smaller, independent, and isolated units communicating with each other using API protocols.

In this blog we’ll dive into the very basics one how to setup containers so that we can later use this knowledge to build the CIS*3760 project template.

---
<h1 align="center">Key Terms in Docker</h1>
---

Before we start, let’s look at the following terms that will serve as the building blocks to containerize our applications.

### Container: 
An isolated process running on a host machine holding all the essential components necessary for your application to run. They are a solution to our old “it works on my machine” problem by creating a standard or consistent environment to run our application.

### Images:
A filesystem that is pulled inside a docker container and has everything needed to run your application. Think of it as a blueprint with application code, dependencies, libraries, and ENV variables. Once created, they can be reused access various environments.

![docker explained]({{site.baseurl}}/assets/img/understand-docker.png)

---
<h1 align="center">How is Docker Used For Our Template</h1>
---

The template app built for CIS*3760 is a simple note app that lets you create, read, update and delete notes. To achieve this, we’re using docker to create three distinct containers:

1. **Sql container:** responsible for running the sql database that stores and manages our notes.
2. **Spring container:** runs the backend code responsible of directly talking with our database and takes care of any logic to manipulate or retrieve data.
3. **React container:** Adds a visual layer to our application, offering an interactive interface to work with the data and communicate with the Spring app.

![docker explained]({{site.baseurl}}/assets/img/app-setup-1.png)

In the next post, we will be going through the specifics of each container, guiding you on how to create a docker image for each one of the applications stated above and how to locally deploy these applications using docker and docker compose. But before we dive into that, lets take a moment and learn a little bit about the concept of Docker files and Docker Compose.

---
<h1 align="center">Understanding Dockerfiles</h1>
---

Earlier in this post we went through what a Docker Image is and how it forms the basis for containers. Now, let’s take a deeper look into creating our own Docker image using a Dockerfile. A Dockerfile is a set of instructions that defines the environment for your application.

### Prerequisites:

Ensure that Docker is installed, and that Docker daemon is up and running on your computer. If not, follow the instructions [here](https://www.docker.com/get-started/).

### Creating a basic node JS app: Step-by-step Guide

1. **Setup your application directory**

Create a new directory for the application and cd into it:

```cd path/to/server```

2. **Create a Simple Node.js Server**

Create your Node.js server by adding the following lines of code to an ‘index.js’ file:

```javascript
const http = require('node:http');

const hostname = '0.0.0.0';
const port = 3000;

const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Hello, World!\n');
});

server.listen(port, hostname, () => {
    console.log(`Server running at http://${hostname}:${port}/`);
});
```

3. **Build your Dockerfile**

Create a Dockerfile in the same directory:

```Dockerfile
FROM node:alpine3.18

WORKDIR /app

COPY . .

EXPOSE 3000

CMD [ "node", "index.js" ]
```

**Explanation:**
- **From [image]** The Dockerfile starts with a FROM clause which defines the base image for our application. Think of it as the pizza base that we can add toppings onto to build our app. Here, we use the “node:alpine3.18” to build our app (which itself is built on top of [other images](https://hub.docker.com/layers/library/node/latest/images/sha256-a9446b301e5c5f20835a3d8df0d31d25e7a86ffe50e97556036bf1f5e638deea?context=explore) such as debian:12 and has Node.js included with it).
- **Workdir [path]** Sets the working directory inside the container. It creates the directory if the directory doesn’t exist already.
- **Copy [src] [dest]** Copies files from our current directory to the docker container. In our case, it’ll copy the index.js file that we need to run.
- **Expose [port]** Informs docker that our container will on port 3000.
- **CMD[“args”]** Defines the entry point of our app and the command to run when our container is ready. In our case, we are starting the node server using the index.js file.

4. **Build and Run your Image:**

Build the image with:

```docker build -t server .```

If you have docker desktop installed, you should be able to see the image in the images section named ‘server’ (Don’t forget the ‘.’, which specifies where the Dockerfile is located).

Run the image with:

```docker run -p 3000:3000 server```

Your server should now be accessible on localhost:3000. The ‘-p 3000:3000’ maps the container port 3000 to port 3000 on our local machine. Explore more Docker run options [here](https://docs.docker.com/engine/reference/commandline/run/)

**Congratulations!** You successfully setup your first server in a Docker container. The containerized application you just created can be run consistently on any machine or os using Docker.

Now let’s consider the scenario where you and your co-worker are working on the same app and are trying to setup the server an identical manner. You could ask them to run the same commands you did, but there is more elegant solution to this and its Docker Compose. In the next section, we’ll explore how Docker Compose simplifies the setup process.

---
<h1 align="center">Understanding Docker Compose</h1>
---

A [docker compose file](https://docs.docker.com/compose/compose-file/) provides a standardized approach to configuring your docker containers. This goes beyond just setting up containers, it allows you to define any services, volumes, and network configurations necessary to run our application. In most cases, this is used for multi-container applications, but we will set it up for our single server created earlier.

### Setting up docker compose: Quick Guide

1. **Create a Compose File:**

Add a compose.yaml file in the root of your project:

```yaml
services:
  server:
    build: .
    ports:
      - "3000:3000"
```

**Explanation:**
- **services** Different containers your application needs.
- **server** The name of the service (can be customized).
- **build**  instructs where to find the Dockerfile.
- **ports ["3000:3000"]** Maps port 3000 from the container to local machine.

2. **Start Your Containers:**

Run the following command to start containers defined in the compose.yaml file:

```
docker compose up
```

**Congratulations!** With the Docker Compose file, you can now share your environment setup with any collaborator and have them run your server on their OS with a single command. This can also be done on any host you would like.
