import os

for month in range(1, 13):
    url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-{month}.csv.gz'
    # download_csv
    gzip_name = f'yellow_tripdata_2019-{month}.csv.gz'
    csv_name = f'yellow_tripdata_2019-{month}.csv.gz'
    os.system(f"wget {url} -O {gzip_name}; gzip -d {gzip_name}")