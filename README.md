# Holberton Airbnb Clone

## Project Overview
Command-line Airbnb clone for managing:
- `User`, `Place`, `State`, `City`, `Amenity`, `Review`

## Installation
```bash
git clone https://github.com/markjoehayes/holbertonschool-hbnb.git
cd holbertonschool-hbnb
python3 -m venv venv  # Optional
source venv/bin/activate

Usage
bash

python3 console.py

Commands
Command	Example	Description
create	create User	New instance
show	show User 123	Display instance
all	all Place	List objects
update	update User 123 name "John"	Modify attribute
destroy	destroy User 123	Delete instance
Examples
bash

(hbnb) create Place
(hbnb) update Place 456 price 99
(hbnb) show Place 456
(hbnb) quit

Structure
text

BaseModel → User, Place, State, City, Amenity, Review

Tests
bash

python3 -m unittest discover tests

Authors

    Mark Joe Hayes

    Giann Pabon

License

Holberton School
