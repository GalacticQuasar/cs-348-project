# Car Dealership Sales Dashboard

## Database Schema

Note: The database schema is defined in `django-project/app/models.py`.

### 1. Brand

| Column | Type | Constraints |
|---|---|---|
| id | AutoField (PK) | Primary Key |
| name | CharField(100) | Unique, Not Null |

Notes:
- Default ordering: `name`

### 2. CarModel

| Column | Type | Constraints |
|---|---|---|
| id | AutoField (PK) | Primary Key |
| brand_id | ForeignKey -> Brand(id) | Not Null, ON DELETE CASCADE |
| model_name | CharField(100) | Not Null |

Notes:
- Composite unique constraint: `(brand_id, model_name)`
- Default ordering: `brand__name`, `model_name`

### 3. SalesPerson

| Column | Type | Constraints |
|---|---|---|
| id | AutoField (PK) | Primary Key |
| first_name | CharField(100) | Not Null |
| last_name | CharField(100) | Not Null |

Notes:
- Default ordering: `last_name`, `first_name`

### 4. Customer

| Column | Type | Constraints |
|---|---|---|
| id | AutoField (PK) | Primary Key |
| first_name | CharField(100) | Not Null |
| last_name | CharField(100) | Not Null |
| email | EmailField | Unique, Not Null |

Notes:
- Default ordering: `last_name`, `first_name`

### 5. Sale (main table)

| Column | Type | Constraints |
|---|---|---|
| id | AutoField (PK) | Primary Key |
| salesperson_id | ForeignKey -> SalesPerson(id) | Not Null, ON DELETE PROTECT |
| customer_id | ForeignKey -> Customer(id) | Not Null, ON DELETE PROTECT |
| car_model_id | ForeignKey -> CarModel(id) | Not Null, ON DELETE PROTECT |
| sale_price | DecimalField(12, 2) | Not Null |
| date | DateField | Not Null |

Notes:
- Default ordering: `-date`, `-id`
- Indexes:
	- `date`
	- `(salesperson_id, date)`
	- `car_model_id`

### Relationship Summary

- One `Brand` has many `CarModel` records.
- One `CarModel` has many `Sale` records.
- One `SalesPerson` has many `Sale` records.
- One `Customer` has many `Sale` records.

