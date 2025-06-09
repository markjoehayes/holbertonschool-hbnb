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

    (Optional) Set up a virtual environment:

bash

python3 -m venv venv
source venv/bin/activate

Usage
Starting the Console
bash

python3 console.py

Available Commands
Command	Description
create <class>	Create new instance
show <class> <id>	Show instance details
destroy <class> <id>	Delete instance
all [class]	List all instances
update <class> <id> <attr> <value>	Update instance
help	Show commands
quit	Exit console
Examples
bash

(hbnb) create User
(hbnb) all User
(hbnb) show User 1234-1234-1234
(hbnb) update User 1234-1234-1234 first_name "John"
(hbnb) quit

File Storage

    Uses JSON serialization

    Saves to file.json automatically

    Loads objects on startup

Testing

Run all tests:
bash

python3 -m unittest discover tests

UML Diagram
text

BaseModel
    ↑
    ├── User
    ├── State
    ├── City
    ├── Amenity
    ├── Place
    └── Review

Authors

    Mark Joe Hayes (GitHub)

    Giann Pabon

License

Educational use as part of Holberton School curriculum.
text


### How to use this:
1. **Click the "Copy" button** in the top-right corner of this code block
2. **Open your README.md file** in a text editor
3. **Paste** (Ctrl+V/Cmd+V) the entire content
4. **Save** the file

### Important Notes:
- The formatting will be preserved exactly as shown
- All markdown elements (headers, code blocks, tables) will work properly
- No extra spaces or formatting issues will be introduced
- The file will render correctly on GitHub and other markdown viewers

If you still experience issues, try:
1. Using a plain text editor (Notepad, VS Code, Sublime Text)
2. Ensuring your file has a `.md` extension
3. Checking line endings (use LF instead of CRLF)
