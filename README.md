# Spring Boot Project with Maven and Docker

This repository contains a complete Java development skeleton configured for Spring Boot, containerized using Docker, managed with Maven, and version-controlled with Git.

## Prerequisites

Before running the application, make sure you have installed:
- [Docker & Docker Compose](https://www.docker.com/products/docker-desktop/)
- [Java JDK 17+](https://adoptium.net/temurin/releases/) (optional for local running without Docker)
- [Maven](https://maven.apache.org/) (optional for local builds without Docker)

---

## Getting Started

### 1. Launch with Docker Compose

To build the Spring Boot application and start it locally in a container network, run:

```bash
docker compose up --build -d
```

Docker Compose will:
1. Build the multi-stage `Dockerfile` (compiling the code inside a Maven build image and packaging it into a minimal JRE container).
2. Start the Spring Boot application on port `8080`.

### 2. Verify the Connection

- **Spring Boot App**: Open [http://localhost:8080](http://localhost:8080) to access the interactive Cloud Deployment Console dashboard.
- **API Endpoint**: Test the REST greeting endpoint directly at [http://localhost:8080/api/hello](http://localhost:8080/api/hello).

---

## Alternative: Build and Run Locally without Docker

### Compile & Package with Maven
```bash
mvn clean package
```

### Run Locally
```bash
java -jar target/demo-0.0.1-SNAPSHOT.jar
```
*The app will start at http://localhost:8080.*
