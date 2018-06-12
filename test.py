import unittest
from src import Plotter
from runme import get_csv_list, get_arguments


class TestCSVPlotter(unittest.TestCase):

    def test_minimum(self):
        args = get_arguments(['-d', 'placeholder', '-c', 'placeholder'])
        self.assertTrue(args.dir and args.cols)

    def test_default_name_dir(self):
        args = get_arguments(
            ['-d', 'ex*/my_examples', '-c', 'hunger', '--xaxis', 'timestamp', '-t', 'Pet Hunger Over Time',
             '-y', 'Hunger', '-x', 'Time (minutes)', '-I'])
        csv_list = get_csv_list(args)
        plot = Plotter(args, csv_list)
        self.assertEqual(plot.arg['name'], 'my_examples.png')


if __name__ == '__main__':
    unittest.main()
