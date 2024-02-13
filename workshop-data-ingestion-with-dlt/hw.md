#### Question 1: What is the sum of the outputs of the generator for limit = 5?
#### ANSWER: 8.382332347441762
```python
def square_root_generator(limit):
    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Example usage:
limit = 5
generator = square_root_generator(limit)
sum = 0

for sqrt_value in generator:
    sum += sqrt_value

print(sum)
```

#### Question 2: What is the 13th number yielded
#### ANSWER: 3.605551275463989
```python
def square_root_generator(limit):
    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Example usage:
limit = 13
generator = square_root_generator(limit)
values = []

for sqrt_value in generator:
    values.append(sqrt_value)

print(values[-1])
```

#### Question 3: Append the 2 generators. After correctly appending the data, calculate the sum of all ages of people.
#### ANSWER: 353
```python
def people_1():
    for i in range(1, 6):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}


def people_2():
    for i in range(3, 9):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}

result = []
total_age = 0
for person in people_1():
    result.append(person)

for person in people_2():
    result.append(person)

for person in result:
  total_age += person['Age']

print(total_age)
```

#### Question 4: Merge the 2 generators using the ID column. Calculate the sum of ages of all the people loaded as described above.
#### ANSWER: 266
```python
#Install the dependencies
%%capture
!pip install dlt[duckdb]
```
```python
def people_1():
    for i in range(1, 6):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"}
```
```python
def people_2():
    for i in range(3, 9):
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"}
```
```python
import dlt

generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='people_info')
info = generators_pipeline.run(people_1(), table_name="people", write_disposition="replace", primary_key='ID')

print(info)
```
```python
import duckdb

conn = duckdb.connect(f"{generators_pipeline.pipeline_name}.duckdb")

# let's see the tables
conn.sql(f"SET search_path = '{generators_pipeline.dataset_name}'")
print('Loaded tables: ')
display(conn.sql("show tables"))
```
```python
print("\n\n\n people table below:")

people_1 = conn.sql("SELECT * FROM people").df()
display(people_1)
```
```python
generators_pipeline = dlt.pipeline(destination='duckdb', dataset_name='people_info')
info = generators_pipeline.run(people_2(), table_name="people", write_disposition="merge")

print(info)
```
```python
print("\n\n\n people table below:")

people_result = conn.sql("SELECT * FROM people ORDER BY id").df()
display(people_result)
```
```python
people_result['age'].sum()
```