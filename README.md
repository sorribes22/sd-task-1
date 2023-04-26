# SD Task 1

## Introduction 
In this project we have created a meteorological service where sensors collect air data, which is sent to a server where it 
is processed and finally the processed data is distributed to terminals.

We have different entities/classes like: Sensors, LoadBalancer (Implementation 1), Server, Proxy and Terminals, a challenge of 
the project is to establish appropriate communication between each node.

The objectives of the project are:
- Test direct communication with gRPC in the Implementation 1.
- Test indirect communication with RabbitMQ in Implementation2.
- Observe the advantages and disadvantages offered by each implementation.
- Learn the ability to decide which communication technology is better depending on the context.
- Try Redis and RabbitMQ services.


## Documentation
### Configuration
All environment parameters are accessed through a single class called Configuration. This class is implemented using a
Singleton pattern in order to load `.env` variables and keeping it in memory.

### Redis implementation
All the measurements stored in redis are written as 'datatype-timestamp:sample' (key:value). The values should be serialized
into a Json in order to follow the "Open for extension, Closed for modification" principle of SOLID. But for this
exercise we skipped it.

### Sensors hierarchy
All sensor implementations extend a Sensor abstract class that has all the communication logic.
This class forces its implementations to define which measure send and where to send it.

### Round Robin
The Round Robin algorithm has been defined as a stub queue. When the load balancer needs a server, it pops it from the
queue. When the server finishes his job the load balancer puts on the end of the queue the stub.

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
manage all requests as fasts as need it could collapse breaking all data detection and procesment.

##### Solution

We can solve it with **redundancy**, if the Load Balancer fails we can have a backup one to replace it.

##### Redis

If we have a lot of data flow or internal issues of the service, Redis can be affected and fail.

##### Solution

We can solve it with **redundancy**.

### Implementation 2

| Section            | Type of communication                                             | Cardinality |
|--------------------|-------------------------------------------------------------------|:-----------:|
| Sensors -> Servers | - **Asynchronous**<br/>- **Pull**<br/>- Transient<br/>- Stateless |   1 -> 1    |
| Proxy -> Terminals | - **Asynchronous**<br/>- **Push**<br/>- Transient<br/>- Stateless |   1 -> N    |

#### Single points of failure

##### RabbitMQ and Redis

We have the same problem as with implementation 1 if one of these services fails we have a problem.

##### Solution

We can solve it with **redundancy**.

### <a name="comparisonbetween2systems"></a>Comparison between 2 systems

By performing both implementations, we have tested communication using **grpc** and **RabbitMQ**. From a programming
perspective, it has been much easier with RabbitMQ as there are no protobuf files or port assignments for each
communication. In terms of **fault tolerance**, we have also found that the indirect implementation with RabbitMQ is
better, as with grpc, if a terminal or sensor stops working, the entire infrastructure throws an error, whereas with
RabbitMQ, if a terminal fails, there is no problem. In terms of **scalability**, RabbitMQ is considerably better because
with grpc, we reserve ports for each connection, which is hard-coded.
On the other hand, with RabbitMQ, we create new instances and connect to the service to easily collect data from the
queue.

### What does a Message Oriented Middleware provide?

A MOM such as RabbitMQ provides a simple implementation of all types of communication between services. It allows to
set up a Asynchronous/Synchronous or Transient/Persistent communication as simple as write 2 or 3 lines of code.
A correct configuration gives our services a strong decoupling and the possibility to scale up as far as we need.

### Briefly describe Redis’ utility as a storage system in this architecture.

Redis can be used to cache data retrieved from grpc, and Provides a very fast response time, making it an excellent
choice for grpc systems that require low latency. On the other hand, Redis is highly scalable and can handle large volumes of data. It is easily horizontally scalable and can work in a distributed environment.
Another advantage is the memory based storage and the matchmaking key-value, this provides fast transference.

## Conclusion
As mentioned in [this comparison](#comparisonbetween2systems), the RabbitMQ implementation is more versatile, scalable
and flexible. We've enjoyed more developing this second implementation than the GRPC one.
We would like to bring the RabbitMQ implementation a step further using RPCs or a RabbitMQ cluster in order to set up
a high availability communication system.

We consider this task a very instructive one and all the suggested objectives achieved.

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

### Setting up all infrastructure
#### gRPC Infrastructure

To prevent the grpc infrastructure from failing, first turn on the terminals and then execute the main.

```bash
venv/bin/python3 main.py grpc_terminal 0
```

```bash
venv/bin/python3 main.py grpc_terminal 1
```

```bash
venv/bin/python3 main.py grpc
```

#### RabbitMQ Infrastructure

In the case of RabbitMQ, it is not necessary to turn on the terminals first.

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


