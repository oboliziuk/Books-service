"# Books-service"

This project is an API-based library management system for tracking books, users, and borrowings. 
It replaces the manual paper system with a digital solution to simplify administration and improve user experience.

## Installation

Python3 must be already installed

shell
git clone https://github.com/oboliziuk/Books-service.git
cd Books_service
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver #starts Django Server

## Environment Variables

To run this project, create a `.env` file in the root directory.  
You can use the provided `simple.env` as a template:

```bash
cp simple.env .env
```

##Features

* Full CRUD for books, users, and borrowings with proper permission handling
* JWT authentication with custom Authorize header support
* Automatic book inventory management on borrow and return
* Borrowing filtering by user and active status
* 60%+ test coverage of custom logic

## Documentation API
(API_DOCUMENTATION.md)

##Demo 
Website Interface: demo.png
