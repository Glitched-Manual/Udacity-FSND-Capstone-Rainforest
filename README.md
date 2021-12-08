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
The Rainforest API may be accessed on heroku at: [heroku app link](https://rainforest-capstone.herokuapp.com/).

During local operation: [local link](http://localhost:5000)
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

To run the server after installing the requirements via pip, and have a database on postgresql called `rainforest_db`

edit the values for you local database credentials in `setup.sh`.

Then run:

```bash
setup.sh
flask run
```


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

Error are return in the json format below:

```bash
{
  "error": 404, 
  "message": "resource not found", 
  "success": false
}
```

The Rainforest returns the following response error code depending how the request fails:

- 400 - Bad Request

- 401 - Unauthorized

- 403 - Forbidden

- 404 - Not Found

- 405 - Method Not Allowed

- 422 - Unproccessible Entity

- 500 - Internal Server Error

## Endpoints

----

### Endpoint methods

```html
Get: get products, get users, get orders, get order_items

Post: create product, create user, create order, create order_item

Delete: delete product, delete user, delete order, delete order_item

Patch: patch product
    
```

## Get

----

Get `/products`

sample request:

```bash

{
  "products": [
    {
      "description": "a Rainforest exclusive t-shirt",
      "id": 1,
      "name": "Rainforset t-shirt - black/green",
      "price": 10.99
    },
    {
      "description": "a chocolate bar",
      "id": 2,
      "name": "snickers bar",
      "price": 2.99
    },
    {
      "description": "a chocolate bar",
      "id": 3,
      "name": "snickers bar",
      "price": 2.99
    }
}

```

sample request:

```bash

```

sample request:

```bash

```

sample request:

```bash

```

sample request:

```bash

```

sample request:

```bash

```

sample request:


```bash

```

sample request:

```bash
sample request:

```

sample request:

```bash

```

sample request:

```bash

```

sample request:

```bash

```

sample request:

```bash

```

sample request:

```bash

```
