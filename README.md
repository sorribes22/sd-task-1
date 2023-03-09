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
in the project root.
It will deploy a **Redis** and a **RabbitMQ** containers.

## Proto compilation
```bash
cd src/implementation1/gRPC

python3 -m grpc_tools.protoc \
-I=./ \
--python_out=. \
--grpc_python_out=. \
--pyi_out=. \
MeteoServer.proto
```
