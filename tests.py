import time
import unittest

import compute_bayesian_average
import load_data
import remove_noise


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


class TestRemoveNoiseMethods(unittest.TestCase):

    def test_main(self):
        self.assertTrue(remove_noise.main())


class TestComputeBayesianAverageMethods(unittest.TestCase):

    def test_print_ranking(self):
        data = {
            'The Behemoth': {'name': 'The Behemoth', 'bayesian_average': 0.905},
            'Valve': {'name': 'Valve', 'bayesian_average': 0.904},
            'Terry Cavanagh': {'name': 'Terry Cavanagh', 'bayesian_average': 0.888},
            '@unepic_fran': {'name': '@unepic_fran', 'bayesian_average': 0.882},
        }
        ranking = compute_bayesian_average.get_ranking(data)
        self.assertTrue(compute_bayesian_average.print_ranking(data, ranking, keyword=None, num_elements=3,
                                                               markdown_format=False))
        self.assertTrue(compute_bayesian_average.print_ranking(data, ranking, keyword=None, num_elements=3,
                                                               markdown_format=True))

    def test_main(self):
        self.assertTrue(compute_bayesian_average.main(verbose=True))


if __name__ == '__main__':
    unittest.main()
