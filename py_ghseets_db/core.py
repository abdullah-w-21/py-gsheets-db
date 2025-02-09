from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCreds
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GSheetsDB:
    """
    A Python library for using Google Sheets as a database.
    Provides simple database-like operations for Google Sheets.
    """

    def __init__(self, credentials_path: str, spreadsheet_id: str):
        """
        Initialize the Google Sheets database connection.

        Args:
            credentials_path (str): Path to the Google Sheets API credentials JSON file
            spreadsheet_id (str): ID of the Google Sheet to use as database
        """
        self.spreadsheet_id = spreadsheet_id
        self.credentials = ServiceAccountCreds.from_service_account_file(credentials_path)
        self.service = build('sheets', 'v4', credentials=self.credentials)
        self.sheet = self.service.spreadsheets()

    def create_table(self, table_name: str, columns: List[str]) -> bool:
        """
        Create a new worksheet (table) in the spreadsheet.

        Args:
            table_name (str): Name of the worksheet/table to create
            columns (List[str]): List of column names

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create new sheet
            body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': table_name
                        }
                    }
                }]
            }
            self.sheet.batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()

            # Add column headers
            range_name = f'{table_name}!A1:{chr(65 + len(columns) - 1)}1'
            body = {
                'values': [columns]
            }
            self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            return True

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def insert(self, table_name: str, data: Dict[str, Any]) -> bool:
        """
        Insert a new row into the specified table.

        Args:
            table_name (str): Name of the worksheet/table
            data (Dict[str, Any]): Dictionary of column:value pairs to insert

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get existing headers
            range_name = f'{table_name}!1:1'
            headers = self.sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute().get('values', [[]])[0]

            # Prepare row data according to headers
            row_data = [data.get(header, '') for header in headers]

            # Append row
            range_name = f'{table_name}!A:Z'
            body = {
                'values': [row_data]
            }
            self.sheet.values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()

            return True

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def select(self, table_name: str, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Select data from the specified table.

        Args:
            table_name (str): Name of the worksheet/table
            columns (Optional[List[str]]): List of columns to select. If None, selects all columns.

        Returns:
            List[Dict[str, Any]]: List of dictionaries containing the selected data
        """
        try:
            range_name = f'{table_name}!A:Z'
            result = self.sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            if not values:
                return []

            headers = values[0]
            if columns:
                # Get indices of requested columns
                col_indices = [headers.index(col) for col in columns if col in headers]
                # Filter headers
                headers = [headers[i] for i in col_indices]
            else:
                col_indices = range(len(headers))

            # Convert rows to dictionaries
            data = []
            for row in values[1:]:
                row_dict = {}
                for i, header in zip(col_indices, headers):
                    row_dict[header] = row[i] if i < len(row) else ''
                data.append(row_dict)

            return data

        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def update(self, table_name: str, where: Dict[str, Any], values: Dict[str, Any]) -> bool:
        """
        Update rows in the specified table that match the where condition.

        Args:
            table_name (str): Name of the worksheet/table
            where (Dict[str, Any]): Dictionary of column:value pairs to match
            values (Dict[str, Any]): Dictionary of column:value pairs to update

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get all data first
            data = self.select(table_name)
            if not data:
                return False

            # Find matching rows
            headers = list(data[0].keys())
            range_name = f'{table_name}!A:Z'

            updates = []
            for i, row in enumerate(data):
                # Check if row matches where condition
                if all(row.get(k) == v for k, v in where.items()):
                    # Update matching row
                    updated_row = row.copy()
                    updated_row.update(values)
                    updates.append([updated_row.get(h, '') for h in headers])
                else:
                    updates.append([row.get(h, '') for h in headers])

            # Update sheet
            body = {
                'values': [headers] + updates
            }
            self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            return True

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def delete(self, table_name: str, where: Dict[str, Any]) -> bool:
        """
        Delete rows from the specified table that match the where condition.

        Args:
            table_name (str): Name of the worksheet/table
            where (Dict[str, Any]): Dictionary of column:value pairs to match

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Get all data first
            data = self.select(table_name)
            if not data:
                return False

            # Find non-matching rows (rows to keep)
            headers = list(data[0].keys())
            range_name = f'{table_name}!A:Z'

            kept_rows = []
            for row in data:
                # Keep row if it doesn't match where condition
                if not all(row.get(k) == v for k, v in where.items()):
                    kept_rows.append([row.get(h, '') for h in headers])

            # Update sheet with kept rows
            body = {
                'values': [headers] + kept_rows
            }
            self.sheet.values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            return True

        except HttpError as error:
            print(f"An error occurred: {error}")
            return False