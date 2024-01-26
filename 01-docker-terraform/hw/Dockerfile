FROM python:3.9

RUN apt-get install \ 
            wget \
            gzip \
    ;

RUN pip install pandas psycopg2 sqlalchemy

WORKDIR /app
COPY ingest_zones.py ingest_zones.py

ENTRYPOINT [ "python", "ingest_zones.py" ]