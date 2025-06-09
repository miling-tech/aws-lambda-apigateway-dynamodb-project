import unittest
from main import isTableExisting

class mainTest(unittest.TestCase):
    def test_isTableExisting(self):
        result = isTableExisting(table_name='Roles')
        expected = True
        self.assertEqual(expected, result)

    def test_isnotTableExisting(self):
        result = isTableExisting(table_name='123')
        expected = False
        self.assertEqual(expected, result)
