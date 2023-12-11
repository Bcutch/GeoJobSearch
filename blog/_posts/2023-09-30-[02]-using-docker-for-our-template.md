---
layout: post
category: Docker
---

In our previous post, we introduced our application consisting of three independent containers featuring a Spring server, a SQL database, and a React frontend server. Each component operates autonomously, handling connection errors with other services without causing a system-wide crash. Without further ado, let's dive into the details of setting up these independent yet interconnected services!

---
<h1 align="center">Spring Container</h1>
---

The Spring container acts as the intermediary service, bridging the gap between the database and the frontend. It's designed to be accessible directly via the '/api' endpoint. It is constructed using [Spring Initializr](https://start.spring.io/) with dependencies like Spring Data JPA, MySQL Driver, and Spring Web.

### File Structure

```
spring/
├─ src/
│  ├─ main/
│  │  ├─ java/.../spring/template/
│  │  │  ├─ controllers/
│  │  │  │  ├─ NotesController.java
│  │  │  ├─ notes/
│  │  │  │  ├─ models/
│  │  │  │  │  ├─ Note.java
│  │  │  │  ├─ dao/
│  │  │  │  │  ├─ NotesDao.java
│  │  │  │  ├─ NotesService.java
│  │  │  ├─ TemplateApplication.java
│  │  ├─ resources/
│  │  │  ├─ application.properties
│  ├─ test/
├─ mvnw
```

![docker explained]({{site.baseurl}}/assets/img/spring-setup.png)

