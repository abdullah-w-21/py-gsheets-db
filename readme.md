# GSheetsDB

A Python library for using Google Sheets as a database. This library provides a simple interface to perform database-like operations on Google Sheets.

# py-gsheets-db

[![PyPI version](https://badge.fury.io/py/py-gsheets-db.svg)](https://badge.fury.io/py/py-gsheets-db)
[![Python Versions](https://img.shields.io/pypi/pyversions/py-gsheets-db.svg)](https://pypi.org/project/py-gsheets-db/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Simple CRUD operations (Create, Read, Update, Delete)
- Easy to use API
- Type hints for better IDE support
- Comprehensive error handling
- Flexible querying options

## Installation

```bash
pip install py-gsheets-db
```

## Prerequisites

Before using the library, you need to:

1. Set up Google Sheets API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Sheets API
   - Create service account credentials
   - Download the credentials JSON file

2. Create a Google Sheet and get its ID (from the URL)
3. Share your Google Sheet with the service account email (found in your credentials JSON)

## Usage

```python
from py_gsheets_db import GSheetsDB

# Initialize the database
db = GSheetsDB(
    credentials_path='path/to/credentials.json',
    spreadsheet_id='your-spreadsheet-id'
)

# Create a new table
db.create_table('users', ['id', 'name', 'email'])

# Insert data
db.insert('users', {
    'id': '1',
    'name': 'John Doe',
    'email': 'john@example.com'
})

# Select data
all_users = db.select('users')
specific_columns = db.select('users', columns=['name', 'email'])

# Update data
db.update(
    'users',
    where={'id': '1'},
    values={'name': 'John Smith'}
)

# Delete data
db.delete('users', where={'id': '1'})
```

## API Reference

### GSheetsDB

#### `__init__(credentials_path: str, spreadsheet_id: str)`
Initialize the Google Sheets database connection.

#### `create_table(table_name: str, columns: List[str]) -> bool`
Create a new worksheet (table) in the spreadsheet.

#### `insert(table_name: str, data: Dict[str, Any]) -> bool`
Insert a new row into the specified table.

#### `select(table_name: str, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]`
Select data from the specified table.

#### `update(table_name: str, where: Dict[str, Any], values: Dict[str, Any]) -> bool`
Update rows in the specified table that match the where condition.

#### `delete(table_name: str, where: Dict[str, Any]) -> bool`
Delete rows from the specified table that match the where condition.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.