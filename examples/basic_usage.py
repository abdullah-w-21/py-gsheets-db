from py_ghseets_db import GSheetsDB

def main():
    # Initialize the database
    db = GSheetsDB(
        credentials_path='path/to/your/credentials.json',
        spreadsheet_id='your-spreadsheet-id'  # Get this from your Google Sheet's URL
    )

    # Create a new table
    db.create_table('users', ['id', 'name', 'email', 'age'])

    # Insert some test data
    test_users = [
        {'id': '1', 'name': 'John Doe', 'email': 'john@example.com', 'age': '30'},
        {'id': '2', 'name': 'Jane Smith', 'email': 'jane@example.com', 'age': '25'},
    ]

    for user in test_users:
        db.insert('users', user)

    # Select all users
    all_users = db.select('users')
    print("All users:", all_users)

    # Select specific columns
    names_only = db.select('users', columns=['name', 'email'])
    print("Names and emails:", names_only)

    # Update a user
    db.update(
        'users',
        where={'id': '1'},
        values={'age': '31'}
    )

    # Delete a user
    db.delete('users', where={'id': '2'})

if __name__ == '__main__':
    main()