Key components to look out for in this structure include the controller class (NotesController.java), the service class (NotesService.java), and the model (Note.java). With [Spring JPA](https://docs.spring.io/spring-data/jpa/reference/index.html), your SQL tables get mapped to object models. For this to work, make sure to align column names with variables in the model class.

However, to make this service fully independent of databases, certain Spring JPA properties in the application.properties file require modification:

```
spring.jpa.properties.hibernate.temp.use_jdbc_metadata_defaults=false
spring.jpa.generate-ddl=false
spring.jpa.hibernate.ddl-auto=none
```
These settings prevent Spring JPA from attempting to create or modify tables during startup, avoiding the risk of app to crash in case of connection issues.

> ENV variables needed > DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD: To setup the connection to our sql server.

### Spring App DockerFile

The following DockerFile is a little more complicated than the one we built in our first post (but the concept stays the same):

```Dockerfile
# Stage 1: build
##  Start with a base image from Eclipse Temurin (a distribution of OpenJDK) with Alpine Linux, specifying it as the build stage and naming it "build".
FROM eclipse-temurin:17-jdk-alpine as build
WORKDIR /workspace/app

## Copy neccessary files for building the java project
COPY mvnw .
RUN chmod +x ./mvnw
COPY .mvn .mvn
COPY pom.xml .
COPY src src

## Use Maven to build the application using the RUN stanza
RUN ./mvnw install -DskipTests
RUN mkdir -p target/dependency && (cd target/dependency; jar -xf ../*.jar)

# Stage 2: runtime
## Start a new stage, using a fresh Alpine-based image from Eclipse Temurin.
FROM eclipse-temurin:17-jdk-alpine
ARG DEPENDENCY=/workspace/app/target/dependency

## Only copy necessary files
COPY --from=build ${DEPENDENCY}/BOOT-INF/lib /app/lib
COPY --from=build ${DEPENDENCY}/META-INF /app/META-INF
COPY --from=build ${DEPENDENCY}/BOOT-INF/classes /app

## Start the srping app
ENTRYPOINT ["java","-cp","app:app/lib/*","com.example.cis4900.spring.template.TemplateApplication"]
```

The dockerfile created in for this project uses a multi-stage build process. The first stage builds the Java application with Maven, and the second stage creates a lightweight runtime image with only the artifacts needed for running the application. This approach saves time and memory by excluding unneccessary build dependencies. A full guide on how you can containerize your spring app can be found [here](https://spring.io/guides/topicals/spring-boot-docker/)

---
<h1 align="center">SQL Container</h1>
---

The mysql container is pretty straightforward to understand. It hosts a database and initializes a table using the setup.sql script provided with the code.

### MySQL Dockerfile

```Dockerfile
# Use the mysql image
FROM mysql

# Copy all the files in the docker-entrypoint-initdb.d inside the container 
# which will run automatically when the sql server will start
COPY ./scripts/setup.sql /docker-entrypoint-initdb.d/
```

This Dockerfile uses the official MySQL image and copies the setup.sql script into the /docker-entrypoint-initdb.d/ directory. The script is automatically executed when the MySQL server starts.

> ENV variables needed > MYSQL_ROOT_PASSWORD, MYSQL_DATABASE: To setup the database as a root user with a password and the name of the initial database to be created on startup.

---
<h1 align="center">React Container</h1>
---

The React container is responsible for hosting the frontend of our application. The project template was initiated using npm ```create-react-app react```. For more detailed guides on creating a React app, refer to this [documentation](https://legacy.reactjs.org/docs/create-a-new-react-app.html).  In our setup, the React app communicates with the Spring app's '/api' endpoint to perform operations such as retrieving, creating, updating, and deleting data. The app uses [bootstrap](https://getbootstrap.com/) components for styling.

### File Structure

```
react/
├─ public/
├─ src/
│  ├─ components/
│  ├─ pages/
│  │  ├─ HomePage/
│  ├─ App.js
│  ├─ App.css
│  ├─ index.js
│  ├─ index.css
├─ package.json
```

### React App DockerFile

```Dockerfile
# Use the Node.js 18 Alpine image as the base image
FROM node:18-alpine

# Copy package.json and package-lock.json to the image
# We need them to build the dependencies for our project
COPY package.json package.json
COPY package-lock.json package-lock.json

# Run `npm ci` to install project dependencies
RUN npm ci

# Set environment variables
ENV CI=true
ENV PORT=3000

# Copy the entire project directory to the image
COPY . .

# Default command to start the app
CMD [ "npm", "start" ]
```

This Dockerfile configures a Node.js environment, installs dependencies, sets necessary environment variables, copies project files, and specifies the default command to run the application.

> ENV variables needed > BACKEND_PROXY: Specifies where the spring server is running.

---
<h1 align="center">Setting up Docker Compose</h1>
---
Let's explore how to deploy our applications locally and facilitate communication between them using Docker Compose. The Docker Compose file for our Spring template may seem a bit hard to understand initially, but let's break it down step by step.

There aren't many things at play here. The following diagram will give you a better idea of what we are trying to achieve.

![Docker Compose]({{site.baseurl}}/assets/img/docker-compose.png)

In Docker, where containers operate in isolation, networking plays a crucial role in enabling services to discover and communicate with each other. The diagram illustrates our networks to interconnect services and exposing the Spring and React apps to end-users.

Since Docker containers are isolated, we are making use of **networks** to allow our services to find each other. For local deployments on our machine, accessing each service would typically involve using the 'localhost' link. However, within Docker, the hostname transforms to the service's name. For instance, while our Spring server would run at http://localhost:8080 locally, within Docker, its address becomes http://spring:8080.

### Docker Compose File

```yaml
services:
  spring:
    build: ./spring
    ports:
      - "8080:8080"
    environment:
      # These are used in apllication.property to setup DB connection
      - DB_ADDRESS=jdbc:mysql://mysql:3306
      - DB_DATABASE=template_db
      - DB_USER=root
      - DB_PASSWORD=pwd
    networks:
      - spring-mysql
      - spring-react

  mysql:
    build: ./mysql
    environment:
      # Mysql docker image env vars
      - MYSQL_ROOT_PASSWORD=pwd
      - MYSQL_DATABASE=template_db
    networks:
      - spring-mysql
    
  react:
    build: ./react
    ports:
      - "3000:3000"
    environment:
      # Tell the react app that our spring server is running here
      - BACKEND_PROXY=http://spring:8080
    networks:
      - spring-react
    
networks:
  spring-mysql:
  spring-react:

```

This Docker Compose file orchestrates the deployment of our services. Let's highlight a few key aspects:

- **Spring Service:** Builds the Spring container, exposes it on port 8080, and connects it to the 'spring-mysql' and 'spring-react' networks.
- **MySQL Service:** Builds the MySQL container, sets necessary environment variables, and connects it to the 'spring-mysql' network.
- **React Service:** Builds the React container, exposes it on port 3000, and informs it about the Spring server's location using the 'BACKEND_PROXY' environment variable. This service is connected to the 'spring-react' network.
- **Networks:** Two networks, 'spring-mysql' and 'spring-react,' facilitate communication between services.

Running ```docker compose up``` in the root of our project will setup the containers locally and you'll be able to access them on ports 3000 (React) and 8080 (Spring) on your localhost.
