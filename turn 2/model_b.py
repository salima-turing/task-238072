import unittest
import tempfile
import hashlib
import os
import subprocess


# Function to be tested
def archive_data(data, archive_path):
    with open(archive_path, "wb") as f:
        f.write(data)


def check_archive_integrity(archive_path):
    md5sum_proc = subprocess.Popen(["md5sum", archive_path], stdout=subprocess.PIPE)
    md5sum, _ = md5sum_proc.communicate()
    return md5sum.decode().split()[0]


class TestArchiveIntegrity(unittest.TestCase):

    def test_archive_integrity_large_file(self):
        # Generate a large test file (20 MB) for demonstration
        test_data = os.urandom(20 * 1024 * 1024)
        expected_hash = hashlib.md5(test_data).hexdigest()

        with tempfile.TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, "test.archive")

            # Archive the data
            archive_data(test_data, archive_path)

            # Check archive integrity using md5sum
            computed_hash = check_archive_integrity(archive_path)

            self.assertEqual(computed_hash, expected_hash, "Archive integrity check failed for large file")


if __name__ == "__main__":
    unittest.main()
