import unittest
from dynamodb import is_table_existing

class DynamodbTest(unittest.TestCase):
    def test_isTableExisting(self):
        result = is_table_existing(table_name='Roles')
        expected = True
        self.assertEqual(expected, result)

    def test_isnotTableExisting(self):
        result = is_table_existing(table_name='123')
        expected = False
        self.assertEqual(expected, result)
