import argparse
import os
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    print(params)

    # download_csv
    gzip_name = "output.csv.gz"
    csv_name = "output.csv"
    os.system(f"wget {url} -O {gzip_name}; gzip -d {gzip_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    print(len(df))
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
    print('out')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        print('in loop')
        t_start = time()
        df = next(df_iter)
        print(len(df))
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists="append")
        t_end = time()

        print("Imported another chunk, took %.3f second" % (t_end - t_start))

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Ingest csv data to pgsql.')

    parser.add_argument('--user', help='user name for pgsql')
    parser.add_argument('--password', help='password for pgsql')
    parser.add_argument('--host', help='host for pgsql')
    parser.add_argument('--port', help='port for pgsql host')
    parser.add_argument('--db', help='database name for pgsql')
    parser.add_argument('--table_name', help='name of the table for results')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)
