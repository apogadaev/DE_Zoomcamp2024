### Question 1:

Install Spark and PySpark

Install Spark
Run PySpark
Create a local spark session
Execute spark.version.
What's the output?

answer: 3.5.1

### Question 2:

FHV October 2019

Read the October 2019 FHV into a Spark Dataframe with a schema as we did in the lessons.

Repartition the Dataframe to 6 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

answer: 6

### Question 3:

Count records

How many taxi trips were there on the 15th of October?

Consider only trips that started on the 15th of October.

answer: 2019-10-15 00:00:00|   62610|

### Question 4:

Longest trip for each day

What is the length of the longest trip in the dataset in hours?

answer: 631152

### Question 5:

User Interface

Spark’s User Interface which shows the application's dashboard runs on which local port?

answer: 4040

### Question 6:

Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark
Zone Data

Using the zone lookup data and the FHV October 2019 data, what is the name of the LEAST frequent pickup location Zone?

answer: Jamaica Bay