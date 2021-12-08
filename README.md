# Rainforest Store API

## Udacity Nanodegree Capstone Project

----

## Summary

----
\
Rainforest is a fullstack API. The Rainforest API is a web application is a simulated store system for recording orders, and user information. The application stores the data in a posgresql server.
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

To run the server after installing the requirements via pip, and have a database on postgresql called `rainforest_db`.

After the postgresql server is setup, edit the values for you local database credentials in `setup.sh`.

Then run:

```bash
setup.sh
flask run
```

## API Reference

----

### API Summary

The Rainforest API has two different roles:

- `Staff`

  - Can perform most of the store functions from viewing products, managing user info, proccesing orders and the items(order_items) within the orders.

  - permissions: `get:users, post:users, delete:users, get:orders, post:orders, delete:orders, get:order_items, post:order_items, delete:order_items`.
- `Owner`
  - Preforms all the actions as a user with the `Staff` role. The owner may also add, edit and remove products from the system.
  
  - Has premissions `post:products, delete:products, patch:products`. The `Owner` additionally has each of the permissions the `Staff` have.
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
Get '/'

- Returns a friendly welcome  message

sample request:

```bash
curl https://rainforest-capstone.herokuapp.com/
```

Output:

```bash
Welcome to Rainforest! :>
```

- Returns a paginated list of products.
- does not require permissions.

Get `/products`

sample request:

```bash
curl https://rainforest-capstone.herokuapp.com/"products"
```

Output:

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

Get `/products/id`

- Returns the product that has the passed id.
- does not require permissions.

sample request:

```bash
curl https://rainforest-capstone.herokuapp.com/"products/1"
```

Output:

```bash
{
  "product": {
    "description": "a Rainforest exclusive t-shirt",
    "id": 1,
    "name": "Rainforset t-shirt - black/green",
    "price": 10.99
  },
  "success": true
}

```

Get `users`

- Returns a paginated list of users.
- Requires the `get:users` permission.

sample request:

```bash
curl -H "Authorization: Bearer $STAFF_TOKEN" -X GET https://rainforest-capstone.herokuapp.com/"users"
```

Output:

```bash
{
 "success": true,
  "total_users": 56,
  "users": [
    {
      "id": 1,
      "name": "slippery sam"
    },
    {
      "id": 2,
      "name": "chris condo"
    }
  ]
}
```

Get `/users/id`

sample request:

- Returns the user that has the passed id.
- Requires the `get:users` permission.

```bash
curl -H "Authorization: Bearer $STAFF_TOKEN" -X GET https://rainforest-capstone.herokuapp.com/"users/1"
```

Output:

```bash
{
  "success": true,
  "user": {
    "id": 1,
    "name": "slippery sam"
  }
}
```

Get `orders`

- Returns a paginated list of orders.
- Requires the `get:orders` permission.

sample request:

```bash
curl -H "Authorization: Bearer $STAFF_TOKEN" -X GET https://rainforest-capstone.herokuapp.com/"orders"
```

Output:

```bash

{
  "orders": [
    {
      "id": 1,
      "user_id": 1
    },
    {
      "id": 2,
      "user_id": 2
    }
 ]
}

```

Get `/orders/id`

- Returns the user that has the passed id.
- Requires the `get:orders` permission.

sample request:

```bash
curl -H "Authorization: Bearer $STAFF_TOKEN" -X GET https://rainforest-capstone.herokuapp.com/"orders/1"
```

Output:

```bash
{
  "order": {
    "id": 1,
    "user_id": 1
  },
  "success": true
}
```

Get `/order_items`

- Returns a paginated list of order items.
- Requires the `get:order_items` permission.

sample request:

```bash
curl -H "Authorization: Bearer $STAFF_TOKEN" -X GET https://rainforest-capstone.herokuapp.com/"order_items"
```

Output:

```bash
{
  "order_items": [
    {
      "id": 1,
      "order_id": 1,
      "product_id": 1,
      "product_quantity": 2
    },
    {
      "id": 2,
      "order_id": 1,
      "product_id": 1,
      "product_quantity": 2
    }
 ]
 "success": true,
 "total_order_items": 55
}
```

Get `/order_items/id`

- Returns the order item that has the passed id.
- Requires the `get:order_items` permission.

sample request:

```bash
curl -H "Authorization: Bearer $STAFF_TOKEN" -X GET https://rainforest-capstone.herokuapp.com/"order_items/1"
```

Output:

```bash
{
  "order_item": {
    "id": 1,
    "order_id": 1,
    "product_id": 1,
    "product_quantity": 2
  },
  "success": true
}

```

