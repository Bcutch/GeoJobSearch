# Use Eclipse Temurin 21 (Java 21) as the base image for the build stage
FROM eclipse-temurin:21-jammy as build

# Set the working directory inside the Docker image
WORKDIR /workspace/app

<<<<<<< HEAD
# Copy the Gradle wrapper and necessary files
COPY gradlew .
COPY gradle gradle
COPY build.gradle .
COPY settings.gradle .


# Make the Gradle wrapper executable
RUN chmod +x ./gradlew

# Use the Gradle wrapper to ensure the project is properly set up
RUN ./gradlew wrapper

# Copy the project source
COPY src src

# At this stage, you can build the project if needed, or prepare for bootRun
# No explicit build command here, as we will use bootRun to run the application in the final stage

# Use Eclipse Temurin 21 (Java 21) for the runtime stage
FROM eclipse-temurin:21-jammy

WORKDIR /app

# Copy the built application or the necessary files from the build stage
COPY --from=build /workspace/app .

# Expose the port the application runs on
EXPOSE 8080

# Command to run the application. Adjust if you perform a build and run a JAR file instead
CMD ["./gradlew", "bootRun"]
=======
## Copy neccessary files for building the java project
COPY gradlew .
RUN chmod +x ./gradlew
COPY gradle ./gradle
COPY build.gradle .
RUN ./gradlew wrapper
COPY src src
>>>>>>> d8be8dc (fixed file structure for backend, created devcontainers for docker, create simplae route in backend, chnaged from maven to gradle for building and updated dockerfile to work with it.)
