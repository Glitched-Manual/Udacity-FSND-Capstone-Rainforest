# Rainforest Store API
## Udacity Nanodegree Capstone Project
----
## Summary
----
\
Rainforest is a fullstack API. Is a web application is a store databank for storing orders, and user information. The application stores the data in a posgresql server.
The data contain with the aplication can be read and managed by using key endpoints.

## Deployment And Testing
----
\
The Rainforest may be accessed at: https://google.com
during local operation: http://localhost:5000
### Dependanies
\
`Python3`
\
Python 3.9 is the reccommend version of python for running the Rainforest API.
Python3 can be downloaded via the [official python site.](https://www.python.org/downloads/) 

\
`Postgresql`

The Rainforest API stores data within a postgresql database.
Postgresql can be downloaded via the [Postgresql site downloads](https://www.postgresql.org/download/).

Insturctions on how to setup the database can be found at the [Posgresql Tutorial site](https://www.postgresqltutorial.com)

`A Virtual Enviornment`

The project folder needs to be imported within a virtual enviornment.
Then the enviornment must be activated.
Info on how to create a virtual enviornment can be found [here](https://docs.python.org/3/tutorial/venv.html).
\

```bash
python3 -m venv {the_directory}
cd {the_directory}
cd Scripts

# run the appropiate activate script
```

`PIP Dependancies`

After the python3 virtual enviornment is activated. The needed Python3 must be installed. This can be done by navigating to the project root directory and running:

```bash
pip install -r requirements.txt
```

## Running the server

----

## API Reference

----

### Summary

The Rainforest API has two different roles:

- `Staff`

  - can perform most of the store functions from viewing products, managing user info, proccesing orders and the items(order_items) within the orders.

  - permissions: `get:users, post:users, delete:users, get:orders, post:orders, delete:orders, get:order_items, post:order_items, delete:order_items`.
- `Owner`
  - preforms all the actions as one with the `Staff` role. The owner may also add, edit and remove products from the system.
  
  - has premissions `post:products, delete:products, patch:products`. The `Owner` additionally has each of the permissions the `Staff` have.
\

## Error Handling

----
