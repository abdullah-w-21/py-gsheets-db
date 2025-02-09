import unittest
from unittest.mock import patch, MagicMock
from py_ghseets_db import GSheetsDB


class TestGSheetsDB(unittest.TestCase):
    def setUp(self):
        self.credentials_path = "fake_credentials.json"
        self.spreadsheet_id = "fake_spreadsheet_id"

        # Create mock service
        self.mock_service = MagicMock()
        self.mock_sheets = MagicMock()
        self.mock_service.spreadsheets.return_value = self.mock_sheets

        # Patch the build function
        self.build_patcher = patch('gsheets_db.core.build')
        self.mock_build = self.build_patcher.start()
        self.mock_build.return_value = self.mock_service

        # Patch the Credentials
        self.creds_patcher = patch('gsheets_db.core.ServiceAccountCreds')
        self.mock_creds = self.creds_patcher.start()

        # Initialize the database
        self.db = GSheetsDB(self.credentials_path, self.spreadsheet_id)

    def tearDown(self):
        self.build_patcher.stop()
        self.creds_patcher.stop()

    def test_create_table(self):
        # Setup
        columns = ["id", "name", "email"]
        self.mock_sheets.batchUpdate.return_value.execute.return_value = {}
        self.mock_sheets.values.return_value.update.return_value.execute.return_value = {}

        # Execute
        result = self.db.create_table("test_table", columns)

        # Assert
        self.assertTrue(result)
        self.mock_sheets.batchUpdate.assert_called_once()
        self.mock_sheets.values.return_value.update.assert_called_once()

    def test_insert(self):
        # Setup
        test_data = {"id": "1", "name": "Test User", "email": "test@example.com"}
        self.mock_sheets.values.return_value.get.return_value.execute.return_value = {
            "values": [["id", "name", "email"]]
        }
        self.mock_sheets.values.return_value.append.return_value.execute.return_value = {}

        # Execute
        result = self.db.insert("test_table", test_data)

        # Assert
        self.assertTrue(result)
        self.mock_sheets.values.return_value.append.assert_called_once()

    def test_select(self):
        # Setup
        mock_data = {
            "values": [
                ["id", "name", "email"],
                ["1", "Test User", "test@example.com"]
            ]
        }
        self.mock_sheets.values.return_value.get.return_value.execute.return_value = mock_data

        # Execute
        result = self.db.select("test_table")

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "1")
        self.assertEqual(result[0]["name"], "Test User")
        self.assertEqual(result[0]["email"], "test@example.com")

    def test_update(self):
        # Setup
        mock_data = {
            "values": [
                ["id", "name", "email"],
                ["1", "Test User", "test@example.com"]
            ]
        }
        self.mock_sheets.values.return_value.get.return_value.execute.return_value = mock_data
        self.mock_sheets.values.return_value.update.return_value.execute.return_value = {}

        # Execute
        result = self.db.update(
            "test_table",
            where={"id": "1"},
            values={"name": "Updated User"}
        )

        # Assert
        self.assertTrue(result)
        self.mock_sheets.values.return_value.update.assert_called_once()

    def test_delete(self):
        # Setup
        mock_data = {
            "values": [
                ["id", "name", "email"],
                ["1", "Test User", "test@example.com"],
                ["2", "Other User", "other@example.com"]
            ]
        }
        self.mock_sheets.values.return_value.get.return_value.execute.return_value = mock_data
        self.mock_sheets.values.return_value.update.return_value.execute.return_value = {}

        # Execute
        result = self.db.delete("test_table", where={"id": "1"})

        # Assert
        self.assertTrue(result)
        self.mock_sheets.values.return_value.update.assert_called_once()


if __name__ == '__main__':
    unittest.main()