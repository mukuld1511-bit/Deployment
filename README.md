# Spring Boot Project with Maven, Docker, and ngrok

This repository contains a complete Java development skeleton configured for Spring Boot, containerized using Docker, managed with Maven, version-controlled with Git, and configured to tunnel externally via ngrok.

## Prerequisites

Before running the application, make sure you have installed:
- [Docker & Docker Compose](https://www.docker.com/products/docker-desktop/)
- [Java JDK 17+](https://adoptium.net/temurin/releases/) (optional for local running without Docker)
- [Maven](https://maven.apache.org/) (optional for local builds without Docker)

---

## Getting Started

### 1. Configure ngrok Authtoken

To use the ngrok tunneling container, you need a free ngrok authtoken.
1. Sign up/log in to [ngrok dashboard](https://dashboard.ngrok.com/).
2. Copy your **Authtoken**.
3. Create a `.env` file in the root directory of this project:
   ```env
   NGROK_AUTHTOKEN=your_actual_ngrok_authtoken_here
   ```

*(Note: `.env` is ignored by Git, so your token remains private and safe).*

### 2. Launch with Docker Compose

To build the Spring Boot application and start both the app and the ngrok tunnel automatically, run:

```bash
docker compose up --build
```

Docker Compose will:
1. Build the multi-stage `Dockerfile` (compiling the code inside a Maven build image and packaging it into a minimal JRE container).
2. Start the Spring Boot application on port `8080`.
3. Start the ngrok container, linking it to the app, and expose a secure public URL.

### 3. Verify the Connections

- **Spring Boot App (Local)**: Open [http://localhost:8080/api/hello](http://localhost:8080/api/hello) to see the local response.
- **ngrok Local Dashboard**: Open [http://localhost:4040](http://localhost:4040). This is the local ngrok status console where you will find your dynamically generated public forwarding URL (e.g., `https://xxxx-xx-xx-xx.ngrok-free.app`).
- **External Access**: Visit your public ngrok URL with `/api/hello` added at the end (e.g., `https://xxxx-xx-xx-xx.ngrok-free.app/api/hello`) to test access from outside your local network.

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
*The app will start at http://localhost:8080/api/hello.*
