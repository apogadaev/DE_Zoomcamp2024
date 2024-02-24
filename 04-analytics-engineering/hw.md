```sql
CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.external_fhv_tripdata_csv`
OPTIONS (
  format = 'CSV',
  uris = ['gs://mage-zoomcamp-../fhv_csv/*.csv']
);

CREATE OR REPLACE TABLE trips_data_all.fhv_tripdata AS
SELECT
dispatching_base_num AS dispatching_baseid,
pickup_datetime AS pickup_datetime,
dropOff_datetime AS dropoff_datetime,
CAST(PUlocationID AS INT) AS pickup_locid,
CAST(DOlocationID AS INT) AS dropoff_locid,
Affiliated_base_number AS affiliated_baseId
FROM trips_data_all.external_fhv_tripdata_csv;
```


#### Question 1:

What happens when we execute dbt build --vars '{'is_test_run':'true'}' You'll need to have completed the "Build the first dbt models" video.

It applies a limit 100 only to our staging models

#### Question 2:

What is the code that our CI job will run? Where is this code coming from?

The code from the development branch we are requesting to merge to main

##### Question 3 (2 points)

I don't have correct answers for this question. Please, let me know if you have any suggestions. Mine are: 18897249

i'm choosing 22998722

##### Question 4 (2 points):
same as 3

i'm choosing FHV
