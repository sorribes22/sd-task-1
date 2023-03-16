# SD Task 1
## About this project
resources/task1_statement.pdf

## Deployment
### System requirements
You will need to have the next packages installed and updated:
- docker
- docker-compose

### Docker deployment
To deploy the services requirements you can run:
```bash
docker-compose up -d
```
in the project root. It will deploy a **Redis** and a **RabbitMQ** containers.

## RabbitMQ
To check the RabbitMQ services you can go to http://localhost:15672/ and log with "user" as user and "password" as a
password.  

## Proto compilation
```bash
GRPC_PATH="./src/implementation1/gRPC/"

python3 -m grpc_tools.protoc \
-I="$GRPC_PATH" \
--python_out="$GRPC_PATH" \
--grpc_python_out="$GRPC_PATH" \
--pyi_out="$GRPC_PATH" \
"$GRPC_PATH"MeteoServer.proto
```

## Workflow
This project has been developed by Roxas and axsor.

In order to merge our code contributions we've tried to follow these [rules](https://chris.beams.io/posts/git-commit/).
Once the project scaffold is defined, we've created a Github project was to create every single task forming the entire
project and divide the work to do.

For each task, we create a branch named like task code. Each branch must have 1 commit with task code and a short
description of the contribution.

`git commit -m 'SD-1: implement Load balancer Round Robin algorithm'`

If we couldn't finish a task in a single work cycle we've done the commit and amend the commit on the next cycle:

`git commit --amend`
