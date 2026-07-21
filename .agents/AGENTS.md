# AWS ECS Fargate Project Rules & Best Practices

This document defines the guidelines and rules for managing container deployments using AWS ECS Fargate in this project.

## 1. Container Task Sizing (Cost Optimization)
- For dev and testing environments, always use the minimum possible CPU and Memory resources to save costs:
  - **Task CPU**: `512` (0.5 vCPU)
  - **Task Memory**: `1024` (1 GB)
  - Individual container limits must be sub-divisions of these task-level limits.

## 2. Secrets & Environment Variables Management
- **Never hardcode credentials** (like MongoDB URI, passwords, or AWS keys) directly in `task-definition.json`.
- Use environment variable references or fetch secrets from **AWS Systems Manager Parameter Store** or **AWS Secrets Manager** using the ECS Task Execution Role.

## 3. Database Architecture Rules
- Running a database (like MongoDB) in the same task definition as the application container is **only allowed for Development and Testing** environments.
- For Production, databases must be separated from ECS Fargate tasks and hosted on managed database services (e.g., MongoDB Atlas or Amazon DocumentDB) to ensure data persistence and scalability.

## 4. Logging & Monitoring
- All containers in the task definition must use the `awslogs` log driver.
- Ensure log groups are created automatically or exist in CloudWatch (`/ecs/spring-boot-app`) with a retention period configured to avoid high CloudWatch costs.

## 5. Security & Network Access
- ECS Services must be deployed in public subnets with **Public IP enabled** only if direct public access is required.
- Maintain minimal security group permissions (e.g., restrict port 8080 to required IP ranges in production, or use an Application Load Balancer).
