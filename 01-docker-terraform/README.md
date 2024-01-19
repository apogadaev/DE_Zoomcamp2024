
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
Create and run pgsql
```bash
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13
```

### CLI tools & Dataset
Install alchemy.
```bash
pip install psycopg2-binary 
pip install SQLAlchemy
```
Install client for pgsql globally.
```bash
pip install pgcli
pgcli -h localhost -p 5432 -u root -d ny_taxi
\dt
\d yellow_taxi_data
```
Download dataset.
```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
gzip -d yellow_tripdata_2021-01.csv.gz
```
Open (option 1).
```bash
less yellow_tripdata_2021-01.csv
```
Open (option 2).
```bash
head -n 100 yellow_tripdata_2021-01.csv
```
Open and copy first 100 to separate file.
```bash
head -n 100 yellow_tripdata_2021-01.csv > yellow_head.csv
```
Count number of lines.
```bash
wc -l yellow_tripdata_2021-01.csv
```
https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv


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
