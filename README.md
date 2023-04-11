# SD Task 1
## About this project
resources/task1_statement.pdf

## Documentation
### Implementation 1
| Section                  | Type of communication                                            | Cardinality |
|--------------------------|------------------------------------------------------------------|:-----------:|
| Sensors -> Load Balancer | - **Synchronous**<br/>- **Pull**<br/>- Transient<br/>- Stateless |   N -> 1    |
| Load Balancer -> Servers | - **Synchronous**<br/>- **Pull**<br/>- Transient<br/>- Stateless |   1 -> N    |
| Proxy -> Terminals       | - **Synchronous**<br/>- **Push**<br/>- Transient<br/>- Stateless |   1 -> N    |

| Single points of failure | Solution |
|--------------------------|----------|
|                          |          |
|                          |          |

### Implementation 2
| Section            | Type of communication                                             | Cardinality |
|--------------------|-------------------------------------------------------------------|:-----------:|
| Sensors -> Servers | - **Asynchronous**<br/>- **Pull**<br/>- Transient<br/>- Stateless |   N -> N    |
| Proxy -> Terminals | - **Asynchronous**<br/>- **Push**<br/>- Transient<br/>- Stateless |   N -> N    |


| Single points of failure | Solution |
|--------------------------|----------|
|                          |          |
|                          |          |

### Comparison between 2 systems

### What does a Message Oriented Middleware provide?

### Briefly describe Redis’ utility as a storage system in this architecture. 

## Deployment
### Project requirements
To install project requirements you can run these commands:
```bash
python3 -m venv venv
venv/bin/python3 -m pip install -r requirements.txt
```
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

### Setting up all infraestructure
```bash
venv/bin/python3 main.py terminal 0
```
```bash
venv/bin/python3 main.py terminal 1
```
```bash
venv/bin/python3 main.py all
```

## RabbitMQ
To check the RabbitMQ services you can go to http://localhost:15672/ and log with "user" as user and "password" as a
password.  

## Proto compilation
```bash
python3 -m grpc_tools.protoc \
    --proto_path="." \
    --grpc_python_out="." \
    --python_out="." \
    --pyi_out="." \
    ./src/implementation1/gRPC/*.proto
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

```bash
git commit --amend
git push --force-with-lease
```
