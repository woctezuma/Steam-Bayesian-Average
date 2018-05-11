import time
import unittest

import load_data


class TestLoadDataMethods(unittest.TestCase):

    def test_get_data_path(self):
        self.assertEqual(load_data.get_data_path(), 'data/')

    def test_get_steamdb_filename(self):
        self.assertEqual(load_data.get_steamdb_filename(), 'data/steamdb.txt')

    def test_get_steamspy_filename(self):
        self.assertEqual(load_data.get_steamspy_filename(), 'data/' + time.strftime('%Y%m%d') + '_steamspy.json')

    def test_load_steamdb_data(self):
        self.assertGreater(len(load_data.load_steamdb_data(verbose=True)), 0)

    def test_load_steamspy_data(self):
        # First run: download data from Internet
        self.assertGreater(len(load_data.load_steamspy_data()), 0)
        # Second run: load cached data
        self.assertGreater(len(load_data.load_steamspy_data()), 0)

    def test_load_filtered_data(self):
        self.assertGreater(len(load_data.load_filtered_data(verbose=True)), 0)

    def test_compare_data(self):
        self.assertTrue(load_data.compare_data(verbose=True))

    def test_main(self):
        self.assertTrue(load_data.main())


if __name__ == '__main__':
    unittest.main()
