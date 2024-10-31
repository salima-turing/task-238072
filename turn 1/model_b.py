import unittest
from unittest.mock import patch, mock_open
import hashlib
import os

# Function to be tested (imported from your archiving module)
from archive_utils import monitor_archive_integrity

class TestArchiveIntegrity(unittest.TestCase):

    def setUp(self):
        # Set up test data and expected results
        self.test_data = b"This is a test data for archiving."
        self.expected_checksum = hashlib.sha256(self.test_data).hexdigest()
        self.archive_file_path = '/path/to/archive/test_file.txt'

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=test_data)
    @patch('hashlib.sha256')
    def test_monitor_archive_integrity_pass(self, mock_sha256, mock_file, mock_exists):
        # Mock the file system and hash function behavior
        mock_exists.return_value = True
        mock_sha256.return_value.hexdigest.return_value = self.expected_checksum

        # Call the function under test
        result = monitor_archive_integrity(self.archive_file_path)

        # Verify the results
        self.assertTrue(result)
        mock_file.assert_called_once_with(self.archive_file_path, 'rb')
        mock_sha256.assert_called_once_with(self.test_data)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=test_data)
    @patch('hashlib.sha256')
    def test_monitor_archive_integrity_fail(self, mock_sha256, mock_file, mock_exists):
        # Mock the file system and hash function behavior to simulate integrity failure
        mock_exists.return_value = True
        mock_sha256.return_value.hexdigest.return_value = "InvalidChecksum"

        # Call the function under test
        result = monitor_archive_integrity(self.archive_file_path)

        # Verify the results
        self.assertFalse(result)
        mock_file.assert_called_once_with(self.archive_file_path, 'rb')
        mock_sha256.assert_called_once_with(self.test_data)

    @patch('os.path.exists')
    def test_monitor_archive_integrity_file_not_found(self, mock_exists):
        # Mock the file system to simulate file not found
        mock_exists.return_value = False

        # Call the function under test
        result = monitor_archive_integrity(self.archive_file_path)

        # Verify the results
        self.assertFalse(result)
        mock_exists.assert_called_once_with(self.archive_file_path)

if __name__ == '__main__':
    unittest.main()
