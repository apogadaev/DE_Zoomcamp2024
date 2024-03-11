### Question 1

Create a materialized view to compute the average, min and max trip time between each taxi zone.

Note that we consider the do not consider a->b and b->a as the same trip pair. So as an example, you would consider the following trip pairs as different pairs:

Yorkville East -> Steinway
Steinway -> Yorkville East
From this MV, find the pair of taxi zones with the highest average trip time. You may need to use the dynamic filter pattern for this.

Bonus (no marks): Create an MV which can identify anomalies in the data. For example, if the average trip time between two zones is 1 minute, but the max trip time is 10 minutes and 20 minutes respectively.

Options:

- **Yorkville East, Steinway** - answer
- Murray Hill, Midwood
- East Flatbush/Farragut, East Harlem North
- Midtown Center, University Heights/Morris Heights

p.s. The trip time between taxi zones does not take symmetricity into account, i.e. A -> B and B -> A are considered different trips. This applies to subsequent questions as well.

 vendorid | tpep_pickup_datetime | tpep_dropoff_datetime | passenger_count | trip_distance | ratecodeid | store_and_fwd_flag | pulocationid | dolocationid | payment_type | fare_amount | extra | mta_tax | tip_amount | tolls_amount | improvement_surcharge | total_amount | congestion_surcharge | airport_fee 
 ```sql
 SELECT 
    taxi_zone.Zone as pickup_zone,
    taxi_zone_1.Zone as dropoff_zone,
    AVG(tpep_dropoff_datetime - tpep_pickup_datetime) as avg_trip_time, 
    MIN(tpep_dropoff_datetime - tpep_pickup_datetime) as min_trip_time, 
    MAX(tpep_dropoff_datetime - tpep_pickup_datetime ) as max_trip_time
FROM trip_data
JOIN taxi_zone ON trip_data.pulocationid = taxi_zone.location_id
JOIN taxi_zone as taxi_zone_1 ON trip_data.dolocationid = taxi_zone_1.location_id
GROUP BY pickup_zone, dropoff_zone;

CREATE MATERIALIZED VIEW trip_time_mv AS
SELECT 
    taxi_zone.Zone as pickup_zone,
    taxi_zone_1.Zone as dropoff_zone,
    AVG(tpep_dropoff_datetime - tpep_pickup_datetime) as avg_trip_time, 
    MIN(tpep_dropoff_datetime - tpep_pickup_datetime) as min_trip_time, 
    MAX(tpep_dropoff_datetime - tpep_pickup_datetime ) as max_trip_time
FROM trip_data
JOIN taxi_zone ON trip_data.pulocationid = taxi_zone.location_id
JOIN taxi_zone as taxi_zone_1 ON trip_data.dolocationid = taxi_zone_1.location_id
GROUP BY pickup_zone, dropoff_zone;
```
From this MV, find the pair of taxi zones with the highest average trip time. You may need to use the dynamic filter pattern for this.
```sql
SELECT pickup_zone, dropoff_zone, avg_trip_time
FROM trip_time_mv
ORDER BY avg_trip_time DESC
LIMIT 1;
-- Yorkville East | Steinway     | 23:59:33
```
Bonus (no marks): Create an MV which can identify anomalies in the data. For example, if the average trip time between two zones is 1 minute, but the max trip time is 10 minutes and 20 minutes respectively.
```sql
CREATE MATERIALIZED VIEW trip_time_anomaly_mv AS
SELECT 
    taxi_zone.Zone as pickup_zone,
    taxi_zone_1.Zone as dropoff_zone,
    AVG(tpep_dropoff_datetime - tpep_pickup_datetime) as avg_trip_time, 
    MIN(tpep_dropoff_datetime - tpep_pickup_datetime) as min_trip_time, 
    MAX(tpep_dropoff_datetime - tpep_pickup_datetime) as max_trip_time
FROM trip_data
JOIN taxi_zone ON trip_data.pulocationid = taxi_zone.location_id
JOIN taxi_zone as taxi_zone_1 ON trip_data.dolocationid = taxi_zone_1.location_id
GROUP BY pickup_zone, dropoff_zone
HAVING (AVG(tpep_dropoff_datetime - tpep_pickup_datetime) < interval '1 minute') AND (MAX(tpep_dropoff_datetime - tpep_pickup_datetime) > interval '10 minute');
```
###Question 2

Recreate the MV(s) in question 1, to also find the number of trips for the pair of taxi zones with the highest average trip time.

Options:

- 5
- 3
- 10
- **1** - answer

```sql
CREATE MATERIALIZED VIEW trip_stat_mv AS
SELECT 
    taxi_zone.Zone as pickup_zone,
    taxi_zone_1.Zone as dropoff_zone,
    COUNT(1) as trip_count,
    AVG(tpep_dropoff_datetime - tpep_pickup_datetime) as avg_trip_time, 
    MIN(tpep_dropoff_datetime - tpep_pickup_datetime) as min_trip_time, 
    MAX(tpep_dropoff_datetime - tpep_pickup_datetime ) as max_trip_time
FROM trip_data
JOIN taxi_zone ON trip_data.pulocationid = taxi_zone.location_id
JOIN taxi_zone as taxi_zone_1 ON trip_data.dolocationid = taxi_zone_1.location_id
GROUP BY pickup_zone, dropoff_zone;
```

### Question 3

From the latest pickup time to 17 hours before, what are the top 3 busiest zones in terms of number of pickups? For example if the latest pickup time is 2020-01-01 17:00:00, then the query should return the top 3 busiest zones from 2020-01-01 00:00:00 to 2020-01-01 17:00:00.


Options:

- Clinton East, Upper East Side North, Penn Station
- **LaGuardia Airport, Lincoln Square East, JFK Airport** answer
- Midtown Center, Upper East Side South, Upper East Side North
- LaGuardia Airport, Midtown Center, Upper East Side North

```sql
SELECT taxi_zone.Zone as pickup_zone, COUNT(1) as pickup_count
FROM trip_data
JOIN taxi_zone ON trip_data.pulocationid = taxi_zone.location_id
WHERE tpep_pickup_datetime > (SELECT MAX(tpep_pickup_datetime) - interval '17 hours' FROM trip_data)
GROUP BY pickup_zone
ORDER BY pickup_count DESC
LIMIT 3;
```