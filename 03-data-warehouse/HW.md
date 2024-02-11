## Homework
```sql
CREATE OR REPLACE EXTERNAL TABLE `terraform-demo-412013.ny_taxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://mage-zoomcamp-alex-pogadaev-3/nyc-tl-data/trip data/green_tripdata_2022-*.parquet']
);

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE terraform-demo-412013.ny_taxi.green_tripdata_non_partitoned AS
SELECT * FROM terraform-demo-412013.ny_taxi.external_green_tripdata;

-- Q1: What is count of records for the 2022 Green Taxi Data?
-- ANSWER: 840402
SELECT COUNT(1) FROM terraform-demo-412013.ny_taxi.external_green_tripdata; --840402
SELECT COUNT(1) FROM terraform-demo-412013.ny_taxi.green_tripdata_non_partitoned; --840402

-- Q2: Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.
-- What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
-- ANSWER: 0 MB for the External Table and 6.41MB for the Materialized Table
SELECT DISTINCT PULocationID FROM terraform-demo-412013.ny_taxi.external_green_tripdata; -- 0MB
SELECT DISTINCT PULocationID FROM terraform-demo-412013.ny_taxi.green_tripdata_non_partitoned; -- 6.41BM

-- Q3: How many records have a fare_amount of 0?
-- ANSWER: 1622
SELECT COUNT(fare_amount) FROM terraform-demo-412013.ny_taxi.external_green_tripdata WHERE fare_amount = 0; -- 1622 
SELECT COUNT(fare_amount) FROM terraform-demo-412013.ny_taxi.green_tripdata_non_partitoned WHERE fare_amount = 0; -- 1622

-- Q4: What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy) "Clustering improves filter queries but we filter only on single column lpep_pickup_datetime. So we go with partitioning on lpep_pickup_datetime by date and clustering of PUlocationID."
-- ANSWER: Partition by lpep_pickup_datetime Cluster on PUlocationID
CREATE OR REPLACE TABLE terraform-demo-412013.ny_taxi.green_tripdata_partitoned_clustered
PARTITION BY DATE(lpep_pickup_datetime)
CLUSTER BY PULocationID AS
SELECT * FROM terraform-demo-412013.ny_taxi.external_green_tripdata;

-- Q5: Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
-- Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values?
-- ANSWER: 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table
SELECT DISTINCT
PULocationID
FROM terraform-demo-412013.ny_taxi.green_tripdata_non_partitoned
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'; -- 12.82MB
SELECT DISTINCT
PULocationID
FROM terraform-demo-412013.ny_taxi.green_tripdata_partitoned_clustered
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'; -- 1.12MB

-- Q6: Where is the data stored in the External Table you created?
-- ANSWER: GCP Bucket

-- Q7: It is best practice in Big Query to always cluster your data:
-- ANSWER: True

-- Q8: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
-- ANSWER: 0 B. In that particular case query is getting answered from metadata tables but there is other optimization that provides efficiency: BQ separates storage from compute (on different hardware) and connect them with highly accessible Jupiter network. Colossus (storage) is column-oriented provide better aggreagtion. Dremel divides query to subqueries and propagate it to leaf nodes.
SELECT COUNT(*) FROM terraform-demo-412013.ny_taxi.green_tripdata_non_partitoned;
```