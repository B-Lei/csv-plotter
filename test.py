import unittest
from src import Plotter
from runme import get_csv_list, get_arguments


class TestCSVPlotter(unittest.TestCase):

    def test_min_args(self):
        args = get_arguments(['-d', 'foo', '-c', 'bar'])
        self.assertTrue(args.dir and args.cols)

    def test_csv_parsing_cat(self):
        args = get_arguments(['-f', 'ex*/my*/cat*', '-c', 'hunger', '-n', 'pet_hunger', '--xaxis', 'timestamp'])
        csv = get_csv_list(args)[0]
        self.assertEquals(csv.numrows, 14)
        self.assertEquals(len(csv.data), 2)

    def test_csv_parsing_dog(self):
        args = get_arguments(['-f', 'ex*/my*/dog*', '-c', 'hunger', '-n', 'pet_hunger', '--xaxis', 'timestamp'])
        csv = get_csv_list(args)[0]
        self.assertEquals(csv.numrows, 12)
        self.assertEquals(len(csv.data), 2)

    def test_plotter_default_name_dir(self):
        args = get_arguments(['-d', 'ex*/my*', '-c', 'hunger', '-n', 'pet_hunger'])
        csv_list = get_csv_list(args)
        plot = Plotter(args, csv_list)
        self.assertEqual(plot.arg['name'], 'pet_hunger.html')

    def test_plotter_arg_filename(self):
        args = get_arguments(['-d', 'ex*/my*', '-c', 'hunger', '-I'])
        csv_list = get_csv_list(args)
        plot = Plotter(args, csv_list)
        self.assertEqual(plot.arg['name'], 'my_examples.png')


if __name__ == '__main__':
    unittest.main()
