from unittest import TestCase
from hello_gh_actions.fizzbuzz import fizzbuzz


class TestFizzBuzz(TestCase):

    def test_valid_input(self):
        self.assertEqual('fizzbuzz', fizzbuzz(0))
        self.assertEqual('', fizzbuzz(4))
        self.assertEqual('fizz', fizzbuzz(5))
        self.assertEqual('buzz', fizzbuzz(7))
        self.assertEqual('fizzbuzz', fizzbuzz(35))

    def test_invalid_input(self):
        with self.assertRaisesRegex(TypeError, 'int expected'):
            fizzbuzz('4')

        with self.assertRaisesRegex(ValueError, 'Positive input expected'):
            fizzbuzz(-20)
