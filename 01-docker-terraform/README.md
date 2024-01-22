
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
Create docker network
```bash
docker network create pg-network

docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data -p 5432:5432 --network=pg-network --name pg-database postgres:13
```
pgadmin in docker 
```
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name pgadmin \
    dpage/pgadmin4
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

### Dockerizing the Ingestion Script
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}

docker build -t taxi_ingest:v001 .

docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=pg-database \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
```
Start HTTP server in python
```bash
python -m http.server

URL="http://127.0.0.1:8000/yellow_tripdata_2021-01.csv.gz"
```

### Running Postgres and pgAdmin with Docker-Compose
Services defined in one docker-compose.yml file can communicate with each other without the need to create a network manually.
### SQL Refreshser
```bash
URL="https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv"

python ingest_zones.py \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --url=${URL}
```
```sql
-- explicit inner join
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zone_pick_up."Borough", ' / ', zone_pick_up."Zone") AS pick_up_location,
	CONCAT(zone_drop_off."Borough", ' / ', zone_drop_off."Zone") AS drop_off_location
FROM
	yellow_taxi_trips
	zones zone_pick_up,
	zones zone_drop_off
WHERE
	yellow_taxi_trips."PULocationID" = zone_pick_up."LocationID"
	AND yellow_taxi_trips."DOLocationID" = zone_drop_off."LocationID"
LIMIT 100;

-- inner join
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zone_pick_up."Borough", ' / ', zone_pick_up."Zone") AS pick_up_location,
	CONCAT(zone_drop_off."Borough", ' / ', zone_drop_off."Zone") AS drop_off_location
FROM
	yellow_taxi_trips
	JOIN zones zone_pick_up ON yellow_taxi_trips."PULocationID" = zone_pick_up."LocationID"
	JOIN zones zone_drop_off ON yellow_taxi_trips."DOLocationID" = zone_drop_off."LocationID"
LIMIT 100;

-- check null
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM yellow_taxi_trips
WHERE "DOLocationID" IS NULL;

-- nested query
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM yellow_taxi_trips
WHERE "DOLocationID" NOT IN (SELECT "LocationID" FROM ZONES);

-- left join
SELECT
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zone_pick_up."Borough", ' / ', zone_pick_up."Zone") AS pick_up_location,
	CONCAT(zone_drop_off."Borough", ' / ', zone_drop_off."Zone") AS drop_off_location
FROM
	yellow_taxi_trips
	LEFT JOIN zones zone_pick_up ON yellow_taxi_trips."PULocationID" = zone_pick_up."LocationID"
	LEFT JOIN zones zone_drop_off ON yellow_taxi_trips."DOLocationID" = zone_drop_off."LocationID"
LIMIT 100;

-- group by day & order by day
SELECT
-- 	DATE_TRUNC('DAY', tpep_dropoff_datetime),
	CAST(tpep_dropoff_datetime AS DATE) AS day,
	COUNT(1)
FROM yellow_taxi_trips
GROUP BY CAST(tpep_dropoff_datetime AS DATE)
ORDER BY day ASC;

-- group by day & order by count
SELECT
	CAST(tpep_dropoff_datetime AS DATE) AS day,
	COUNT(1) AS count
FROM yellow_taxi_trips
GROUP BY CAST(tpep_dropoff_datetime AS DATE)
ORDER BY count DESC;

-- max
SELECT
	CAST(tpep_dropoff_datetime AS DATE) AS day,
	COUNT(1) AS count,
	MAX(total_amount),
	MAX(passenger_count)
FROM yellow_taxi_trips
GROUP BY CAST(tpep_dropoff_datetime AS DATE)
ORDER BY count DESC;

-- group by select index
SELECT
	CAST(tpep_dropoff_datetime AS DATE) AS day,
	"DOLocationID",
	COUNT(1) AS count,
	MAX(total_amount),
	MAX(passenger_count)
FROM yellow_taxi_trips
GROUP BY 1, 2
ORDER BY count DESC;
```

### GCP
![Alt text](/01-docker-terraform/documentation/images/image.png)

### Terraform Primer
HashiCorp Terraform is an infrastructure as code tool that lets you define both cloud and on-prem resources in human-readable configuration files that you can version, reuse, and share. You can then use a consistent workflow to provision and manage all of your
infrastructure throughout its lifecycle.
Source - https://developer.hashicorp.com/terraform/intro

why?
- simplicity in keeping track of infrastructure
- easier collaboration
- reproducibility
- ensure resources are removed when not needed
what is not?
- does not manage and update code on infrastructure
- does not give you the ability to change immutable resources
- not used to manage resources not defined in your terraform files

infrastructure as code - allow you make resources in code.
![Alt text](/01-docker-terraform/documentation/images/image3.png)
https://registry.terraform.io/browse/providers

### Terraform CLI
get provider i need
```bash
terraform init
```
what i am about to do
```bash
terraform plan
```
do what is in the tf files
```bash
terraform apply
```
remove everything defined in tf files
```bash
terraform destroy
```
### Terraform Basics
In GCP project go to IAM & Admin -> Service Accounts -> Create Service Account.

Roles: Cloud Storage:Storage Admin, BigQuery:BigQueryAdmin, ComputeEngine:ComputeAdmin.

Manage keys -> Create new key -> JSON -> Create.

```bash
terraform fmt

export GOOGLE_CREDENTIALS='/...'
```

Initialize
```bash
terraform init
```
Plan
```bash
terraform plan
```
Deploy
```bash
terraform apply
```
Get rid of everything
```bash
terraform destroy
```
