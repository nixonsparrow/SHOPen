# SHOPen - e-commerce project

## Tech stack:
Django, DRF, SQLite3


## How to run

To start the project simply type:

`python manage.py migrate`
`python manage.py runserver`

Then create superuser to give Users proper roles to use an application:<br>
`python manage.py createsuperuser`

Enter endpoint: <br>
`/admin/auth/user/`

To make a User a Client or a Vendor add him to the group `Client` or `Vendor` respectively.<br>
You can add one User to both groups.

## Views

### Add Category
###### Authorisation needed, role Vendor needed
Endpoint: `POST /api/products/`

Data needed to create a new category:<br>
`"name"`

Example JSON data to add to request:<br>
```json
{
  "name": "cats"
}
```
The easiest way to add a product is via the Django REST framework view.


### Add product
###### Authorisation needed, role Vendor needed
Endpoint: `POST /api/products/`

Data needed to create a new product:<br>
`"name", "price", "category", "image"`

Example JSON data to add to request:<br>
```json
{
  "name": "Fluffy",
  "price": 2.00,
  "category": 1,
  "image": <image data>,
}
```
The easiest way to add a product is via the Django REST framework view.<br>
Category must much the id of Category object in database.

### View all products
###### No authorisation needed
Endpoint: `GET /api/products/`

For extra options add one or more parameters to your GET query:<br>
- `name=<x>` - filter by product's name with `<x>`<br>
- `category=<x>` - filter by product's category's name with `<x>`<br>
- `price=<x>` - filter by product's price with `<x>`<br>
- `description=<x>` - filter by product's description with `<x>`<br>
- `sort=<name/description/price>` - sort by product's attribute (add `-` at the beginning of the attribute to reverse order)<br>
- `page_size=<x>` - paginate by `<x>` products (default value is `10`)
- `page=<x>` - go to page `<x>` of pagination.<br>

Example usages (one or multiple parameters):<br>
- `/api/products/?name=fluffy`
- `/api/products/?name=fluffy&category=cats`
- `/api/products/?name=Chopin&category=musicians`
- `/api/products/?name=fluffy&page=3`
- `/api/products/?page_size=30&page=2`
- `/api/products/?sort=-name`
- `/api/products/?sort=-name&price=2`

### View one product
###### No authorisation needed

Endpoint: `GET /api/products/<x>`

Replace `<x>` with `id` of demanded product.

### Place Order
###### Authorisation needed, role Client needed

Endpoint: `POST /api/orders/`

Data needed to create a new order:<br>
`"address", "cart"`

Example JSON data to add to request:<br>
```json
{
  "address": "Lovely 13 street, HearthVille",
  "cart": [
    {"product": 1, "quantity": 1, "price": 1.00},
    {"product": 2, "quantity": 2, "price": 3.00}
  ]
}
```
The easiest way to add a product is via the Django REST framework view.<br>
`"product"` must much the id of Product object in database.


### See stats of most popular products
###### Authorisation needed, role Vendor needed

Endpoint: `GET /api/stats/`

For extra options add one or more parameters to your GET query:
- `limit=<x>` - output is limited to `<x>` products
- `from=<DD-MM-YYYY>` - input takes items bought after given date (inclusively)
- `to=<DD-MM-YYYY>` - input takes items bought before given date (inclusively)

Example usages (one or multiple parameters):<br>
- `/api/products/?limit=10`
- `/api/products/?limit=100&from=15-11-2023`
- `/api/products/?from=15-04-2023&to=20-11-2023`
