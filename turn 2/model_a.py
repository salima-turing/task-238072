import unittest
import tempfile
import hashlib
import os
import shutil

CHUNK_SIZE = 65536  # 64KB chunk size for reading large files

# Function to be tested
def archive_data(data_path, archive_path):
	with open(data_path, "rb") as src, open(archive_path, "wb") as dest:
		shutil.copyfileobj(src, dest)

def check_archive_integrity(archive_path):
	md5_hash = hashlib.md5()
	with open(archive_path, "rb") as f:
		for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
			md5_hash.update(chunk)
	return md5_hash.hexdigest()

class TestArchiveIntegrity(unittest.TestCase):

	def test_archive_integrity_large_file(self):
		# Create a temporary large file for testing
		with tempfile.NamedTemporaryFile(delete=False) as temp_data_file:
			temp_data_file.write(b"\0" * 1024 * 1024 * 100)  # 100MB of zero data
			temp_data_file.close()

			expected_hash = check_archive_integrity(temp_data_file.name)

		with tempfile.TemporaryDirectory() as temp_dir:
			archive_path = os.path.join(temp_dir, "test.archive")

			# Archive the large file
			archive_data(temp_data_file.name, archive_path)

			# Check archive integrity
			computed_hash = check_archive_integrity(archive_path)

			self.assertEqual(computed_hash, expected_hash, "Archive integrity check failed for large file")

		# Cleanup the temporary large file
		os.remove(temp_data_file.name)

if __name__ == "__main__":
	unittest.main()
