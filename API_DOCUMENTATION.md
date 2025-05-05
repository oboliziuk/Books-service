# Books Service

Purpose: Managing the quantity and details of books.

Permissions:
* Admins: Full access (CRUD)
* All users: Can list and view books

### Endpoints:


| Method     | Endpoint      | Description                                |
|------------|---------------|--------------------------------------------|
| POST	      | books         | 	Add a new book (admin only)               |
| GET	       | books         | 	Get a list of all books                   |
| GET	       | books/<id>/   | 	Get detail of a specific book             |
| PUT/PATCH	 | /books/<id>/  | Update book info or inventory (admin only) |
| DELETE	    | /books/<id>/	 | Delete a book (admin only)                 |

## Users Service
Purpose: User registration and authentication with JWT.

### Endpoints:


| Method     | Endpoint               | Description                   |
|------------|------------------------|-------------------------------|
| POST	      | /users/	               | Register a new user           |
| POST	      | /users/token/	         | Obtain JWT tokens             |
| POST	      | /users/token/refresh/	 | Refresh access token          |
| GET	       | /users/me/	            | Get current user's profile    |
| PUT/PATCH	 | /users/me/	            | Update current user's profile |

## Borrowings Service
Purpose: Track borrowings and manage inventory accordingly.
Permissions:
* Authenticated users: Can borrow and return
* Admins: Can view all borrowings, filter by user

### Endpoints:


| Method | Endpoint                          | Description                                    |
|--------|-----------------------------------|------------------------------------------------|
| POST	  | /borrowings/	                     | Borrow a book (decrease inventory by 1)        |
| GET	   | /borrowings/?user_id=&is_active=	 | Filter borrowings by user and active status    |
| GET	   | /borrowings/<id>/	                | Get detail about a borrowing                   |
| POST	  | /borrowings/<id>/return/          | 	Return a book (set return date, +1 inventory) |
