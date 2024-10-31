import unittest
import tempfile
import hashlib
import os

# Function to be tested
def archive_data(data, archive_path):
	with open(archive_path, "wb") as f:
		f.write(data)

def check_archive_integrity(archive_path):
	with open(archive_path, "rb") as f:
		data = f.read()
		return hashlib.md5(data).hexdigest()

class TestArchiveIntegrity(unittest.TestCase):

	def test_archive_integrity(self):
		# Test data
		test_data = b"This is some data to be archived."
		expected_hash = hashlib.md5(test_data).hexdigest()

		with tempfile.TemporaryDirectory() as temp_dir:
			archive_path = os.path.join(temp_dir, "test.archive")

			# Archive the data
			archive_data(test_data, archive_path)

			# Check archive integrity
			computed_hash = check_archive_integrity(archive_path)

			self.assertEqual(computed_hash, expected_hash, "Archive integrity check failed")

if __name__ == "__main__":
	unittest.main()
