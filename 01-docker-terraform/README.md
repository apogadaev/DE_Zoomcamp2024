
### Data Pipelines & Docker
- Process or service that gets some input data froume source and produces output data to destination is called **Data Peipeline (DP)**. There can be multiple data sources, destinations and multiple.
![Alt text](/01-docker-terraform/documentation/images/image1.png)
- Each DP has it's own dedicated docker container with all required dependencies.
![Alt text](/01-docker-terraform/documentation/images/image2.png)
- Docker images provide us 100% reproduceability in different environments.

### Docker CLI
Overwrite entrypoint process in container.
```bash
docker run -t --entrypoint=bash python:3.9 
```
Define a tag:version to container.
```bash
docker build -t test:pandas .; docker run -t test:pandas
```
Add to docker file in order to create workdirectory and copy pipeline script to it.
```Dockerfile
WORKDIR /app
COPY pipeline.py pipeline.py
```

### Example
Run a pipeline on specific day
```python
# pipeline.py
import sys

print(sys.argv)
day = sys.argv[1]

print('Job finished successfully for day = f{day}.')
```

```Dockerfile
# Dockerfile
ENTRYPOINT [ "python", "pipeline.py" ]
```
"2024-01-19" is the sys argument for the container
```bash
docker run -t test:pandas 2024-01-19
```
