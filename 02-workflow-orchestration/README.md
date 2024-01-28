## 2.2.1 What is Orchestration?

![Alt text](documentation/image.png)

### Extract
Pull data from a source (API— NYC taxi dataset)
### Transform
Data cleaning, transformation, and partitioning.
### Load
API to Mage, Mage to Postgres, GCS, BigQuery.

### Orchestration
A large part of data engineering is extracting, transforming, and loading data between sources. Orchestration is a process of dependency management, facilitated through automation. The data orchestrator manages scheduling, triggering, monitoring, and even resource allocation.
- Every workflow requires sequential steps. (A French press with cold water will only brew disappointment)
- Steps 🟰 tasks
- Workflows 🟰 DAGs (directed acyclic graphs) or Pipelines

![Alt text](documentation/image-1.png)

### Orchestrator handles
- Workflow management
- Automation
- Error handling 
- Recovery
- Monitoring, alerting
- Resource optimization
- Observability
- Debugging
- Compliance/Auditing

## 2.2.2 What is Mage?
An open-source pipeline tool for orchestrating transforming, and integrating data

![Alt text](documentation/image-3.png)

Hybrid environment
 - Use our GUI for interactive development (or don’t, I like VSCode)
- Use blocks as testable, reusable pieces of code.
Improved DevEx
- Code and test in parallel.
- Reduce your dependencies, switch tools less, be efficient.

Best code practices.
- In-line testing and debugging. Familiar, notebook-style format
- Fully-featured observability. Transformation in one place: dbt models, streaming, & more.
- DRY principles. No more DAGs with duplicate functions and weird imports DEaaS.

![Alt text](documentation/image-4.png)
### Projects
- A project forms the basis for all the work you can do in Mage— you can think of it like a GitHub repo. 
- It contains the code for all of your pipelines, blocks, and other assets.
- A Mage instance has one or more projects
### Pipelines
- A pipeline is a workflow that executes some data operation— maybe extracting, transforming, and loading data from an API. They’re also called DAGs on other platforms
- In Mage, pipelines can contain Blocks (written in SQL, Python, or R) and charts. 
- Each pipeline is represented by a YAML file in the “pipelines” folder of your project.
### Blocks
- A block is a file that can be executed independently or within a pipeline. 
- Together, blocks form Directed Acyclic Graphs (DAGs), which we call pipelines. 
- A block won’t start running in a pipeline until all its upstream dependencies are met.
- Blocks are reusable, atomic pieces of code that perform certain actions. 
- Changing one block will change it everywhere it’s used, but don’t worry, it’s easy to detach blocks to separate instances if necessary.
- Blocks can be used to perform a variety of actions, from simple data transformations to complex machine learning models.

![Alt text](documentation/image-5.png)

## Configuring Postgres
```yaml
version: '3'
services:
  magic:
    image: mageai/mageai:latest
    command: mage start ${PROJECT_NAME}
    env_file:
      - .env
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      USER_CODE_PATH: /home/src/${PROJECT_NAME}
      POSTGRES_DBNAME: ${POSTGRES_DBNAME}
      POSTGRES_SCHEMA: ${POSTGRES_SCHEMA}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_HOST: ${POSTGRES_HOST}
      POSTGRES_PORT: ${POSTGRES_PORT}
    ports:
      - 6789:6789
    volumes:
      - .:/home/src/
      - ~/Documents/secrets/personal-gcp.json:/home/src/personal-gcp.json
    restart: on-failure:5
  postgres:
    image: postgres:14
    restart: on-failure
    container_name: ${PROJECT_NAME}-postgres
    env_file:
      - .env
    environment:
      POSTGRES_DB: ${POSTGRES_DBNAME}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
```

Path where mage manages all connections "02-workflow-orchestration/mage-zoomcamp/magic-zoomcamp/io_config.yaml" for example we
define new connection profile:
```yaml
dev:
  # PostgresSQL https://docs.getdbt.com/reference/dbt-jinja-functions/env_var
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{ env_var('POSTGRES_DBNAME') }}"
  POSTGRES_SCHEMA: "{{ env_var('POSTGRES_SCHEMA') }}"
  POSTGRES_USER: "{{ env_var('POSTGRES_USER') }}"
  POSTGRES_PASSWORD: "{{ env_var('POSTGRES_PASSWORD') }}"
  POSTGRES_HOST: "{{ env_var('POSTGRES_HOST') }}"
  POSTGRES_PORT: "{{ env_var('POSTGRES_PORT') }}"
```

In mage GUI:
1. Create new pipeline
2. Create new SQL Loader
3. Define connection to Postgres
4. Define profile as dev
5. Define SQL query

## 2.2.3 ETL: API to Postgres
1. Create new pipeline
2. Create Python API loader
```python
@data_loader
def load_data_from_api(*args, **kwargs):
    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
    
    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                }

    # native date parsing 
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']

    return pd.read_csv(url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates)
```
3. Create Python transformer
```python
@transformer
def transform(data, *args, **kwargs):
    print(f"Preprocessing rows with zero passengers: { data[['passenger_count']].isin([0]).sum() }")

    return data[data['passenger_count'] > 0]

@test
def test_output(output, *args) -> None:
    assert output[ 'passenger_count'].isin([0]).sum() === 0, 'There are rides with zero passengers'
```
4. Create Postgres Python exporter
```python
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = 'ny_taxi'  # Specify the name of the schema to export data to
    table_name = 'yellow_cab_data'  # Specify the name of the table to export data to
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
        loader.export(
            df,
            schema_name,
            table_name,
            index=False,  # Specifies whether to include index in exported table
            if_exists='replace',  # Specify resolution policy if table name already exists
        )

```
5. Create SQL loader
```sql
SELECT * FROM ny_taxi.yellow_cab_data LIMIT 5;
```