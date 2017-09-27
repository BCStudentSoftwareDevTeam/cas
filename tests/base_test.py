import os
from app import allImports
import unittest
import tempfile

class TestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_name = tempfile.mkstemp()
        allImports.app.config["TESTING"] = True
        self.app = allImports.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_name)


if __name__ == "__main__":
    unittest.main()