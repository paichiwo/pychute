import unittest
from pychute.helpers import format_date_string, format_duration_string


class TestStringFormatting(unittest.TestCase):

    def test_format_date_string(self):
        test_date_string = " First published at 15:00 UTC on May 4th, 2024. "

        formatted_date = format_date_string(test_date_string)
        self.assertEqual(formatted_date, "04-05-2024 15:00:00")

        with self.assertRaises(ValueError):
            format_date_string("2024-05-07 15:00:00")

        with self.assertRaises(ValueError):
            format_date_string("Invalid Date String")

    def test_format_duration_string(self):
        self.assertEqual(format_duration_string("01:23"), "00:01:23")

        self.assertEqual(format_duration_string("10:05:30"), "10:05:30")

        self.assertEqual(format_duration_string("12:30"), "00:12:30")


if __name__ == '__main__':
    unittest.main()
