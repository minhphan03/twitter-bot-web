import unittest
from src.wordfinder import webscraping


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(webscraping("hello"), "an expression or gesture of greeting")


if __name__ == '__main__':
    unittest.main()
