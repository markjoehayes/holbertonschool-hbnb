# Holberton Airbnb Clone

## Project Overview

This project is a foundational clone of the Airbnb web application, developed as part of the Holberton School curriculum. It primarily implements a command-line interpreter (console) for managing various objects related to the Airbnb platform, such as `User`, `Place`, `State`, `City`, `Amenity`, and `Review`.

The project demonstrates proficiency in:

* **Python:** Core language features and scripting.
* **Object-Oriented Programming (OOP):** Class design, inheritance, and encapsulation.
* **Serialization/Deserialization:** Persisting and loading objects using JSON.
* **Software Engineering Principles:** Modularity, testing, and documentation.

## Installation

To get a copy of this project up and running on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/markjoehayes/holbertonschool-hbnb.git](https://github.com/markjoehayes/holbertonschool-hbnb.git)
    cd holbertonschool-hbnb
    ```

2.  ** (Optional) Set up a virtual environment:** It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

## Usage

### Starting the Console

Once installed, you can start the console by running:

```bash
python3 console.py

You will see a prompt (hbnb) indicating the console is ready for commands.
Available Commands

The console supports the following commands for object management:

    create <class>: Creates a new instance of the specified class (e.g., User, Place).
    show <class> <id>: Displays the string representation of an instance given its class and ID.
    destroy <class> <id>: Deletes an instance based on its class and ID.
    all [class]: Lists all instances, or all instances of a specific class if provided.
    update <class> <id> <attribute_name> <attribute_value>: Updates an attribute of an instance. The attribute_value should be properly quoted if it contains spaces.
    help: Shows a list of available commands and their descriptions.
    quit: Exits the console.

Examples

Here are some common interactions with the console:
Plaintext

(hbnb) create User
# A new User instance is created, and its ID is printed
(hbnb) all User
# Lists all User instances currently in storage
(hbnb) show User 1234-1234-1234
# Displays details of the User with the specified ID
(hbnb) update User 1234-1234-1234 first_name "John"
# Updates the 'first_name' attribute of the User instance
(hbnb) quit
# Exits the console

File Storage

The project utilizes JSON serialization and deserialization for data persistence. All created objects are automatically saved to a file named file.json when the console exits. Conversely, when the console starts, all objects are loaded from file.json, ensuring data continuity between sessions.
Testing

Comprehensive unit tests are provided to ensure the correctness and robustness of the application's components. To run the test suite, execute the following command from the project root:
Bash

python3 -m unittest discover tests

UML Diagram

The project's class structure and inheritance hierarchy are as follows:

BaseModel
    ↑
    ├── User
    ├── State
    ├── City
    ├── Amenity
    ├── Place
    └── Review

BaseModel serves as the base class for all other models, providing common attributes and functionalities like id, created_at, and updated_at.
Authors

    Mark Joe Hayes - GitHub Profile
    Giann Pabon
    Holberton School Staff (for curriculum guidance and foundational concepts)

License

This project is part of the Holberton School curriculum and is provided for educational purposes.
