import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tests.test_data_pipeline import TestDataPipeline

if __name__ == '__main__':
    print("Running Automated Data Analysis Portfolio Test Suite...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDataPipeline)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
