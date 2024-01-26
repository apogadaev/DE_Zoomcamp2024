### Question 1. Knowing docker tags
```
--rm
```

### Question 2. Understanding docker first run
```
0.42.0
```

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"
docker build -t green_taxi_ingest_data:v001 .
docker run -it --network=hw_default green_taxi_ingest_data:v001 --user=root --password=root --host=pgdatabase --port=5432 --db=ny_taxi --table_name=green_taxi_trips --url=${URL}
```
swap script in docker file
```bash
URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
docker build -t taxi_zones_ingest_data:v001 .
docker run -it --network=hw_default taxi_zones_ingest_data:v001 --user=root --password=root --host=pgdatabase --port=5432 --db=ny_taxi --table_name=taxi_zones --url=${URL}
```

### Question 3. Count records
15612
```sql
SELECT COUNT(*) FROM green_taxi_trips
WHERE DATE(lpep_dropoff_datetime) = '2019-09-18' AND DATE(lpep_pickup_datetime) = '2019-09-18';
```

### Question 4. Largest trip for each day
2019-09-26
```sql
SELECT
CAST(lpep_pickup_datetime AS DATE),
MAX(trip_distance) AS distance
FROM green_taxi_trips
GROUP BY 1
ORDER BY distance DESC;
```
### Question 5. Three biggest pick up Boroughs
"Brooklyn" "Manhattan" "Queens"
```sql
SELECT
	CAST(lpep_pickup_datetime AS DATE),
	zone_pick_up."Borough",
	SUM(total_amount) AS sum_total_amount
FROM green_taxi_trips
LEFT JOIN taxi_zones zone_pick_up ON green_taxi_trips."PULocationID" = zone_pick_up."LocationID"
WHERE
	DATE(lpep_pickup_datetime) = '2019-09-18'
	AND zone_pick_up."Borough" != 'Unknown'
GROUP BY 1, 2
ORDER BY sum_total_amount DESC;
```

### Question 6. Largest tip
JFK Airport
```sql
SELECT
tip_amount,
zone_drop_off."Zone"
FROM green_taxi_trips
INNER JOIN taxi_zones zone_pick_up ON green_taxi_trips."PULocationID" = zone_pick_up."LocationID"
INNER JOIN taxi_zones zone_drop_off ON green_taxi_trips."DOLocationID" = zone_drop_off."LocationID"
WHERE lpep_pickup_datetime BETWEEN '2019-09-01 00:00:00' AND '2019-09-30 23:59:59'
AND zone_pick_up."Zone" = 'Astoria'
-- AND passenger_count > 1
ORDER BY tip_amount DESC
LIMIT 100;
```

### Question 7
```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.demo_dataset will be created
  + resource "google_bigquery_dataset" "demo_dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "EUROPE-WEST3"
      + max_time_travel_hours      = (known after apply)
      + project                    = "terraform-demo-412013"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "EUROPE-WEST3"
      + name                        = "terraform-demo-412013-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.demo_dataset: Creating...
google_storage_bucket.demo-bucket: Creating...
google_bigquery_dataset.demo_dataset: Creation complete after 1s [id=projects/terraform-demo-412013/datasets/demo_dataset]
google_storage_bucket.demo-bucket: Creation complete after 1s [id=terraform-demo-412013-terra-bucket]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```