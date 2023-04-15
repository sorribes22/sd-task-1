# SD Task 1
## About this project
resources/task1_statement.pdf

## Documentation
### Implementation 1
| Section                   | Type of communication                                               | Cardinality |
|---------------------------|---------------------------------------------------------------------|:-----------:|
| Sensors -> Sensor servers | - **Synchronous**<br/>- **Pull**<br/>- Transient<br/>- Stateless    |   1 -> 1    |
| Sensors -> Load Balancer  | - **Synchronous**<br/>- **Pull**<br/>- Transient<br/>- Stateless    |   1 -> 1    |
| Load Balancer -> Servers  | - **Synchronous**<br/>- **Pull**<br/>- Transient<br/>- **Stateful** |   1 -> 1    |
| Proxy -> Terminals        | - **Synchronous**<br/>- **Push**<br/>- Transient<br/>- Stateless    |   1 -> N    |

#### Single points of failure
##### Load balancer
This entity is where all the messages between sensors and sensor servers must pass with. If it falls or can not
manage all requests as fasts as need it could colapse breaking all data detection and procesment.
##### Solution

### Implementation 2
| Section            | Type of communication                                             | Cardinality |
|--------------------|-------------------------------------------------------------------|:-----------:|
| Sensors -> Servers | - **Asynchronous**<br/>- **Pull**<br/>- Transient<br/>- Stateless |   1 -> 1    |
| Proxy -> Terminals | - **Asynchronous**<br/>- **Push**<br/>- Transient<br/>- Stateless |   1 -> N    |


#### Single points of failure
##### SPF
##### Solution

### Comparison between 2 systems

### What does a Message Oriented Middleware provide?
A MOM such as RabbitMQ provides a simple implementation of all types of communication between services. It allows to
set up a Asynchronous/Synchronous or Transient/Persistent communication as simple as write 2 or 3 lines of code.
A correct configuration gives our services a strong decoupling and the possibility to scale up as far as we need.

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
#### gRPC Infraestructure
```bash
venv/bin/python3 main.py grpc_terminal 0
```
```bash
venv/bin/python3 main.py grpc_terminal 1
```
```bash
venv/bin/python3 main.py grpc
```
#### RabbitMQ Infraestructure
```bash
venv/bin/python3 main.py rabbitmq_terminal
```
```bash
venv/bin/python3 main.py rabbitmq_terminal
```
```bash
venv/bin/python3 main.py rabbitmq
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
## TODO
On estan els possibles SPF?
És normal la dependència entre terminals i proxy en grpc? Si

