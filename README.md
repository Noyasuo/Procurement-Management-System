# Procurment Management System

## About This Project
A comprehensive mobile procurement management system that digitizes the entire procurement workflow. Features include vendor management, purchase order creation, approval workflows, inventory tracking, budget monitoring, and reporting analytics. Designed for seamless mobile experience with offline capabilities.

## Platforms
- **User:** Mobile App
- **Admin:** Web and Desktop

## Tech Stack
- **Backend:** Python, Django
- **API:** Django REST Framework
- **Authentication:** SimpleJWT (JSON Web Tokens)
- **Documentation:** DRF Spectacular (OpenAPI/Swagger)
- **Database:** SQLite (default for development)
- **Utilities:** Python-dotenv, Pillow

## Getting Started

### Development Installation

Installation requires an active version of Python 3.

1. Clone this repository.
2. Create a virtual environment and activate it:

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install all dependencies.

   ```
   pip3 install -r requirements.txt
   ```

4. Create an .env file in the root project folder with the following items:

   ```
   DEBUG=True
   ```

5. Create a database and start serving the dev server with the following commands:

   ```
   python3 manage.py migrate
   python3 manage.py runserver
   ```

5.1. To have access to site and admin page, create a superuser like so:

```
python3 manage.py createsuperuser
```

6. Access the development site at [http://localhost:8000/](http://localhost:8000/).
