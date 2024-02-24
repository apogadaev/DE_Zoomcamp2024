{{
    config(
        materialized='view'
    )
}}

with tripdata as 
(
  select *,
    row_number() over(partition by dispatching_baseid, affiliated_baseId, pickup_datetime) as rn
  from {{ source('staging','fhv_tripdata') }}
  where dispatching_baseid is not null 
  and affiliated_baseId is not null
  and pickup_locid is not null
  and dropoff_locid is not null
  and EXTRACT(YEAR FROM pickup_datetime) = 2019
)
select
    {{ dbt_utils.generate_surrogate_key(['dispatching_baseid', 'affiliated_baseId', 'pickup_datetime']) }} as tripid,
    dispatching_baseid,
    affiliated_baseId as affiliated_baseid,
    {{ dbt.safe_cast("pickup_locid", api.Column.translate_type("integer")) }} as pickup_locationid,
    {{ dbt.safe_cast("dropoff_locid", api.Column.translate_type("integer")) }} as dropoff_locationid,

        -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
from tripdata
where rn = 1


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}