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
