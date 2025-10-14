A RESTful API for a vacation rental platform built with Flask.

## Project Structure
hbnb/
├── app/ # Main application package
│ ├── init.py # Flask application factory
│ ├── models/ # Data models and business logic
│ │ ├── init.py # Models package initialization
│ │ ├── base_model.py # Base model with common functionality
│ │ ├── user.py # User model
│ │ ├── place.py # Place/Property model
│ │ ├── amenity.py # Amenity model
│ │ └── review.py # Review model
│ ├── api/ # API routes and endpoints
│ │ ├── init.py # API package initialization
│ │ └── v1/ # API version 1
│ │ ├── init.py
│ │ ├── users.py # User-related endpoints
│ │ ├── places.py # Place-related endpoints
│ │ ├── amenities.py
│ │ └── reviews.py
│ ├── services/ # Business logic layer
│ │ ├── init.py
│ │ └── facade.py # Service facade pattern
│ └── persistence/ # Data persistence layer
│ ├── init.py
│ └── repository.py # Data access abstraction
├── instance/ # Instance-specific config (not in version control)
├── venv/ # Python virtual environment (not in version control)
├── run.py # Application entry point
├── .flaskenv # Flask environment variables
├── .env # Environment variables (not in version control)
├── .gitignore # Git ignore rules
└── requirements.txt # Python dependencies


## Key Files Description

- **`run.py`**: Main entry point that starts the Flask development server
- **`app/__init__.py`**: Creates and configures the Flask application instance
- **`app/models/`**: Contains all data models implementing the business logic
- **`app/api/v1/`**: REST API endpoints organized by resource type
- **`app/services/`**: Business logic layer separating concerns from API and persistence
- **`app/persistence/`**: Data access layer abstracting storage implementation

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hbnb
```
### 2. Create Virtual Environment
```bash
python3 -m venv venv
```
### 3. Install Dependancies
```bash
pip install -r requirements.txt
```
### 4. Environment Configuration
Create .flaskenv file for environment-specific variables:
```bash
export FLASK_APP=run.py > .flaskenv


source venv/bin/activate
```