## POST Requests

----

POST `/products`

- Creates a new product
- Requires `name`(string), `description`(string), price(float) to be passed as json for the request.
- Requires the `post:products` permission. Only a user with the`owner` role can use this endpoint

sample request:

```bash
curl -d '{  "name":"rbg dice",  "description":"programmable gaming dice set",  "price":15}' -H "Content-Type: application/json" -H "Authorization: Bearer $OWNER_TOKEN" -X POST https://rainforest-capstone.herokuapp.com/"products"
```

Output:

```bash
{
  "created": 101,
  "product": {
    "description": "programmable gaming dice set",
    "id": 101,
    "name": "rbg dice",
    "price": 15.0
  },
  "success": true,
  "total_products": 84
}

```

POST `/users`

- Creates a new user.
- Requires `name`(string) to be passed as json for the request.
- Requires the `post:users` permission.

sample request:

```bash
curl -d '{  "name":"cool guy"}' -H "Content-Type: application/json" -H "Authorization: Bearer $STAFF_TOKEN" -X POST https://rainforest-capstone.herokuapp.com/"users"
```

Output:

```bash
{
  "created": 80,
  "success": true,
  "user": {
    "id": 80,
    "name": "cool guy"
  }
}
```

POST `/orders`

- Creates a new order.
- Requires `user_id`(integer) to be passed as json for the request.
- The `user_id` must match the id of an existing user.
- Requires the `post:orders` permission.

sample request:

```bash
curl -d '{  "user_id":2 }' -H "Content-Type: application/json" -H "Authorization: Bearer $STAFF_TOKEN" -X POST https://rainforest-capstone.herokuapp.com/"orders"
```

Output:

```bash
{
  "created": 58,
  "order": {
    "id": 58,
    "user_id": 2
  },
  "success": true
}
```

POST `/order_items`

- Creates a new order item.
- Requires `user_id`(integer) to be passed as json for the request.
- The `order_id` must match the id of an existing order.
- The `product_id` must match the id of an existing product.
- Requires the `post:order_items` permission.

sample request:

```bash
curl -d '{  "order_id":7, "product_id":1, "product_quantity":20 }' -H "Content-Type: application/json" -H "Authorization: Bearer $STAFF_TOKEN" -X POST https://rainforest-capstone.herokuapp.com/"order_items"
```

Output:

```bash
{
  "created": 58,
  "order_item": {
    "id": 58,
    "order_id": 7,
    "product_id": 1,
    "product_quantity": 20
  },
  "success": true
}
```

## Delete Methods

Delete `/products/id`

- Deletes the `product` that has the passed `id` as the value for it id atrribute.

- Requires the `delete:products` permission. Only a user with the`owner` role can use this end point

sample request:

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer $OWNER_TOKEN" -X DELETE $root"products/102"
```

Output:

```bash
{
  "deleted": 102,
  "success": true,
  "total_products": 101
}
```

Delete `/users/id`

- Deletes the `user` that has the passed `id` as the value for it id atrribute.

- Requires the `delete:users` permission.

sample request:

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer $STAFF_TOKEN" -X DELETE $root"users/12"
```

Output:

```bash
{
  "deleted": 12,
  "success": true
}
```

Delete `/orders/id`

- Deletes the `order` that has the passed `id` as the value for it id atrribute.

- Requires the `delete:orders` permission.

sample request:

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer $STAFF_TOKEN" -X DELETE $root"orders/57"
```

Output:

```bash
{
  "deleted": 57,
  "success": true
}
```

Delete `/order_items/id`

Delete `/users/id`

- Deletes the `order item` that has the passed `id` as the value for it id atrribute.

- Requires the `delete:order_items` permission.

sample request:

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer $STAFF_TOKEN" -X DELETE $root"order_items/55"
```

Output:

```bash
{
  "deleted": 55,
  "success": true
}
```

## Patch Methods

----

Patch `/products/id`

- Updates the `product` that has the passed id as the value for its `id` attribute.

- Requires the `patch:products` permission. Only a user with the`owner` role can use this endpoint

sample request:

```bash
curl -d '{  "name":"new video game",  "description":"the most EPIC AAA of the year!!!!!!!!!",  "price":90.95}' -H "Content-Type: application/json" -H "Authorization: Bearer $OWNER_TOKEN" -X PATCH $root"products/99"
```

Output:

```bash
{
  "patched": 99,
  "product_description": "the most EPIC AAA of the year!!!!!!!!!",
  "product_name": "new video game",
  "product_price": 90.95,
  "success": true
}
```
