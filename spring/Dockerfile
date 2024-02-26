# Stage 1: build
##  Start with a base image from Eclipse Temurin (a distribution of OpenJDK) with Alpine Linux, specifying it as the build stage and naming it "build".
FROM eclipse-temurin:21-jammy as build
WORKDIR /workspace/app

## Copy neccessary files for building the java project
COPY gradlew .
RUN chmod +x ./gradlew
COPY gradle ./gradle
COPY build.gradle .
RUN ./gradlew wrapper
COPY src src