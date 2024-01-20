# ATM Service

## General Technical Details
- Development is done using Fast API framework
- Python version 3.9
- Database PostgreSQL (already predefined with  necessary table and data)

## Modules / Directories
- app - contains main functionality of ATM
- db - db instance creation
- utils - functions for general usage
- constants - constant values for service activation


## Using Docker
Build docker image (from venv environment)

> docker-compose -f docker-compose.yml up --build -d

Run tests: 

> docker-compose exec web pytest .

Service will be initialized with access through following address 'http://localhost:8002'
Swagger with docs: 

> http://localhost:8002/docs

## Usage

### Withdrawal request
~~~
curl -L -g -X POST 'http://127.0.0.1:8002/atm/withdrawal' -H 'Content-Type: application/json' --data-raw '{ "amount":"25.00"}'
~~~
### Refill request
~~~
curl -L -g -X POST 'http://127.0.0.1:8002/atm/refill' -H 'Content-Type: application/json' --data-raw '{
"money":{ "0.1": 5, "5": 20, "20": 15, "100": 30 }}'
~~~
### Get inventory
This was done to allow to verify investment in db
~~~
curl -L -g -X GET 'http://127.0.0.1:8002/atm/inventory' 
~~~

