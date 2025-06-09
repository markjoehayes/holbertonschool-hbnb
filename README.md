```markdown
# Holberton Airbnb Clone

## Project Overview
This project is a foundational clone of the Airbnb web application, developed as part of the Holberton School curriculum. It implements a command-line interpreter (console) for managing Airbnb-related objects like `User`, `Place`, `State`, `City`, `Amenity`, and `Review`.

The project demonstrates proficiency in:
- Python programming
- Object-Oriented Programming (OOP)
- JSON serialization/deserialization
- Software engineering principles

## Installation
1. Clone the repository:
```bash
git clone https://github.com/markjoehayes/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

2. (Optional) Set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Usage
### Starting the Console
```bash
python3 console.py
```

### Available Commands
| Command | Description |
|---------|-------------|
| `create <class>` | Create new instance |
| `show <class> <id>` | Show instance details |
| `destroy <class> <id>` | Delete instance |
| `all [class]` | List all instances |
| `update <class> <id> <attr> <value>` | Update instance |
| `help` | Show commands |
| `quit` | Exit console |

### Examples
```bash
(hbnb) create User
(hbnb) all User
(hbnb) show User 1234-1234-1234
(hbnb) update User 1234-1234-1234 first_name "John"
(hbnb) quit
```

## File Storage
- Uses JSON serialization
- Saves to `file.json` automatically
- Loads objects on startup

## Testing
Run all tests:
```bash
python3 -m unittest discover tests
```

## UML Diagram
```
BaseModel
    ↑
    ├── User
    ├── State
    ├── City
    ├── Amenity
    ├── Place
    └── Review
```

## Authors
- Mark Joe Hayes ([GitHub](https://github.com/markjoehayes))
- Giann Pabon

## License
Educational use as part of Holberton School curriculum.
```
